# Project 09 — Rainbow Table Attack & Password Defense Lab

> **Status:** ✅ Complete (Phase 2B — SIEM rule pending Wazuh deployment)  
> **Date:** 2026-05-28  
> **Tools:** Python 3.10 · Hashcat v6.2.5 · RTX 3050 Laptop GPU (OpenCL) · bcrypt · Argon2id  
> **Skills:** Cryptography · Password Security · Python · Offensive Tooling · Security Hardening

---

## What This Project Proves

MD5 and SHA-1 are not password hashing algorithms — they are checksum algorithms repurposed for passwords, catastrophically. This project demonstrates the attack in full, then proves exactly why modern algorithms (bcrypt, Argon2id) defeat it.

---

## The Attack — Unsalted Hashes

Without a salt, identical passwords always produce identical hashes:

```
"password"  →  5f4dcc3b5aa765d61d8327deb882cf99  (MD5, every time, forever)
```

A pre-computed rainbow table turns cracking into a lookup — not a computation. An attacker with a stolen MD5 database doesn't crack anything. They just search a table.

**Phase 1A** — Generated 20 unsalted MD5 and SHA-1 hashes (`generate_hashes.py`)  
**Phase 1B** — Ran Hashcat with rockyou.txt (14.3M passwords)

### Results

| Hash | Recovered | Speed | Time | GPU utilisation |
|---|---|---|---|---|
| MD5 | **20 / 20 (100%)** | 50,414,100 H/s | **< 1 second** | 5% |
| SHA-1 | **20 / 20 (100%)** | 46,171,100 H/s | **< 1 second** | 5% |

The GPU was at **5% utilisation**. It only needed 3.66% of rockyou.txt before all 20 were cracked. At 50 million attempts per second, the full 14M-word list takes under 5 minutes.

---

## The Defense — Salted Hashing

**Phase 2A** — Rewrote storage with bcrypt (cost 12) and Argon2id (`salted_defense.py`)

Salting adds a random value to each password before hashing:
- `"password" + random_salt` → unique hash every time
- The rainbow table is now worthless — every user's hash is different
- Each hash must be cracked independently — no shortcuts

bcrypt and Argon2 add deliberate slowness via cost factors and memory requirements:

```
bcrypt gensalt → $2b$12$...   (cost 12 = ~212ms per hash on this hardware)
Argon2id       → $argon2id$v=19$m=65536... (64MB RAM per attempt)
```

### Results — same GPU, same wordlist, same passwords

| Hash | Speed | GPU utilisation | Time to crack 10 common passwords |
|---|---|---|---|
| MD5 (unsalted) | 50,414,100 H/s | 5% | < 1 second |
| bcrypt cost 12 | **142 H/s** | **100%** | **5 days, 20 hours** |

**354,000× speed reduction.** The GPU ran at 100% for 30 seconds and estimated 5+ days — for passwords like `123456`. The serial computation bcrypt requires cannot be parallelised across GPU cores the way MD5 can.

---

## Algorithm Comparison

| Algorithm | Salted | Attacker speed (GPU) | Verdict |
|---|---|---|---|
| MD5 | ❌ | ~50 billion H/s | Never — broken |
| SHA-1 | ❌ | ~46 billion H/s | Never — broken |
| SHA-256 | ❌ | ~10 billion H/s | No — use bcrypt |
| bcrypt | ✅ | ~10,000 H/s | Yes — passwords |
| Argon2id | ✅ | ~1,000 H/s | Gold standard |

---

## Files

| File | Description |
|---|---|
| `scripts/generate_hashes.py` | Generates 20 unsalted MD5 + SHA-1 hashes, saves CSV and Hashcat-ready txt |
| `scripts/salted_defense.py` | bcrypt + Argon2id implementation, comparison table, writes bcrypt hashes for Hashcat test |
| `evidence/cracked_md5.txt` | Hashcat output — all 20 MD5 hashes cracked with plaintext revealed |

---

## MITRE ATT&CK

| Technique | ID | Relevance |
|---|---|---|
| Brute Force: Password Cracking | T1110.002 | Hashcat dictionary attack against stolen hashes |
| Credentials from Password Stores | T1555 | Simulated stolen database dump scenario |

---

## Resume Bullet

> "Demonstrated dictionary attack against unsalted MD5/SHA-1 password hashes using Hashcat (RTX 3050, 50M H/s, 100% recovery in <1s); hardened storage with bcrypt/Argon2id, reducing attack throughput 354,000× and proving pre-computation attacks fail against salted hashes."
