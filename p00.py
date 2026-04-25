rows = 10
for i in range(rows):
    print(" " * (rows - i), end="")
    print("*" * (2 * i + 1), end="")
    print(" " * (rows - i), end="")
    print("*" * (2 * i + 1))
for i in range(rows, 0, -1):
    print(" " * (rows - i + 1), end="")
    print("*" * (2 * i - 1))
