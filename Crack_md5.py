#!/usr/bin/env python3
# crack_mask_fixed_passlib.py
# Requires: pip install passlib

from passlib.hash import md5_crypt
import itertools, string

hashes = {
    "$1$MASK$x7IpStDuIMkWd.F9saA5V.",
    "$1$MASK$j/DmhKHa2pgk8FIWIi7YP1",
    "$1$MASK$5kIdQId6kYCM5z2KEtWgQ1",
    "$1$MASK$kGxVYUG7k95Hxbr6xkjdy/"
}

# the prefix from the puzzle
prefix = "SKY-MASK-"

# Charsets to try (adjust order/contents as needed).
# The script will try numeric, lowercase, uppercase, then alnum.
charsets = [
    ("digits", string.digits),
    ("lower", string.ascii_lowercase),
    ("upper", string.ascii_uppercase),
    ("alnum", string.digits + string.ascii_lowercase + string.ascii_uppercase),
]

length = 4  # the suffix length per puzzle
found = {}

for name, charset in charsets:
    print(f"Trying charset: {name} (size {len(charset)})")
    for combo in itertools.product(charset, repeat=length):
        suffix = ''.join(combo)
        candidate = prefix + suffix
        # verify candidate against each remaining hash
        for h in list(hashes):
            if h in found:
                continue
            if md5_crypt.verify(candidate, h):
                found[h] = candidate
                print("FOUND:", h, "->", candidate)
        if len(found) == len(hashes):
            break
    if len(found) == len(hashes):
        break

print("\nResults:")
for h in hashes:
    if h in found:
        print(h, "=>", found[h])
    else:
        print(h, "=> NOT FOUND (try other charsets/lengths)")

