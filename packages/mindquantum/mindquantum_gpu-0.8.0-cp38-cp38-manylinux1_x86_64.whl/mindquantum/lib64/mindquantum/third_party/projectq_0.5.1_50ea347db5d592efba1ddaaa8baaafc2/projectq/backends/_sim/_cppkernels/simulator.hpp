// Copyright 2017 ProjectQ-Framework (www.projectq.ch)
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#ifndef SIMULATOR_HPP_
#define SIMULATOR_HPP_

#include <complex>
#include <vector>

#include "intrin/kernels.hpp"

#include "core/utils.hpp"
#include "fusion.hpp"
#include "intrin/alignedallocator.hpp"
#include <algorithm>
#include <cassert>
#include <cstring>
#include <functional>
#include <map>
#include <random>
#include <tuple>

namespace projectq {
class Simulator {
public:
  using calc_type = double;
  using complex_type = std::complex<calc_type>;
  using StateVector = calc_type *;
  using Map = std::map<unsigned, unsigned>;
  using RndEngine = std::mt19937;
  using Term = std::vector<std::pair<unsigned, char>>;
  using TermsDict = std::vector<std::pair<Term, calc_type>>;
  using ComplexTermsDict = std::vector<std::pair<Term, complex_type>>;
  StateVector vec_;

  Simulator(unsigned seed = 1, unsigned N = 0)
      : N_(N), fusion_qubits_min_(4), fusion_qubits_max_(5), rnd_eng_(seed) {
    len_ = 1UL << (N_ + 1);
    vec_ = (StateVector)calloc(len_, sizeof(calc_type));
    vec_[0] = 1.; // all-zero initial state
    std::uniform_real_distribution<double> dist(0., 1.);
    rng_ = std::bind(dist, std::ref(rnd_eng_));
    for (unsigned i = 0; i < N_; i++)
      map_[i] = i;
  }

  template <class M>
  void apply_controlled_gate(M const &m, const std::vector<unsigned> &ids,
                             const std::vector<unsigned> &ctrl) {
    auto fused_gates = fused_gates_;
    fused_gates.insert(m, ids, ctrl);

    if (fused_gates.num_qubits() >= fusion_qubits_min_ &&
        fused_gates.num_qubits() <= fusion_qubits_max_) {
      fused_gates_ = fused_gates;
      run();
    } else if (fused_gates.num_qubits() > fusion_qubits_max_ ||
               (fused_gates.num_qubits() - ids.size()) >
                   fused_gates_.num_qubits()) {
      run();
      fused_gates_.insert(m, ids, ctrl);
    } else
      fused_gates_ = fused_gates;
  }

  calc_type get_expectation_value(TermsDict const &td,
                                  std::vector<unsigned> const &ids) {
    run();
    calc_type expectation = 0.;

    StateVector current_state = (StateVector)malloc(len_ * sizeof(calc_type));
    THRESHOLD_OMP_FOR(
        N_, mindquantum::nQubitTh,
        for (omp::idx_t i = 0; i < len_; ++i) { current_state[i] = vec_[i]; })
    for (auto const &term : td) {
      auto const &coefficient = term.second;
      apply_term(term.first, ids, {});
      calc_type delta = 0.;
            THRESHOLD_OMP(
                MQ_DO_PRAGMA(
                    omp parallel for reduction(+:delta) schedule(static)),
                N_, mindquantum::nQubitTh,
                for (omp::idx_t i = 0; i < (len_ >> 1); ++i) {
        auto const a1 = current_state[2 * i];
        auto const b1 = -current_state[2 * i + 1];
        auto const a2 = vec_[2 * i];
        auto const b2 = vec_[2 * i + 1];
        delta += a1 * a2 - b1 * b2;
        // reset vec_
        vec_[2 * i] = current_state[2 * i];
        vec_[2 * i + 1] = current_state[2 * i + 1];
                })
            expectation += coefficient * delta;
    }
    if (NULL != current_state) {
      free(current_state);
      current_state = NULL;
    }
    return expectation;
  }

