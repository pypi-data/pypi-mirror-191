#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "mindquantum::mq_base" for configuration "Release"
set_property(TARGET mindquantum::mq_base APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(mindquantum::mq_base PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/mindquantum/libmq_base.a"
  )

list(APPEND _cmake_import_check_targets mindquantum::mq_base )
list(APPEND _cmake_import_check_files_for_mindquantum::mq_base "${_IMPORT_PREFIX}/lib64/mindquantum/libmq_base.a" )

# Import target "mindquantum::mqsim_common" for configuration "Release"
set_property(TARGET mindquantum::mqsim_common APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(mindquantum::mqsim_common PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/mindquantum/libmqsim_common.a"
  )

list(APPEND _cmake_import_check_targets mindquantum::mqsim_common )
list(APPEND _cmake_import_check_files_for_mindquantum::mqsim_common "${_IMPORT_PREFIX}/lib64/mindquantum/libmqsim_common.a" )

# Import target "mindquantum::mqsim_vector_cpu" for configuration "Release"
set_property(TARGET mindquantum::mqsim_vector_cpu APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(mindquantum::mqsim_vector_cpu PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/mindquantum/libmqsim_vector_cpu.a"
  )

list(APPEND _cmake_import_check_targets mindquantum::mqsim_vector_cpu )
list(APPEND _cmake_import_check_files_for_mindquantum::mqsim_vector_cpu "${_IMPORT_PREFIX}/lib64/mindquantum/libmqsim_vector_cpu.a" )

# Import target "mindquantum::mqsim_vector_gpu" for configuration "Release"
set_property(TARGET mindquantum::mqsim_vector_gpu APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(mindquantum::mqsim_vector_gpu PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CUDA"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/mindquantum/libmqsim_vector_gpu.a"
  )

list(APPEND _cmake_import_check_targets mindquantum::mqsim_vector_gpu )
list(APPEND _cmake_import_check_files_for_mindquantum::mqsim_vector_gpu "${_IMPORT_PREFIX}/lib64/mindquantum/libmqsim_vector_gpu.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
