<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/banner-light.svg">
  <img alt="OpenSec. From vulnerability to visibility. AI-native vulnerability management." src="assets/banner-dark.svg" width="100%">
</picture>

<p align="center">
  <a href="https://opensec.in"><img alt="opensec.in" src="https://img.shields.io/badge/opensec.in-050505?style=for-the-badge&logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMDAgMTAwIj48ZyBmaWxsPSIjYmFmYzZiIj48cGF0aCBkPSJNNTEuNSA4LjAyNyBBNDIgNDIgMCAwIDEgOTEuOTczIDQ4LjUgTDc1Ljk1NyA0OC41IEEyNiAyNiAwIDAgMCA1MS41IDI0LjA0MyBaIi8+PHBhdGggdHJhbnNmb3JtPSJyb3RhdGUoOTAgNTAgNTApIiBkPSJNNTEuNSA4LjAyNyBBNDIgNDIgMCAwIDEgOTEuOTczIDQ4LjUgTDg0Ljk2OCA0OC41IEEzNSAzNSAwIDAgMCA1MS41IDE1LjAzMiBaIE01MS41IDE3LjUzNSBBMzIuNSAzMi41IDAgMCAxIDgyLjQ2NSA0OC41IEw3NS45NTcgNDguNSBBMjYgMjYgMCAwIDAgNTEuNSAyNC4wNDMgWiIvPjxwYXRoIHRyYW5zZm9ybT0icm90YXRlKDE4MCA1MCA1MCkiIGQ9Ik01MS41IDguMDI3IEE0MiA0MiAwIDAgMSA5MS45NzMgNDguNSBMNzUuOTU3IDQ4LjUgQTI2IDI2IDAgMCAwIDUxLjUgMjQuMDQzIFoiLz48cGF0aCB0cmFuc2Zvcm09InJvdGF0ZSgyNzAgNTAgNTApIiBkPSJNNTEuNSA4LjAyNyBBNDIgNDIgMCAwIDEgOTEuOTczIDQ4LjUgTDg0Ljk2OCA0OC41IEEzNSAzNSAwIDAgMCA1MS41IDE1LjAzMiBaIE01MS41IDE3LjUzNSBBMzIuNSAzMi41IDAgMCAxIDgyLjQ2NSA0OC41IEw3NS45NTcgNDguNSBBMjYgMjYgMCAwIDAgNTEuNSAyNC4wNDMgWiIvPjwvZz48L3N2Zz4K"></a>
  <a href="https://github.com/opensec-git/Pi-Bolt"><img alt="Pi-Bolt" src="https://img.shields.io/badge/Pi--Bolt-050505?style=for-the-badge"></a>
  <a href="https://opensec.in/#disclosures"><img alt="Disclosures" src="https://img.shields.io/badge/Disclosures-050505?style=for-the-badge"></a>
  <a href="https://opensec.in/blog"><img alt="Blog" src="https://img.shields.io/badge/Blog-050505?style=for-the-badge"></a>
  <a href="https://x.com/OpenSecAI"><img alt="X: @OpenSecAI" src="https://img.shields.io/badge/@OpenSecAI-050505?style=for-the-badge&logo=x&logoColor=bafc6b"></a>
  <a href="https://opensec.in/contact"><img alt="Contact" src="https://img.shields.io/badge/Contact-bafc6b?style=for-the-badge"></a>
</p>

**OpenSec** builds AI-native vulnerability management for enterprise and government security teams: deep white-box
codebase scans, codebase-aware pull request reviews and autonomous pentesting, joined into one workflow from the attack
path to the line of code and the fix that closes it.

Research is our proving ground. We have found **150+ CVEs across 100+ open-source repositories**, among them Argo CD,
Apache Airflow, FreeRDP, Gitea and rclone. Published records are on the
[disclosure ledger](https://opensec.in/#disclosures).

## Open source

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/pi-bolt-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/pi-bolt-light.svg">
  <img alt="Pi-Bolt: Pi, the coding agent, compiled ahead of time to one native executable. 10x sooner ready to type, 120x faster writing a 400 KB file, 4.5x less memory than Pi on Node 24." src="assets/pi-bolt-dark.svg" width="100%">
</picture>

<p align="center">
  <a href="https://github.com/opensec-git/Pi-Bolt/stargazers"><img alt="Stars" src="https://img.shields.io/github/stars/opensec-git/Pi-Bolt?style=flat-square&logo=github&label=stars&labelColor=050505&color=bafc6b"></a>
  <a href="https://github.com/opensec-git/Pi-Bolt/releases/latest"><img alt="Version" src="https://img.shields.io/npm/v/pi-bolt?style=flat-square&label=version&labelColor=050505&color=bafc6b"></a>
  <a href="https://www.npmjs.com/package/pi-bolt"><img alt="npm" src="https://img.shields.io/npm/dm/pi-bolt?style=flat-square&logo=npm&label=npm&labelColor=050505&color=bafc6b"></a>
  <img alt="Linux, macOS, Windows, Android" src="https://img.shields.io/badge/linux%20·%20macOS%20·%20windows%20·%20termux-050505?style=flat-square">
</p>

Extensions for Pi and Pi-Bolt, offered by the Pi-Bolt installer:

- **[opensec-pi-subagents](https://github.com/opensec-git/opensec-pi-subagents)**: specialized agents in separate sessions that inherit the parent's model and thinking level, with parallel workflows and scheduled jobs.
- **[opensec-pi-todo](https://www.npmjs.com/package/opensec-pi-todo)**: a todo list for the model, shown as a live panel that survives `/reload` and compaction.
- **[opensec-pi-fff](https://www.npmjs.com/package/opensec-pi-fff)**: fast fuzzy file and content search, with find, grep and `@`-mentions.

Add one with `pi-bolt install npm:<name>`. Pi-Bolt itself also installs with npm,
[Homebrew](https://github.com/opensec-git/homebrew-tap), [Scoop](https://github.com/opensec-git/scoop-bucket) and mise.

## Stack

<p>
  <img alt="TypeScript" src="https://img.shields.io/badge/TypeScript-050505?style=flat-square&logo=typescript&logoColor=bafc6b">
  <img alt="Bun" src="https://img.shields.io/badge/Bun-050505?style=flat-square&logo=bun&logoColor=bafc6b">
  <img alt="C++" src="https://img.shields.io/badge/C++-050505?style=flat-square&logo=cplusplus&logoColor=bafc6b">
  <img alt="Go" src="https://img.shields.io/badge/Go-050505?style=flat-square&logo=go&logoColor=bafc6b">
  <img alt="Python" src="https://img.shields.io/badge/Python-050505?style=flat-square&logo=python&logoColor=bafc6b">
  <img alt="Rust" src="https://img.shields.io/badge/Rust-050505?style=flat-square&logo=rust&logoColor=bafc6b">
  <img alt="React" src="https://img.shields.io/badge/React-050505?style=flat-square&logo=react&logoColor=bafc6b">
  <img alt="Cloudflare" src="https://img.shields.io/badge/Cloudflare-050505?style=flat-square&logo=cloudflare&logoColor=bafc6b">
</p>

<sub><code>// SEE DEEPER INTO YOUR CODE. GET AHEAD OF ATTACKERS. SECURE WHAT MATTERS.</code></sub>