  void apply_qubit_operator(ComplexTermsDict const &td,
                            std::vector<unsigned> const &ids) {
    run();
    StateVector new_state = (StateVector)calloc(len_, sizeof(calc_type));
    StateVector current_state = (StateVector)malloc(len_ * sizeof(calc_type));
    THRESHOLD_OMP_FOR(
        N_, mindquantum::nQubitTh,
        for (omp::idx_t i = 0; i < len_; ++i) { current_state[i] = vec_[i]; })
    for (auto const &term : td) {
      auto const &coefficient = term.second;
      apply_term(term.first, ids, {});
      THRESHOLD_OMP_FOR(
          N_, mindquantum::nQubitTh,
          for (omp::idx_t i = 0; i < (len_ >> 1); ++i) {
            new_state[2 * i] += coefficient.real() * vec_[2 * i] -
                                coefficient.imag() * vec_[2 * i + 1];
            new_state[2 * i + 1] += coefficient.real() * vec_[2 * i + 1] +
                                    coefficient.imag() * vec_[2 * i];
            vec_[2 * i] = current_state[2 * i];
            vec_[2 * i + 1] = current_state[2 * i + 1];
          })
    }
    if (NULL != vec_)
      free(vec_);
    vec_ = new_state;
    if (NULL != new_state)
      new_state = NULL;
    if (NULL != current_state) {
      free(current_state);
      current_state = NULL;
    }
  }

  void emulate_time_evolution(TermsDict const &tdict, calc_type const &time,
                              std::vector<unsigned> const &ids,
                              std::vector<unsigned> const &ctrl) {
    run();
    complex_type I(0., 1.);
    calc_type tr = 0., op_nrm = 0.;
    TermsDict td;
    for (unsigned i = 0; i < tdict.size(); ++i) {
      if (tdict[i].first.size() == 0)
        tr += tdict[i].second;
      else {
        td.push_back(tdict[i]);
        op_nrm += std::abs(tdict[i].second);
      }
    }
    unsigned s = std::abs(time) * op_nrm + 1.;
    complex_type correction = std::exp(-time * I * tr / (double)s);
    auto output_state = copy(vec_, len_);
    auto ctrlmask = get_control_mask(ctrl);
    for (unsigned i = 0; i < s; ++i) {
      calc_type nrm_change = 1.;
      for (unsigned k = 0; nrm_change > 1.e-12; ++k) {
        auto coeff = (-time * I) / double(s * (k + 1));
        auto current_state = copy(vec_, len_);
        auto update = (StateVector)calloc(len_, sizeof(calc_type));
        for (auto const &tup : td) {
          apply_term(tup.first, ids, {});
          THRESHOLD_OMP_FOR(
              N_, mindquantum::nQubitTh, for (omp::idx_t j = 0; j < len_; ++j) {
                update[j] += vec_[j] * tup.second;
                vec_[j] = current_state[j];
              })
        }
        nrm_change = 0.;
                THRESHOLD_OMP(MQ_DO_PRAGMA(omp parallel for reduction(+:nrm_change) schedule(static)), N_, mindquantum::nQubitTh,
                    for (omp::idx_t j = 0; j < (len_ >> 1); ++j){
          complex_type tmp(update[2 * j], update[2 * j + 1]);
          tmp *= coeff;
          update[2 * j] *= std::real(tmp);
          update[2 * j + 1] *= std::imag(tmp);
          vec_[2 * j] = update[2 * j];
          vec_[2 * j + 1] = update[2 * j + 1];
          if ((j & ctrlmask) == ctrlmask) {
            output_state[2 * j] += update[2 * j];
            output_state[2 * j + 1] += update[2 * j + 1];
            nrm_change += std::sqrt(update[2 * j] * update[2 * j] +
                                    update[2 * j + 1] * update[2 * j + 1]);
          }
                    })
                nrm_change = std::sqrt(nrm_change);
                if (NULL != current_state) {
                  free(current_state);
                  current_state = NULL;
                }
                if (NULL != update) {
                  free(update);
                  update = NULL;
                }
      }
      THRESHOLD_OMP_FOR(
          N_, mindquantum::nQubitTh,
          for (omp::idx_t j = 0; j < (len_ >> 1); ++j) {
            if ((j & ctrlmask) == ctrlmask) {
              complex_type tmp(output_state[2 * j], output_state[2 * j + 1]);
              tmp *= correction;
              output_state[2 * j] = std::real(tmp);
              output_state[2 * j + 1] = std::imag(tmp);
            }
            vec_[2 * j] = output_state[2 * j];
            vec_[2 * j + 1] = output_state[2 * j + 1];
          })
    }
    if (NULL != output_state) {
      free(output_state);
      output_state = NULL;
    }
  }

