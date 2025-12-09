# a = 10
# b = 5
# c = a + b
# print(c)

#decorator function
# def my_decorator(func):
#     def inner():
#         print("Before function runs")
#         func()
#         print("After function runs")
#     return inner

# @my_decorator
# def say_hello():
#     print("Hello!")

# say_hello()



def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

for i in range(10):
    print(fib(i), end=" ")
