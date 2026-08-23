a = list(map(int, input("Enter elements: ").split()))

maximum = a[0]
minimum = a[0]

for x in a:
    if x > maximum:
        maximum = x

    if x < minimum:
        minimum = x

print("Maximum =", maximum)
print("Minimum =", minimum)
