import base64
from cryptography.fernet import Fernet


payload = b"gAAAAABkEnJ0d31HqHMzKifO1hDgIlMtDggKpCQEeLT_KaKuVjCW6ltgddjuFXT7vLF3txx-UtrEITi9DCsQkAVpL6KSFg2Yao5jPdfH4YLJ4V7xS3MxKXClofooazYQHIS4SvgZt1EmExf-0kmUlzGVdPI53v0KmwYr5Bf98aqpW9WWYab32DujMhlBcnp-eBMEm4jueLfVRkhglQ7KB7gyNVYKYRFalxKO3hfH1m4wv4C8iAJBoUsVqwgLITFtODrlQobcSQGHXrY3aOiH8ecj6jzYNkWbbg=="

key_str = "correctstaplecorrectstaplecorrec"
key_base64 = base64.b64encode(key_str.encode())
f = Fernet(key_base64)
plain = f.decrypt(payload)
exec(plain.decode())
# print(plain.decode())
