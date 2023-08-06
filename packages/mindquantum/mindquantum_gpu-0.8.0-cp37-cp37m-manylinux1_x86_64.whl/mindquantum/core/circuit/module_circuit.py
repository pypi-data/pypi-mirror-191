# Copyright 2021 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================

"""Module circuit."""

import warnings
from collections.abc import Iterable

import numpy as np

from mindquantum.core.gates import SWAP, BasicGate
from mindquantum.core.gates.basic import _check_gate_type

from .circuit import Circuit


class UN(Circuit):
    """
    Map a quantum gate to different objective qubits and control qubits.

    Args:
        gate (BasicGate): A quantum gate.
        maps_obj (Union[int, list[int]]): Objective qubits.
        maps_ctrl (Union[int, list[int]]): Control qubits. Default: None.

    Returns:
        Circuit, Return a quantum circuit.

    Examples:
        >>> from mindquantum.core.circuit import UN
        >>> from mindquantum.core.gates import X
        >>> circuit1 = UN(X, maps_obj = [0, 1], maps_ctrl = [2, 3])
        >>> print(circuit1)
        q0: ──X───────
              │
        q1: ──┼────X──
              │    │
        q2: ──●────┼──
                   │
        q3: ───────●──
        >>> from mindquantum.core.gates import SWAP
        >>> circuit2 = UN(SWAP, maps_obj =[[0, 1], [2, 3]]).x(2, 1)
        >>> print(circuit2)
        q0: ──@───────
              │
        q1: ──@────●──
                   │
        q2: ──@────X──
              │
        q3: ──@───────
    """

    def __init__(self, gate: BasicGate, maps_obj, maps_ctrl=None):
        """Initialize a UN object."""
        _check_gate_type(gate)
        if isinstance(maps_obj, Iterable):
            if maps_ctrl is None:
                gates = [gate.on(i) for i in maps_obj]
            else:
                if isinstance(maps_ctrl, Iterable):
                    gates = [gate.on(maps_obj[i], maps_ctrl[i]) for i in range(len(maps_obj))]
                else:
                    gates = [gate.on(i, maps_ctrl) for i in maps_obj]
        else:
            if maps_ctrl is None:
                gates = [gate.on(i) for i in range(maps_obj)]
            else:
                if isinstance(maps_ctrl, Iterable):
                    gates = [gate.on(maps_obj, i) for i in maps_ctrl]
                else:

                    gates = [gate.on(maps_obj, maps_ctrl)]
        Circuit.__init__(self, gates)


class SwapParts(Circuit):
    """
    Swap two different part of quantum circuit, with or without control qubits.

    Args:
        a (Iterable): The first part you need to swap.
        b (Iterable): The second part you need to swap.
        maps_ctrl (int, Iterable): Control the swap by a single qubit or by
            different qubits or just no control qubit. Default: None.

    Examples:
        >>> from mindquantum.core.circuit import SwapParts
        >>> SwapParts([1, 2], [3, 4], 0)
        q0: ──●────●──
              │    │
        q1: ──@────┼──
              │    │
        q2: ──┼────@──
              │    │
        q3: ──@────┼──
                   │
        q4: ───────@──
    """

    def __init__(self, a: Iterable, b: Iterable, maps_ctrl=None):
        """Initialize a SwapParts object."""
        if not isinstance(a, Iterable) or not isinstance(b, Iterable):
            raise Exception("Swap part should be iterable!")
        maps = [[a[i], b[i]] for i in range(len(a))]
        Circuit.__init__(self, UN(SWAP, maps, maps_ctrl))


class U3(Circuit):
    r"""
    This circuit represent arbitrary single qubit gate.

    U3 gate with matrix as:

    .. math::

        U3(\theta, \phi, \lambda) =
        \begin{pmatrix}
           cos \left( \frac{\theta}{2} \right) & -e^{i \lambda} sin \left( \frac{\theta}{2} \\
        e^{i \phi} sin \left( \frac{\theta}{2} & e^{i (\phi + \lambda)} cos \left( \frac{\theta}{2}
        \end{pmatrix}

    It can be decomposed as:

    .. math::

        U3(\theta, \phi, \lambda) = RZ(\phi) RX(-\pi/2) RZ(\theta) RX(\pi/2) RZ(\lambda)

    Args:
        theta (Union[numbers.Number, dict, ParameterResolver]): First parameter for U3 circuit.
        phi (Union[numbers.Number, dict, ParameterResolver]): Second parameter for U3 circuit.
        lam (Union[numbers.Number, dict, ParameterResolver]): Third parameter for U3 circuit.
        obj_qubit (int): Which qubit the U3 circuit will act on. Default: None.

    Examples:
        >>> from mindquantum.core.circuit import U3
        >>> U3('theta','phi','lambda')
        q0: ──RZ(lambda)────RX(π/2)────RZ(theta)────RX(-π/2)────RZ(phi)──
    """

    def __init__(self, theta, phi, lam, obj_qubit=None):
        """Initialize a U3 object."""
        warnings.warn(
            "U3 from circuit is deprecated, please use U3 as a gate from mindquantum.core.gates.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        if obj_qubit is None:
            obj_qubit = 0
        circ = Circuit()
        circ.rz(lam, obj_qubit)
        circ.rx(np.pi / 2, obj_qubit)
        circ.rz(theta, obj_qubit)
        circ.rx(-np.pi / 2, obj_qubit)
        circ.rz(phi, obj_qubit)
        Circuit.__init__(self, circ)
