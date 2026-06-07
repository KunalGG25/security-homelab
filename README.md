# Kunal's Cybersecurity Homelab Portfolio

> SOC Analyst in progress · CompTIA Security+ SY0-701 (in progress)
> Homelab: Proxmox · TrueNAS · pfSense · Wazuh (planned)

Hands-on security projects covering offensive techniques, defensive detection, malware analysis, and Active Directory attacks. Every project runs in a real homelab — not a course VM. Results are real.

---

## Projects

| # | Project | Category | Status |
|---|---|---|---|
| 09 | [Rainbow Table Attack & Defense Lab](#project-09--rainbow-table-attack--defense-lab) | Cryptography | ✅ Complete |
| 15 | [Malware Static Analysis & SOC Triage](#project-15--malware-static-analysis--soc-triage) | Reverse Engineering | 🔜 Next |
| 16 | [Dynamic Malware Analysis — REMnux + Ghidra](#project-16--dynamic-malware-analysis--remnux--ghidra) | Reverse Engineering | ⬜ Planned |
| 17 | [Active Directory Home Lab Build](#project-17--active-directory-home-lab-build) | Active Directory | ⬜ Planned |
| 18 | [AD Attack Chain — BloodHound → Kerberoasting → PTH](#project-18--ad-attack-chain) | Active Directory | ⬜ Planned |
| 19 | [AD Detection & Hardening](#project-19--ad-detection--hardening) | Active Directory | ⬜ Planned |

---

## Project 09 — Rainbow Table Attack & Defense Lab

**Skills:** Python · Hashcat · Cryptography · Password Security  
**Tools:** Python 3.10 · Hashcat v6.2.5 · RTX 3050 (OpenCL) · bcrypt · Argon2id

### What I built

Both sides of a password cracking attack:

1. **Attack** — Generated 20 unsalted MD5/SHA-1 hashes (simulating a stolen database), then cracked them with Hashcat and rockyou.txt
2. **Defense** — Rewrote password storage using bcrypt and Argon2id, then re-ran Hashcat to prove the attack collapses

### Results

| Hash | Cracked | Speed | Time | GPU util |
|---|---|---|---|---|
| MD5 (unsalted) | **20/20 (100%)** | 50,414,100 H/s | < 1 second | 5% |
| SHA-1 (unsalted) | **20/20 (100%)** | 46,171,100 H/s | < 1 second | 5% |
| bcrypt cost 12 (salted) | 5/10 in 30s | **142 H/s** | est. 5+ days | **100%** |

**354,000× speed reduction** just by switching to bcrypt. Same GPU, same passwords, same wordlist.

### Key finding

Without a salt, `password` always hashes to `5f4dcc3b5aa765d61d8327deb882cf99` (MD5) — on every machine, forever. A rainbow table makes cracking a lookup, not a computation. Salting destroys this: every hash is unique, every crack is independent, bcrypt forces serial computation that GPUs cannot parallelise.

### Files
- [`scripts/generate_hashes.py`](Project-09-Rainbow-Table-Lab/scripts/generate_hashes.py) — unsalted MD5/SHA-1 hash generator
- [`scripts/salted_defense.py`](Project-09-Rainbow-Table-Lab/scripts/salted_defense.py) — bcrypt + Argon2id implementation with comparison table
- [`evidence/cracked_md5.txt`](Project-09-Rainbow-Table-Lab/evidence/cracked_md5.txt) — Hashcat output: all 20 hashes cracked

---

## Project 15 — Malware Static Analysis & SOC Triage

**Status:** 🔜 Coming soon  
**Skills:** IOC extraction · PE analysis · YARA rules · Analyst reporting  
**Tools:** strings · FLOSS · PE-bear · VirusTotal · YARA

Static analysis of real malware samples from MalwareBazaar — without executing a single file. Extract hashes, strings, PE imports, and network IOCs. Write YARA detection rules. Produce analyst reports with MITRE ATT&CK mapping.

---

## Project 16 — Dynamic Malware Analysis — REMnux + Ghidra

**Status:** ⬜ Planned (requires REMnux VM on Proxmox)  
**Skills:** Behavioural analysis · Network traffic analysis · Reverse engineering  
**Tools:** REMnux · FakeNet-NG · Wireshark · Ghidra

Execute malware in an isolated VM, intercept C2 traffic with FakeNet-NG, disassemble the binary in Ghidra to identify the C2 communication function.

---

## Project 17 — Active Directory Home Lab Build

**Status:** ⬜ Planned (requires Windows Server eval ISO)  
**Skills:** AD DS · Identity management · Windows Server administration  
**Tools:** Windows Server 2022 · Proxmox · PowerShell · Active Directory

Deploy a `corp.local` domain with Windows Server 2022 DC, Windows 10 client, realistic OU structure, and intentional misconfigurations for attack projects.

---

## Project 18 — AD Attack Chain

**Status:** ⬜ Planned (requires Project 17)  
**Skills:** Offensive security · Credential attacks · Lateral movement  
**Tools:** BloodHound · SharpHound · Impacket · Hashcat · CrackMapExec

Full attack chain: BloodHound enumeration → Kerberoasting → offline hash cracking → Pass-the-Hash lateral movement → Domain Admin. Every stage documented with MITRE ATT&CK mapping.

---

## Project 19 — AD Detection & Hardening

**Status:** ⬜ Planned (requires Projects 17, 18, and Wazuh)  
**Skills:** Detection engineering · SIEM · AD hardening · Incident response  
**Tools:** Wazuh · Windows Event Forwarding · Sysmon · Group Policy

Write Wazuh detection rules for every stage of the Project 18 attack chain. Harden the AD environment. Produce a full incident response report treating the attack as a real breach.

---

## Skills

| Skill | Projects |
|---|---|
| Cryptography & password security | 09 |
| Malware analysis & IOC extraction | 15, 16 |
| Active Directory attacks | 17, 18 |
| Detection engineering & SIEM | 19 |
| Python scripting | 09, 15 |
| Offensive tools (Hashcat, BloodHound, Impacket) | 09, 18 |
| Incident response | 19 |

---

## Homelab

```
MSI Cubi 3 Silent  →  Proxmox VE (hypervisor)
                       ├── pfSense VM      (firewall/router)
                       ├── Windows Server  (AD DC — planned)
                       ├── Windows 10 VM   (domain client — planned)
                       ├── Kali Linux VM   (attacker — planned)
                       ├── REMnux VM       (malware analysis — planned)
                       └── Wazuh VM        (SIEM — planned)

TrueNAS SCALE      →  NAS, storage, VM backups
Acer Nitro 5       →  Admin workstation (Pop!_OS, RTX 3050)
```

---

## Certifications

- ✅ ISC2 Certified in Cybersecurity (CC)
- 🔄 CompTIA Security+ SY0-701 — in progress

---

*All projects run in a self-built homelab. No cloud sandboxes, no course VMs.*
