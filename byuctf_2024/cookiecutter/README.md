### Challenge description

```markdown
I know there are a bunch of vulnerabilities with JWT, so I wanted to use a different implementation to not leave my site vulnerable. This is my best shot.

https://cookiecutter.chal.cyberjousting.com
```

### Analysis

- We're given the source code of server, called `server.py`.
- Seems like it uses `AES.ECB_MODE` to encrypt and decrypt data.
- The `Profile` class return a format string.

```python
def __str__(self):
    return f"email={self.email}&uid={self.uid}&role={self.role}"
```

where `role` is set to a fixed value `"user"`.

- The `email` attribute is preprocessed before assign.

```python
self.email = email.replace('&','').replace('=','')
```

- The `get_user_input()` function encrypt our `Profile` information and return as a cookie.

```python
def profile_for(input : str):
    return Profile(input)

def get_user_input(inp : str, oracle : ECBOracle):
    prof = profile_for(inp)
    userinfo = oracle.encrypt(str(prof).encode())
    return userinfo
```

- Our mission is create an `admin` profile to access `flag.html` page.

```python
def auth():
    cookie = request.cookies.get('cookie')
    user_info = decrypt_user_input(cookie.encode(), oracle)
    print(user_info)
    if user_info.role == 'admin':
        response = make_response(render_template('flag.html'))
        response.set_cookie('cookie', cookie)
        return response
    else:
        response = make_response(render_template('failed_home.html'))
        response.set_cookie('cookie', cookie)
        print("failed auth")
        return response
```

### Approach

- Cuz the server side used `AES.ECB_MODE` with block-size of 16-byte, and the characteristic of `ECB_MODE` is that under the same key, plaintext-block always been encrypted into an identical cipher-block.
- According to the format of plaintext we're given, it's ending up with `user` string.
- So, we can easily exploit the flaw of `ECB_MODE` to make a fake `admin` profile by feeding the email until `user` is the beginning of final plaintext block.
- My idea is illustrated by the following picture:

![](https://i.ibb.co/VkXxWwy/02.png)

- As you can see, padded `admin` block will be returned as the second block in ciphertext.
- However, the static variable `uid` can be varied, instead of being fixed with `1` so we need to solve an extra problem to reach the flag.
- The solution is feed server's oracle until its return-ciphertext changed the size. At this point, we know `r` in `user` is the beginning of the last plaintext block. Feed `3` more bytes to make `user` become the beginning of plaintext block.
- Finally, simply cut out the `admin` cipher-block and use it to replace `user` cipher-block, we're now having a ciphertext of `admin` role.

- See my [solve script](./solve.py).

### Flag

```
byuctf{d0nt_cut_1t_l1k3_th4t!!}
```
