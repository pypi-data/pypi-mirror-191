#ifndef LRU_CACHE_LRU_CACHE_H_
#define LRU_CACHE_LRU_CACHE_H_

#include "dynamic_lru_cache.h"
namespace lru_cache::dynamic
{

// Create simple cache
template <typename Key, typename Value>
DynamicLruCache<Key, Value>
make_cache(std::size_t max_size) {
  return {max_size};
}

// Memoize a single-argument function.
template <std::size_t max_size, typename ValueProvider>
DynamicLruCache<internal::single_arg_t<ValueProvider>,
                internal::return_t<ValueProvider>,
                ValueProvider>
memoize_function(ValueProvider provider) {
  return {max_size, provider};
}
}

#include "static_lru_cache.h"
namespace lru_cache::staticc
{

// Create simple cache
template <std::size_t max_size, typename Key, typename Value>
StaticLruCache<Key, Value, max_size>
make_cache() {
  return {};
}

// Memoize a single-argument function.
template <std::size_t max_size, typename ValueProvider>
StaticLruCache<internal::single_arg_t<ValueProvider>,
               internal::return_t<ValueProvider>,
               max_size,
               ValueProvider>
memoize_function(ValueProvider provider) {
  return {provider};
}
}

#ifdef LRU_CACHE_HAS_ABSEIL_CPP

#include "node_lru_cache.h"
namespace lru_cache::node
{

// Create simple cache
template <typename Key, typename Value>
NodeLruCache<Key, Value>
make_cache(
    size_t max_size) {
  return {max_size};
}

// Memoize a single-argument function.
template <typename ValueProvider>
NodeLruCache<internal::single_arg_t<ValueProvider>,
             internal::return_t<ValueProvider>, ValueProvider>
memoize_function(
    size_t max_size, ValueProvider v) {
  return {max_size, v};
}
}

#endif // LRU_CACHE_HAS_ABSEIL_CPP
#endif  // LRU_CACHE_LRU_CACHE_H_
