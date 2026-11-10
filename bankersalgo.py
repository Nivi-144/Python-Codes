
allocation = [
    [0, 1, 0],
    [2, 0, 0],
    [3, 0, 2],
    [2, 1, 1],
    [0, 0, 2]
]

maximum = [
    [7, 5, 3],
    [3, 2, 2],
    [9, 0, 2],
    [2, 2, 2],
    [4, 3, 3]
]

available = [3, 3, 2]

n = len(allocation)
m = len(available)

need = []

for i in range(n):
    row = []
    for j in range(m):
        row.append(maximum[i][j] - allocation[i][j])
    need.append(row)

print("Need Matrix:")
for row in need:
    print(row)

work = available.copy()
finish = [False] * n
safe_sequence = []

while len(safe_sequence) < n:
    found = False

    for i in range(n):
        if not finish[i]:
            if all(need[i][j] <= work[j] for j in range(m)):
                for j in range(m):
                    work[j] += allocation[i][j]

                finish[i] = True
                safe_sequence.append(i)
                found = True

    if not found:
        break

if all(finish):
    print("System is in SAFE state")
    print("Safe Sequence:", safe_sequence)
else:
    print("System is NOT in SAFE state")
