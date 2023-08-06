# pb-amarder
This is a progress bar for iterators that lets you specify a callback.

## Installation
To install in python3:
`pip install pb-amarder`

## Usage
```python
from pb_amarder import Progress
primes = []
pb = Progress(total=1000000, message='Message to print', increment=10, callback=lambda: 'Prime numbers found: {:,d}'.format(len(primes)))
for n in pb.iterator(range(1000000)):
    if is_prime(n):
        primes.append(n)
```
