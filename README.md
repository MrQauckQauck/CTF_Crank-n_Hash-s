# CTF_Crank-n_Hash-s

Created this Python script, so i could crack md5 hash faster while playing CFT 

## Overview
This is an MD5 password cracker that uses brute-force to crack multiple MD5-crypt hashes with a known prefix. The script attempts to find passwords that match given MD5-crypt hashes by trying different combinations with the prefix `SKY-MASK-`.

## Requirements
```bash
pip install passlib
```

## Script Walkthrough

### Step-by-Step Breakdown

#### 1. Imports
```python
from passlib.hash import md5_crypt
import itertools, string
```
- `passlib.hash.md5_crypt`: Library for MD5-crypt hashing/verification
- `itertools, string`: For generating combinations and character sets

#### 2. Target Hashes
```python
hashes = {
    "$1$MASK$x7IpStDuIMkWd.F9saA5V.",
    "$1$MASK$j/DmhKHa2pgk8FIWIi7YP1",
    "$1$MASK$5kIdQId6kYCM5z2KEtWgQ1",
    "$1$MASK$kGxVYUG7k95Hxbr6xkjdy/"
}
```
- Defines a set of 4 MD5-crypt hashes to crack
- Format: `$1$MASK$...` (MD5-crypt format with salt "MASK")

#### 3. Known Prefix
```python
prefix = "SKY-MASK-"
```
- All passwords start with this prefix
- The script only needs to crack the 4-character suffix

#### 4. Character Sets
```python
charsets = [
    ("digits", string.digits),
    ("lower", string.ascii_lowercase),
    ("upper", string.ascii_uppercase),
    ("alnum", string.digits + string.ascii_lowercase + string.ascii_uppercase),
]
```
Tries 4 different charsets in order:
- **digits**: 0-9 (10 chars)
- **lower**: a-z (26 chars)
- **upper**: A-Z (26 chars)
- **alnum**: all alphanumeric (62 chars)

This prioritization tries simpler charsets first for efficiency.

#### 5. Configuration
```python
length = 4  # the suffix length per puzzle
found = {}
```
- `length = 4`: Suffix is 4 characters long
- `found = {}`: Dictionary to store cracked passwords

#### 6. Main Cracking Loop
```python
for name, charset in charsets:
    print(f"Trying charset: {name} (size {len(charset)})")
    for combo in itertools.product(charset, repeat=length):
        suffix = ''.join(combo)
        candidate = prefix + suffix
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
```
- **Outer loop**: Iterates through each charset
- **Inner loop**: Generates all possible 4-character combinations using `itertools.product`
- **For each candidate**:
  - Constructs full password: `prefix + suffix` (e.g., "SKY-MASK-0000")
  - Tests against each uncracked hash using `md5_crypt.verify()`
  - If match found, stores it and prints result
  - Stops early if all hashes are cracked

#### 7. Results Display
```python
print("\nResults:")
for h in hashes:
    if h in found:
        print(h, "=>", found[h])
    else:
        print(h, "=> NOT FOUND (try other charsets/lengths)")
```
- Prints final summary
- Shows which passwords were found for each hash
- Indicates if any hashes remain uncracked

## How It Works

The script performs a **brute-force attack** by:
1. Knowing the password format: `SKY-MASK-XXXX`
2. Systematically trying every possible 4-character suffix
3. Starting with smaller charsets (numeric only) before trying larger ones
4. Verifying each candidate against the MD5-crypt hashes
5. Stopping when all passwords are found

## Efficiency Strategy

Rather than immediately trying all 62 alphanumeric characters (62^4 = 14.7M combinations), it tries:
- **Digits only**: 10^4 = 10,000 combinations
- **Lowercase only**: 26^4 = 456,976 combinations  
- **Uppercase only**: 26^4 = 456,976 combinations
- **All alphanumeric**: 62^4 = 14,776,336 combinations (only if needed)

This approach is much faster if the passwords use simpler character sets.

## Usage
```bash
python3 Crack_md5.py
```

The script will output progress as it tries different charsets and display found passwords immediately when discovered.
