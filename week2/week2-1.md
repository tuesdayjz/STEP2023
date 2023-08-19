### week2-1: hash table

#### run

- `$ python3 hash_table.py`

- main function calls `functional_test()` and `performance_test()`

#### ideas

**delete(key)**

- calculate the index of the item
- for each item in the bucket
  - if the key matches the key of the item
    - if the item is not the first item in the bucket
      - connect the previous item to the next item
    - else (if the item is the first item in the bucket)
      - set the next item as the first item in the bucket
    - decrement the count of items in the bucket
    - return True
  - else (if the key does not match the key of the item)
    - move to the next item in the bucket
  - return False

<br>

**rehash**

- make new buckets
- for each item in the old buckets
  - calculate the index of the item in the new buckets
  - add the item to the new buckets
- set the new buckets as the buckets of the hash table

<br>

**hash function**

- compaired 3 different hash functions

```python
def hash0(key):
    assert type(key) == str
    hash = 0
    for i in key:
        hash += ord(i)
    return hash
```

```python
def hash1(key):
    assert type(key) == str
    hash = 0
    for i in key:
      hash *= 10
        hash += ord(i)
    return hash
```

```python
def hash2(key):
    assert type(key) == str
    hash = 0
    for i in key:
        hash <<= 1
        hash += ord(i)
    return hash
```

<br>

![image](https://user-images.githubusercontent.com/82920808/239954025-d565d2c4-a566-4e35-873f-73b1cde69c62.png)

- I think that the reduced performance of all hash functions at the same point is due to a particularly high number of re-hashes (hash numbers collide)

---

**messy notes**

- at first I tried 3 different hash functions
  - $hash0 = \sum_{i=0}^{len(key)-1} ord(i)$
  - $hash1 = \sum_{i=0}^{len(key)-1} ord(i) \times (i+1)$
  - $hash2 = \sum_{i=0}^{len(key)-1} ord(i)$ << $i$
    - that means $hash2 = \sum_{i=0}^{len(key)-1} ord(i) \times 2^i$

<br>

- **without rehashing**

| function | 0        | 1        | 2        | 3        | 4        | 5        | 6        | 7        | 8        | 9        | 10       |
| -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- |
| hash0    | 0.141675 | 0.264194 | 0.458196 | 0.894663 | 1.583601 | 2.386393 | 3.192551 | 3.905212 | 4.996136 | 6.936427 | 7.515041 |
| hash1    | 0.103742 | 0.197821 | 0.370617 | 0.654073 | 0.926428 | 1.295166 | 1.637758 | 1.912461 | 2.206000 | 2.596715 | 2.835486 |
| hash2    | 0.087641 | 0.164476 | 0.300828 | 0.494401 | 0.796167 | 1.115073 | 1.414891 | 1.683746 | 2.196558 | 2.475865 | 2.564640 |

- hash2 is a little bit faster than hash1
  - is it simply because bit shifting is faster than multiplication ... ?

<br>

- **with rehashing**

| function | 0        | 1        | 2        | 3        | 4        | 5        | 6        | 7        | 8        | 9        | 10       |
| -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- |
| hash0    | 0.138501 | 0.335138 | 0.364132 | 0.759933 | 0.771389 | 1.313483 | 2.903889 | 1.599014 | 2.188509 | 2.672673 | 3.321305 |
| hash1    | 0.076618 | 0.124491 | 0.115954 | 0.253815 | 0.201688 | 0.303220 | 0.753027 | 0.401658 | 0.500669 | 0.620192 | 0.741426 |
| hash2    | 0.060210 | 0.069839 | 0.055781 | 0.130432 | 0.067772 | 0.079858 | 0.271970 | 0.097294 | 0.105789 | 0.134958 | 0.123959 |

- with rehashing, it turns out that hash2 is much faster than hash1
  - it means that shifting can distribute the items more evenly than multiplication
  - it may be because shifting is an exponential function, while multiplication is a linear function
  - then if we make it a quadratic function, is it better than hash1 and worse than hash2?
  - what about cubic function, quartic function, etc.?

<br>

- the quadratic function was found to perform as well as the hash2 function.
- the performance of the functions gets better and better as the dimension increases.
- after 5th-8th order functions, the performance drops off.
  - would there be an overflow? or multiplying by a large number takes time?
- the further apart the numbers multiplied by ord(i) and ord(i+1) are, the better the distribution is likely to be ...
- then how about $\sum_{i=0}^{len(key)-1} ord(i)$ << $(i\times 2)$ ?
- I attached an image that shows the performance of the functions.

![image](https://user-images.githubusercontent.com/82920808/239747945-bfe81038-de09-423b-8959-36acf32a1ba3.png)

- graph with logarithmic axis

![image](https://user-images.githubusercontent.com/82920808/239747957-de82e052-fd7d-4d6f-bb4a-335084d63703.png)
