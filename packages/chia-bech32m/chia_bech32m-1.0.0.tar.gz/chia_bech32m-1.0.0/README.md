# chia_bech32m for python

A BIP350 compatible Bech32m encoding/decoding library for chia.

## install

```bash
pip install chia-bech32m
```

## Use

### import

```python
from chia_bech32m import bech32m
```

### Example
```python
print(bech32m.encode("7382e99e0679b68b6e8211c48224c99fc941a5f035bd85f9f32c4a8f48d3bb29","xch"))
print(bech32m.encode("0x7382e99e0679b68b6e8211c48224c99fc941a5f035bd85f9f32c4a8f48d3bb29","xch"))
print(bech32m.encode("7382e99e0679b68b6e8211c48224c99fc941a5f035bd85f9f32c4a8f48d3bb29",""))
print(bech32m.encode("7382e99e0679b68b6e8211c48224c99fc941a5f035bd85f9f32c4a8f48d3bb29","nft"))
# xch1wwpwn8sx0xmgkm5zz8zgyfxfnly5rf0sxk7ct70n939g7jxnhv5smryxmv
# xch1wwpwn8sx0xmgkm5zz8zgyfxfnly5rf0sxk7ct70n939g7jxnhv5smryxmv
# xch1wwpwn8sx0xmgkm5zz8zgyfxfnly5rf0sxk7ct70n939g7jxnhv5smryxmv
# nft1wwpwn8sx0xmgkm5zz8zgyfxfnly5rf0sxk7ct70n939g7jxnhv5sam5p80
```

```python
print(bech32m.decode("xch1wwpwn8sx0xmgkm5zz8zgyfxfnly5rf0sxk7ct70n939g7jxnhv5smryxmv"))
# 7382e99e0679b68b6e8211c48224c99fc941a5f035bd85f9f32c4a8f48d3bb29
```

## Support
XCH: `xch1crwg0ryz5rf90a6xmmspza2jmhc437sllnen8m7nu2dlx7ugjs9qaxgyjw`

pawket: `hezuoshe.xch`