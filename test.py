from collections import deque

dq = deque(['b','a','c'])
print(dq)

# LRU
if 'a' in dq:
    dq.remove('a')

print(dq)

dq.appendleft('a')

print(dq)