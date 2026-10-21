# Operator guide

Use only the equipment, network, devices, and capture scope you are authorized to observe. The tools assume a Linux workstation and a compatible administered access point; they are not automatic discovery tools for an unfamiliar network.

## Local configuration

| Variable | Purpose |
| --- | --- |
| `RL_LAB_NETWORK` | Required authorized IPv4 CIDR for the operator's lab-network connection. |
| `AP_MAC_PREFIX` | AP vendor prefix used against the existing neighbor cache; verify the actual host key separately. The historical default is a generic vendor OUI and is not a unique identity. |
| `RL_OPERATOR` | Operator label written to records. |
| `ROBOLAB_ROBOTS` | Private inventory; defaults to `~/.config/robolab/robots.json`. |
| `OUTDIR` | Interactive capture/run output; defaults under `~/Documents/robolab-evidence/scans`. |
| `ROBOLAB_EVIDENCE` | Evidence root used by `robot-show`. |
| `ROBOT_NET` | Wired-link capture subnet; default `192.168.123.0/24`, reflecting the original device family. Verify it for your own hardware. |
| `RL_OUTDIR` | Unattended capture output; default `~/robolab-capture`. |

Keep the robot inventory, captures, logs, operator notes, and SSH files outside Git. The supplied ignore rules reduce accidental commits; they do not sanitize existing evidence.

## Choose the vantage point

`robot-listen` captures at the wireless access point. `wire-listen` captures on the authorized machine at the other end of the robot's cable. The two observe different links. Keep their UTC clocks synchronized before correlating activity.

Default interactive robot capture uses the selected hardware-address filter. Wider modes are available in some tools and require explicit operator acknowledgment. Inspect the actual filter before starting. Acknowledgment flags are not an authorization system; scope depends on the operator's configuration and permissions.

## Before collecting evidence

Confirm device attribution, the capture point, the filter, disk space, time synchronization, and the physical handler's readiness. A software preflight does not verify that a physical robot is safe to power or operate. Follow the device owner's approved procedure; the network script waits for the handler and does not control the robot.

Record a quiet baseline and mark actual operator actions as they happen. Keep failures and ambiguous results in the record. Do not report an empty capture as a quiet device until the capture path, filter, device attribution, and physical state are established.

## Rehearsal

`robot-round-up --dry-run` and `robot-roll-call --dry-run` rehearse their procedure. The public snapshot suppresses remote preflight checks in these modes. Output is rehearsal data, not a real capture or result. EOF at a required human pause stops the procedure.

Avoid mixing rehearsal output with collected evidence. Use a separate `OUTDIR` for rehearsals. Tests use temporary directories and mocked management commands.

## Host identity

`ap-hostkey` checks whether the host key is already trusted at the current address or elsewhere in the local known-hosts file. It does not independently prove that a key belongs to your AP. Establish that trust through your own verified setup process. The helper refuses an unfamiliar key; it can add a new address for an already trusted key.

## Sharing results

Share a separately reviewed narrative or aggregate result. Captures, hardware identifiers, hostnames, network layouts, and operator notes can expose other people or an institution. The public repository contains reusable source and fictional configuration examples only; it contains no collected lab evidence.
