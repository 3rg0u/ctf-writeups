from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import requests
from base64 import b64decode, b64encode
import time

url = "https://cookiecutter.chal.cyberjousting.com"


p1 = b"a" * (AES.block_size - len(b"email="))
p2 = pad(b"admin", AES.block_size)


response = requests.post(url=f"{url}/login", data={"email": (p1 + p2).decode()})
admin = b64decode(response.cookies.get("cookie"))[16:32]


# feed oracle until 'r' becomes the beginning of plaintext-block
org_len = len(b64decode(response.cookies.get("cookie")))
p3 = 1
while True:
    r = requests.post(
        url=f"{url}/login", data={"email": (p1 + p2 + (p3 * b"a")).decode()}
    )
    p3 += 1
    if len(b64decode(r.cookies.get("cookie"))) != org_len:
        break
p3 = (p3 + 3) * b"a"  # p + 3 means 'user' to be the beginning


response = requests.post(url=f"{url}/login", data={"email": (p1 + p2 + p3).decode()})

cookie = b64decode(response.cookies.get("cookie"))
cookie = cookie[:-16] + admin


flag = requests.get(
    url=f"{url}/authenticate", cookies={"cookie": b64encode(cookie).decode()}
).text

print(flag)
