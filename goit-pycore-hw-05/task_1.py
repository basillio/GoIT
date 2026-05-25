def caching_fibonacci():
    # 1. Create cache with base values
    cache = {0: 0, 1: 1}

    def fibonacci(n):
        # 2. Protection from negative numbers
        if n < 0:
            return 0

        # 3. Check cache using .get()
        result = cache.get(n)
        if result is not None:
            return result

        # 4. If not in cache — calculate and store
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)

        return cache[n]

    # 5. Return function as object
    return fibonacci

# Usage:
fib = caching_fibonacci()
print(fib(10))   # 55
print(fib(15))   # 610
print(fib(-5))   # 0