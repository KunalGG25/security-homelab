#!/usr/bin/env python3
"""
Project 9 — Phase 1A: Generate unsalted MD5 and SHA-1 hash lists.
Simulates a stolen database dump with no password protection (no salt).
"""

import hashlib
import csv

passwords = [
    "password", "123456", "12345678", "qwerty", "abc123",
    "monkey", "1234567", "letmein", "trustno1", "dragon",
    "baseball", "iloveyou", "master", "sunshine", "ashley",
    "bailey", "passw0rd", "shadow", "123123", "654321",
]

md5_rows = []
sha1_rows = []

for p in passwords:
    md5_hash  = hashlib.md5(p.encode()).hexdigest()
    sha1_hash = hashlib.sha1(p.encode()).hexdigest()
    md5_rows.append((p, md5_hash))
    sha1_rows.append((p, sha1_hash))

# Save CSVs (simulated stolen DB dump)
with open("hashes_md5.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["plaintext", "md5_hash"])
    writer.writerows(md5_rows)

with open("hashes_sha1.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["plaintext", "sha1_hash"])
    writer.writerows(sha1_rows)

# Plain hash lists for Hashcat (one hash per line)
with open("hashes_md5.txt", "w") as f:
    f.writelines(h + "\n" for _, h in md5_rows)

with open("hashes_sha1.txt", "w") as f:
    f.writelines(h + "\n" for _, h in sha1_rows)

print(f"Generated {len(passwords)} password hashes\n")
print(f"{'Password':<15} {'MD5 (32 chars)':<35} {'SHA-1 (40 chars)'}")
print("-" * 90)
for p, md5 in md5_rows:
    sha1 = dict(sha1_rows)[p]
    print(f"{p:<15} {md5:<35} {sha1}")

print("\nFiles written:")
print("  hashes_md5.csv / hashes_sha1.csv  — full dump with plaintexts")
print("  hashes_md5.txt / hashes_sha1.txt  — hash-only lists for Hashcat")
