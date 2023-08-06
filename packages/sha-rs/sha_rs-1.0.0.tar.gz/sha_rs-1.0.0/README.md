# SHA-py

Using SHA-3 and Keccak cryptographic algorithms based on Rust crate [`sha3`](https://crates.io/crates/sha3)

For fun. To be improved

# Installation

```bash
pip install sha_rs
```

# Usage

```python
from sha_rs import sha3_224, sha3_256, sha3_384, sha3_512
from sha_rs import keccak_224, keccak_256, keccak_384, keccak_512


# Keccak
assert keccak_224(b"hello") == "45524ec454bcc7d4b8f74350c4a4e62809fcb49bc29df62e61b69fa4"
assert keccak_256(b"hello") == "1c8aff950685c2ed4bc3174f3472287b56d9517b9c948127319a09a7a36deac8"
assert keccak_384(b"hello") == "dcef6fb7908fd52ba26aaba75121526abbf1217f1c0a31024652d134d3e32fb4cd8e9c703b8f43e7277b59a5cd402175"
assert keccak_512(b"hello") == "52fa80662e64c128f8389c9ea6c73d4c02368004bf4463491900d11aaadca39d47de1b01361f207c512cfa79f0f92c3395c67ff7928e3f5ce3e3c852b392f976"

# Sha3
assert sha3_224(b"hello") == "b87f88c72702fff1748e58b87e9141a42c0dbedc29a78cb0d4a5cd81"
assert sha3_256(b"hello") == "3338be694f50c5f338814986cdf0686453a888b84f424d792af4b9202398f392"
assert sha3_384(b"hello") == "720aea11019ef06440fbf05d87aa24680a2153df3907b23631e7177ce620fa1330ff07c0fddee54699a4c3ee0ee9d887"
assert sha3_512(b"hello") == "75d527c368f2efe848ecf6b073a36767800805e9eef2b1857d5f984f036eb6df891d75f72d9b154518c1cd58835286d1da9a38deba3de98b5a53e5ed78a84976"
```

