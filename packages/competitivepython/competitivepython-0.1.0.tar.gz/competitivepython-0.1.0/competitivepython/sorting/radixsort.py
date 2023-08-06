import logging

def radix_sort(arr):
    try:
        max_val = max(arr)
        num_digits = len(str(max_val))
        for k in range(num_digits):
            s = [[] for i in range(10)]
            for i in arr:
                s[i // (10**k) % 10].append(i)
            arr = [j for sub in s for j in sub]
        return arr
    except Exception as e:
        logging.exception("An error occurred during radix sort: %s", e)
        return "An error occurred during radix sort: {}".format(str(e))

