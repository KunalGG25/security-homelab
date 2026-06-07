#!/usr/bin/env python3
"""
Project 9 — Phase 2A: Salted password storage with bcrypt and Argon2.
Demonstrates why salting defeats dictionary and rainbow table attacks.
"""

import bcrypt
import hashlib
import time
from argon2 import PasswordHasher

passwords = [
    "password", "123456", "12345678", "qwerty", "abc123",
    "monkey", "1234567", "letmein", "trustno1", "dragon",
]

print("=" * 70)
print("UNSALTED MD5 — what the attacker sees in a stolen dump")
print("=" * 70)
for p in passwords:
    h = hashlib.md5(p.encode()).hexdigest()
    print(f"  {p:<15} → {h}")

print("\nObservation: same password always produces the same hash.")
print("One rainbow table cracks every user who picked 'password'.\n")

print("=" * 70)
print("BCRYPT — salted, adaptive, slow by design")
print("=" * 70)
bcrypt_hashes = []
start = time.time()
for p in passwords:
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(p.encode(), salt)
    bcrypt_hashes.append((p, hashed))
elapsed = time.time() - start

for p, h in bcrypt_hashes[:3]:
    print(f"  {p:<15} → {h.decode()[:60]}...")
print(f"  ... (10 passwords hashed in {elapsed:.2f}s — ~{elapsed/10*1000:.0f}ms each)")
print("\nObservation: every hash is different even for the same password.")
print("The $2b$12$ prefix = bcrypt, cost factor 12.\n")

# Verify bcrypt works correctly
p_test, h_test = bcrypt_hashes[0]
assert bcrypt.checkpw(p_test.encode(), h_test), "Verification failed"
print(f"  Verification check: '{p_test}' matches its hash → PASS\n")

print("=" * 70)
print("ARGON2id — current gold standard (winner of Password Hashing Competition)")
print("=" * 70)
ph = PasswordHasher(time_cost=2, memory_cost=65536, parallelism=2)
argon2_hashes = []
start = time.time()
for p in passwords:
    hashed = ph.hash(p)
    argon2_hashes.append((p, hashed))
elapsed = time.time() - start

for p, h in argon2_hashes[:3]:
    print(f"  {p:<15} → {h[:60]}...")
print(f"  ... (10 passwords hashed in {elapsed:.2f}s — ~{elapsed/10*1000:.0f}ms each)")
print("\nObservation: $argon2id$ prefix. Uses 64 MB RAM per hash — ")
print("defeats GPU attacks because GPU VRAM limits parallelism.\n")

# Verify argon2 works correctly
p_test, h_test = argon2_hashes[0]
assert ph.verify(h_test, p_test), "Verification failed"
print(f"  Verification check: '{p_test}' matches its hash → PASS\n")

print("=" * 70)
print("ALGORITHM COMPARISON")
print("=" * 70)
print(f"{'Algorithm':<12} {'Salted':<8} {'Speed (attacker)':<22} {'Recommended'}")
print("-" * 65)
print(f"{'MD5':<12} {'No':<8} {'~50 billion H/s (GPU)':<22} {'Never — broken'}")
print(f"{'SHA-1':<12} {'No':<8} {'~46 billion H/s (GPU)':<22} {'Never — broken'}")
print(f"{'SHA-256':<12} {'No':<8} {'~10 billion H/s (GPU)':<22} {'No — use bcrypt'}")
print(f"{'bcrypt':<12} {'Yes':<8} {'~10,000 H/s (GPU)':<22} {'Yes — passwords'}")
print(f"{'Argon2id':<12} {'Yes':<8} {'~1,000 H/s (GPU)':<22} {'Yes — gold standard'}")

print("\nSalting means each password hash is unique.")
print("A rainbow table pre-computed for 'password' → MD5 is useless against bcrypt.")
print("The attacker must crack each hash individually, at ~10k attempts/sec instead of 50B.")
print("\nSave these hashes to hashes_bcrypt.txt and try hashcat — it will fail.")

# Save bcrypt hashes for Hashcat attempt
with open("hashes_bcrypt.txt", "w") as f:
    for _, h in bcrypt_hashes:
        f.write(h.decode() + "\n")
print("\nWrote hashes_bcrypt.txt — run: hashcat -m 3200 -a 0 hashes_bcrypt.txt rockyou.txt")
print("Watch the speed drop from 50,000,000 H/s → ~1,000 H/s")
