weights = [10,20,30]
values = [60,100,120]
capacity = 50

items = list(zip(values, weights))

items.sort(key=lambda x: x[0]/x[1], reverse=True)

total_value = 0

for value, weight in items:
    if capacity >= weight:
        total_value += value
        capacity -= weight
    else:
        total_value += value * (capacity/weight)
        break

print("Maximum Value =", total_value)
