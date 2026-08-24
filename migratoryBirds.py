def migratoryBirds(arr):
    count = [0] * 6

    for bird in arr:
        count[bird] += 1

    max_frequency = max(count)

    for bird in range(1, 6):
        if count[bird] == max_frequency:
            return bird
