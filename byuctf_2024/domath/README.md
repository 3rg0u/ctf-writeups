### Challenge description

```markdown
We need to... do math... as cybersecurity people?
```

### Analysis

- In this challenge, we're given 2 files, called `domath.py` and `hints.txt`, respectively.
- $p$ and $q$ are `2048`-bits prime, while the public exponent $e$ has the familiar value of `65537`.
- A list called `hints` contains all the values of `p, q, n, e, d`, where $d$ is inverse modular of $e$ in $Z_{\phi{(n)}}$.
- Each element in `hints` can be presented by the following formula:

  $$
  a * x \equiv h_{i} \mod{N}
  $$

  where all values of $h_i$ are given in [hints.txt](./hints.txt), and $x$ is a `1024`-bit prime.

### Approach

- Due to the size of $p$ and $q$ are the same, `2048`-bit, so $N$ become a `4096`-bit integer, extremely large to be factorized.
- Let's take a glance on this details in the for loop that generated `hints`'s elements.
  ```python
  hints = [p, q, e, n, d]
  for _ in range(len(hints)):
      hints[_] = (hints[_] * getPrime(1024)) % n
      if hints[_] == 0: hints[_] = (hints[_] - 1) % n
  ```
  Because `hints` also contains `n`, so the 4-th element of `hints` is basically the inverse modular of $-1$ in $Z_{N}$, or simply, equals to $N-1$.
- At this point, by recovering value of $N-1$, we also have $N$ in reached.
- Furthermore, $N$ is a `4096`-bit integer, so $p*x$ is not big enough to be _overflow_ in $Z_{N}$, so $p' \equiv p * x \mod{N}$ can be simplified as $p' = p * x$. Similarly, we have $q' = q * y$.
- Because $x$ and $y$ are prime numbers, so $gcd(N, x) = 1$ and $gcd(N, y) = 1$.
- We can recover $p$ and $q$ using $gcd$, that's $gcd(N, p') = p$ and $gcd(N, q') = q$.
- See my [solve script](./solve.py).

### Flag

```
byuctf{th3_g00d_m4th_1snt_th4t_h4rd}
```
