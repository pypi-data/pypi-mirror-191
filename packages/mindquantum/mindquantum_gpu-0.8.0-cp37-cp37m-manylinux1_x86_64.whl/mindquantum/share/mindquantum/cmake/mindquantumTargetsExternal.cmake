# ==============================================================================
#
# Copyright 2022 <Huawei Technologies Co., Ltd>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# ==============================================================================



# projectq (local)
find_package(projectq
             0.5.1
             CONFIG
             NO_DEFAULT_PATH
             PATHS
             "${MQ_PACKAGE_PREFIX_DIR}/lib64/mindquantum/third_party/projectq_0.5.1_50ea347db5d592efba1ddaaa8baaafc2"
             REQUIRED)
if(TARGET projectq::projectq AND NOT TARGET mindquantum::projectq)
  add_library(mindquantum::projectq ALIAS projectq::projectq)
endif()

# Eigen3 (local)
find_package(Eigen3
             3.4.0
             CONFIG
             NO_DEFAULT_PATH
             PATHS
             "${MQ_PACKAGE_PREFIX_DIR}/lib64/mindquantum/third_party/Eigen3_3.4.0_32fe71391656ea127eacd6b8ba0dd020"
             REQUIRED)
if(TARGET Eigen3::Eigen AND NOT TARGET mindquantum::eigen)
  add_library(mindquantum::eigen ALIAS Eigen3::Eigen)
endif()

# fmt (local)
find_package(fmt
             9.1.0
             CONFIG
             NO_DEFAULT_PATH
             PATHS
             "${MQ_PACKAGE_PREFIX_DIR}/lib64/mindquantum/third_party/fmt_9.1.0_9499136dd3c60f75aac6e1d006218185"
             REQUIRED)
if(TARGET fmt::fmt-header-only AND NOT TARGET mindquantum::fmt)
  add_library(mindquantum::fmt ALIAS fmt::fmt-header-only)
endif()

# pybind11 (system)
find_package(pybind11
             2.10.0
             REQUIRED)
if(TARGET pybind11::headers AND NOT TARGET mindquantum::pybind11_headers)
  add_library(mindquantum::pybind11_headers ALIAS pybind11::headers)
endif()
if(TARGET pybind11::module AND NOT TARGET mindquantum::pybind11_module)
  add_library(mindquantum::pybind11_module ALIAS pybind11::module)
endif()
if(TARGET pybind11::lto AND NOT TARGET mindquantum::pybind11_lto)
  add_library(mindquantum::pybind11_lto ALIAS pybind11::lto)
endif()

# nlohmann_json (local)
find_package(nlohmann_json
             3.11.2
             CONFIG
             NO_DEFAULT_PATH
             PATHS
             "${MQ_PACKAGE_PREFIX_DIR}/lib64/mindquantum/third_party/nlohmann_json_3.11.2_6a22c5133fe182fbb2b83cd4928729f0"
             REQUIRED)
if(TARGET nlohmann_json::nlohmann_json AND NOT TARGET mindquantum::json)
  add_library(mindquantum::json ALIAS nlohmann_json::nlohmann_json)
endif()

# Boost (local)
find_package(Boost
             1.78.0
             CONFIG
             NO_DEFAULT_PATH
             PATHS
             "${MQ_PACKAGE_PREFIX_DIR}/lib64/mindquantum/third_party/Boost_1.78.0_43078f9c7c8a07e85074772e2dcebba3"
             COMPONENTS
             serialization
             filesystem
             system
             REQUIRED)
if(TARGET Boost::headers AND NOT TARGET mindquantum::boost_headers)
  add_library(mindquantum::boost_headers ALIAS Boost::headers)
endif()
if(TARGET Boost::serialization AND NOT TARGET mindquantum::boost_serialization)
  add_library(mindquantum::boost_serialization ALIAS Boost::serialization)
endif()
if(TARGET Boost::system AND NOT TARGET mindquantum::boost_system)
  add_library(mindquantum::boost_system ALIAS Boost::system)
endif()
if(TARGET Boost::filesystem AND NOT TARGET mindquantum::boost_filesystem)
  add_library(mindquantum::boost_filesystem ALIAS Boost::filesystem)
endif()

# lru_cache (local)
find_package(lru_cache
             0.0.1
             CONFIG
             NO_DEFAULT_PATH
             PATHS
             "${MQ_PACKAGE_PREFIX_DIR}/lib64/mindquantum/third_party/lru_cache_0.0.1_d0c11ef9cf682b923338ed72cd38ecde"
             REQUIRED)
if(TARGET lru_cache::lru_cache AND NOT TARGET mindquantum::lru_cache)
  add_library(mindquantum::lru_cache ALIAS lru_cache::lru_cache)
endif()
