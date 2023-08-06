import logging

def heap_sort(arr):
    try:
        n = len(arr)
        for i in range(n//2 - 1, -1, -1):
            heapify(arr, n, i)
        for i in range(n-1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]
            heapify(arr, i, 0)
        return arr
    except Exception as e:
        logging.exception("An error occurred during heap sort: %s", e)
        return "An error occurred during heap sort: {}".format(str(e))


def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and arr[l] > arr[largest]:
        largest = l
    if r < n and arr[r] > arr[largest]:
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)
