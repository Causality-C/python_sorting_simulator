'''
Sorting algorithm generators

Currently Supports
- Bubble Sort
- Merge Sort
- Insertion Sort

'''

def bubble_sort_iteration(lst : list) -> None:
    # Swap Variable: If swap then keep running algorithm
    swap = True
    length = len(lst)

    while swap:
        swap = False # there has been no swaps yet
        # Iterate through list
        for i in range(length - 1):
            cur, next = lst[i], lst[i+1]
            if cur > next:
                swap = True
                lst[i+1] = cur
                lst[i] = next
                yield
            else:
                yield

def merge_sort_iteration(lst: list) -> None:
    # Function to merge the array
    def merge(lst: list, start: int, mid: int, end: int) -> None:
        merged = []
        leftIdx = start
        rightIdx = mid + 1
    
        while leftIdx <= mid and rightIdx <= end:
            if lst[leftIdx] < lst[rightIdx]:
                merged.append(lst[leftIdx])
                leftIdx += 1
            else:
                merged.append(lst[rightIdx])
                rightIdx += 1
    
        while leftIdx <= mid:
            merged.append(lst[leftIdx])
            leftIdx += 1
    
        while rightIdx <= end:
            merged.append(lst[rightIdx])
            rightIdx += 1
    
        for i in range(len(merged)):
            lst[start + i] = merged[i]
            yield lst

    def merge_sort(lst: list, start: int, end: int):
        if end <= start:
            return
        
        mid = start + ((end - start + 1) // 2 ) -1
        yield from merge_sort(lst, start, mid)
        yield from merge_sort(lst, mid + 1, end)
        yield from merge(lst, start, mid, end)
    
    yield from merge_sort(lst, 0, len(lst) - 1)

def insertion_sort_iteration(lst: list):
    length = len(lst)
    for i in range(length): 
        key = lst[i]
        j = i - 1

        while j >= 0 and key < lst[j] :
            lst[j + 1] = lst[j]
            j -= 1
            yield
        lst[j + 1] = key 
        yield
    return