  void set_wavefunction(StateVector const &wavefunction,
                        std::vector<unsigned> const &ordering) {
    run();
    if (NULL != vec_) {
      free(vec_);
    }
    vec_ = copy(wavefunction, len_);
  }

  void run() {
    if (fused_gates_.size() < 1)
      return;

    Fusion::Matrix m;
    Fusion::IndexVector ids, ctrls;

    fused_gates_.perform_fusion(m, ids, ctrls);

    for (auto &id : ids)
      id = map_[id];

    auto ctrlmask = get_control_mask(ctrls);

    switch (ids.size()) {
    case 1:
      THRESHOLD_OMP(MQ_DO_PRAGMA(omp parallel), N_, mindquantum::nQubitTh,
                    kernel(vec_, ids[0], m, ctrlmask, len_ >> 1);)
      break;
    case 2:
      THRESHOLD_OMP(MQ_DO_PRAGMA(omp parallel), N_, mindquantum::nQubitTh,
                    kernel(vec_, ids[1], ids[0], m, ctrlmask, len_ >> 1);)
      break;
    case 3:
      THRESHOLD_OMP(
          MQ_DO_PRAGMA(omp parallel), N_, mindquantum::nQubitTh,
          kernel(vec_, ids[2], ids[1], ids[0], m, ctrlmask, len_ >> 1);)
      break;
    case 4:
      THRESHOLD_OMP(
          MQ_DO_PRAGMA(omp parallel), N_, mindquantum::nQubitTh,
          kernel(vec_, ids[3], ids[2], ids[1], ids[0], m, ctrlmask, len_ >> 1);)
      break;
    case 5:
      THRESHOLD_OMP(MQ_DO_PRAGMA(omp parallel), N_, mindquantum::nQubitTh,
                    kernel(vec_, ids[4], ids[3], ids[2], ids[1], ids[0], m,
                           ctrlmask, len_ >> 1);)
      break;
    default:
      throw std::invalid_argument(
          "Gates with more than 5 qubits are not supported!");
    }

    fused_gates_ = Fusion();
  }

  std::vector<complex_type> cheat() {
    run();
    std::vector<complex_type> result;
    for (unsigned int i = 0; i < (len_ >> 1); i++) {
      result.push_back({vec_[2 * i], vec_[2 * i + 1]});
    }
    return result;
  }

  inline StateVector copy(StateVector source, unsigned len) {
    StateVector result = (StateVector)malloc(len * sizeof(calc_type));
    THRESHOLD_OMP_FOR(
        N_, mindquantum::nQubitTh,
        for (omp::idx_t i = 0; i < len; ++i) { result[i] = source[i]; })
    return result;
  }

  ~Simulator() {
    if (NULL != vec_)
      free(vec_);
  }

private:
  void apply_term(Term const &term, std::vector<unsigned> const &ids,
                  std::vector<unsigned> const &ctrl) {
    complex_type I(0., 1.);
    Fusion::Matrix X = {{0., 1.}, {1., 0.}};
    Fusion::Matrix Y = {{0., -I}, {I, 0.}};
    Fusion::Matrix Z = {{1., 0.}, {0., -1.}};
    std::vector<Fusion::Matrix> gates = {X, Y, Z};
    for (auto const &local_op : term) {
      unsigned id = ids[local_op.first];
      apply_controlled_gate(gates[local_op.second - 'X'], {id}, ctrl);
    }
    run();
  }
  std::size_t get_control_mask(std::vector<unsigned> const &ctrls) {
    std::size_t ctrlmask = 0;
    for (auto c : ctrls)
      ctrlmask |= (1UL << map_[c]);
    return ctrlmask;
  }

  bool check_ids(std::vector<unsigned> const &ids) {
    for (auto id : ids)
      if (!map_.count(id))
        return false;
    return true;
  }

  unsigned N_; // #qubits
  unsigned len_;
  Map map_;
  Fusion fused_gates_;
  unsigned fusion_qubits_min_, fusion_qubits_max_;
  RndEngine rnd_eng_;
  std::function<double()> rng_;
};
} // namespace projectq

#endif
