def insertion_sort(arr):
    for i in range(1,len(arr)):
        key=arr[i]
        j=i-1
        while j>=0 and arr[j]>key:
            arr[j+1]=arr[j]
            j-=1
        arr[j+1]=key
    return arr
arr=[5,8,6,9,12,75]
print("Original Array:", arr)
sorted_arr=insertion_sort(arr)
print("Sorted array:", sorted_arr)