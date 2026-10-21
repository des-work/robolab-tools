# RoboLab Tools

**Tools for scoped robot-network observation, operator timelines, and careful interpretation of capture evidence.**

This public source snapshot extracts the reusable tooling from a graduate robotics security-monitoring project. It contains seven command-line tools and a shared network-scope helper. Lab evidence, device inventories, campus settings, internal runbooks, and the private development history are excluded.

| Tool | Purpose |
| --- | --- |
| `robot-listen` | Observe a selected configured robot's wireless traffic at an administered access point; record operator action marks on the same UTC timeline. |
| `wire-listen` | Observe a robot's wired link on an authorized remote operator machine, with an explicit subnet filter and consent prompt. |
| `robot-roll-call` | Compare access-point station-table reads during a handler-controlled procedure; report candidate device attribution and ambiguity. |
| `robot-round-up` | Capture two handler-controlled boots of the same device and compare observed startup traffic. |
| `rl-unattended-capture` | Time- and storage-bounded capture streamed from the access point to a local ring buffer. |
| `robot-show` | Browse existing local evidence with hardware-address labels replacing raw addresses by default. |
| `ap-hostkey` | Check a management host's SSH identity against already trusted keys, including when its address changes. |

Traffic observation is passive at the chosen capture point. Authorized SSH management, public-host-key retrieval, and capture streaming **generate management traffic**. These tools do not command robot movement. A physical robot's approved operating and safety procedure remains a separate responsibility.

## Setup

Developed on Linux, with Python 3 and Bash. Depending on the command, the environment needs OpenSSH, `iproute2`, `tcpdump`, Zeek, Wireshark command-line utilities, NetworkManager, and access to an administered AP with a compatible station-table/capture interface. This is an experimental toolkit; dependencies and live hardware behavior are environment-specific.

```bash
git clone https://github.com/des-work/robolab-tools.git
cd robolab-tools
export PATH="$PWD/tools:$PATH"
export RL_OPERATOR="your-operator-label"
export RL_LAB_NETWORK="your-authorized-lab-cidr"
export AP_MAC_PREFIX="your-access-point-vendor-prefix"
```

`RL_LAB_NETWORK` must be a valid IPv4 network in CIDR notation. For example, **`192.0.2.64/26` is a documentation-only network**, useful for offline tests; substitute your authorized network for actual use. The membership check uses the complete CIDR, not a string prefix. Missing or invalid scope fails closed before AP discovery/SSH checks. A vendor prefix is not a unique device identity; verify the AP's SSH key independently before enabling the tools.

Create your private robot inventory from `robots.example.json` at `~/.config/robolab/robots.json`, or point `ROBOLAB_ROBOTS` at it. Keep that file private. Configure key-based management access to your own equipment; the repository contains no credentials or trusted-host database.

```bash
robot-listen --help
robot-listen --check
```

`--check` can perform management connections after local scope checks succeed. It is not an offline test. Read the [operator guide](docs/OPERATOR-GUIDE.md) before a capture or rehearsal.

## Evidence and limits

- AP station entries can linger after a device powers off. A listed address does not establish current power state or activity.
- A new station-table entry is a candidate attribution. Concurrent arrivals, stale entries, and address changes can make the result ambiguous.
- Packet counts include both directions unless explicitly separated. An empty capture and a failed capture are different outcomes.
- Traffic near an operator mark shows timing, not causation. A destination label is a classification heuristic, not proof of a service's function or of what encrypted content says.
- Two similar boots describe two observations of one device. They do not establish general reliability or behavior across a device family.
- `robot-show` replaces MAC addresses; this is **not complete anonymization**. IP addresses, hostnames, payloads, filenames, and operator notes can still identify a lab or person.

## Offline validation

```bash
python3 -m unittest discover -s tests -v
```

These tests cover exact CIDR membership, missing/invalid-scope rejection, suppression of remote checks outside scope, and script syntax. They do not capture traffic, contact a robot, verify real AP compatibility, or establish the scientific validity of a lab finding. See [validation](docs/VALIDATION.md).

## Project context

Developed by Desmond Workman for graduate work in robotics network security monitoring. The engineering focus is reproducible collection, explicit observation limits, and keeping operational evidence separate from reusable tools. The original lab/organization repositories and evidence stores remain private.

A public-source license has not yet been selected for this extracted snapshot. Public visibility alone does not grant additional reuse rights.
