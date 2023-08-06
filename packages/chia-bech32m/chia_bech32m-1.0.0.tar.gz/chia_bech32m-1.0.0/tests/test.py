#! /usr/bin/env python3

from chia_bech32m import bech32m

print(bech32m.encode("7382e99e0679b68b6e8211c48224c99fc941a5f035bd85f9f32c4a8f48d3bb29","xch"))
print(bech32m.encode("0x7382e99e0679b68b6e8211c48224c99fc941a5f035bd85f9f32c4a8f48d3bb29","xch"))
print(bech32m.encode("7382e99e0679b68b6e8211c48224c99fc941a5f035bd85f9f32c4a8f48d3bb29",""))
print(bech32m.encode("7382e99e0679b68b6e8211c48224c99fc941a5f035bd85f9f32c4a8f48d3bb29","nft"))

print(bech32m.decode("xch1wwpwn8sx0xmgkm5zz8zgyfxfnly5rf0sxk7ct70n939g7jxnhv5smryxmv"))