#ifndef OMP_COMPAT_HPP
#define OMP_COMPAT_HPP

#include <stdint.h>

namespace omp {
#ifdef _MSC_VER
typedef int64_t idx_t;
#else
typedef uint64_t idx_t;
#endif // _MSC_VER
}  // omp

#endif // OMP_COMPAT_HPP
