def binary_search(key,arr):
   low,high=0,len(arr)-1
   if low<=high:
      mid=(low+high)//2
      if arr[mid]==key:
         return mid
      elif arr[mid]<key:
         low=mid +1
      else:
         high=mid -1
    return -1        


    