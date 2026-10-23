import json

matrix = json.loads(input()) # Input: ["10100","10111","11111","10010"]
if not matrix or not matrix[0]:
    print(0)
    exit()

rows, cols = len(matrix), len(matrix[0])
dp = [[0] * cols for _ in range(rows)]
max_side = 0

for i in range(rows):
    for j in range(cols):
        if matrix[i][j] == '1':
            if i == 0 or j == 0: # first row or col
                dp[i][j] = 1
            else:
                dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
            max_side = max(max_side, dp[i][j])

print(max_side * max_side) # area = side * side
