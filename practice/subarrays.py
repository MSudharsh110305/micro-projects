def generate_all_subarrays(arr):
    subarrays = []
    n = len(arr)
    
    for i in range(n):
        for j in range(i, n):
            subarrays.append(arr[i:j+1])
    
    return subarrays

arr = [1, 2, 3]
result = generate_all_subarrays(arr)
print("Generated subarrays:", result)
