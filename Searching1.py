def linear_search(key,arr):
    for i in range(len(arr)):
        if arr[i]==key:
            return i
    return -1    

    