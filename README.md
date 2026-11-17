# APKBully

**APKBully** is a fast, automated Android APK decompiler and secret scanning tool. It decompiles APKs using **JADX** and scans the extracted source code and resources for exposed credentials, API tokens, and other secrets using **BetterLeaks**.

<p align="left">
  <img src="https://github.com/user-attachments/assets/ded0bf66-d7ca-45bb-899f-17fdd1cad995" alt="APKBully scanning interface" width="800">
</p>

---

## Features

- **Automated Tool Setup (`setup`)**
- **Full APK Scan (`scan`)**
- **Direct Directory Scan (`direct-scan`)**    
- **Structured Findings and JSON Output**
  
### Can a Local LLM Make Secret Detection Better?

What if we combined BetterLeaks with a locally hosted LLM to reduce false positives? I experimented with this idea using Liquid AI's `d1-omni:600m`. The results were... interesting.

**[Read the research →](research/research.md)**

