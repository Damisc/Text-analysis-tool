fizz = 3
buzz = 5
numRange = 50

for num in range(1, numRange + 1):
    if num % fizz == 0 and num % buzz == 0:
        print("FizzBuzz")
    elif num % fizz == 0:
        print("Fizz")
    elif num % buzz == 0:
        print("Buzz")
    else:
        print(num)