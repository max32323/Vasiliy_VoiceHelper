# first line: 7
@mem.cache
def fib(n):
    if n < 2:
        return n
    else:
        return fib(n-1) + fib(n-2)
