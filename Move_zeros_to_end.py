a = list(map(int, input("Enter elements: ").split()))

non_zero = []

for x in a:
    if x != 0:
        non_zero.append(x)

zeros = len(a) - len(non_zero)

result = non_zero + [0] * zeros

print("Array after moving zeros:", result)
