### Challenge description

```markdown
Found these keys... wonder what they do...
```

### Analysis

We're given a file called `cne.txt`, which contains 3 variables, `c`, `n` and `e`.  
The first idea in my mind is trying to factor `n`, using this [site](https://www.alpertron.com.ar/ECM.HTM). And fortunately, the given `n` is a _prime number_, so the rest tasks is like a "piece of cake".

![](https://i.ibb.co/fBgtm9h/01.png)

Using RSA's decryption formula:

$$
d \equiv e^{-1} \mod{(n-1)}
$$

due to the fact that $n$ is a prime number, so $\phi{(n)}=n-1$.

$$
m \equiv c^{d} \mod{n}
$$

### Flag

```
byuctf{d1d_s0m3_rs4_stuff...m1ght_d3l3t3_l4t3r}
```
