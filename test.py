from collections import deque

de = deque([], maxlen= 4)

de.appendleft(1)
de.appendleft(2)
de.appendleft(3)
de.appendleft(4)
de.appendleft(5)

print(de) # deque([5, 4, 3, 2], maxlen=4)

de.appendleft(6)

print(de) # deque([6, 5, 4, 3], maxlen=4)