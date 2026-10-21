# Validation and release scope

Checked on Linux with Python 3.14.6 and Bash on 2026-10-21. Eight offline test methods cover CIDR membership/boundaries, invalid or absent configuration, AP-discovery/SSH suppression outside scope, rehearsal without management connections, per-key SSH trust preservation, and Bash syntax for all four shell tools. Tests use mocked commands, fictional documentation addresses, and temporary output directories.

The source was extracted from the private RoboLab tools repository at commit `9cb42e8009ddedf73bbc45779004c0b105870549`. The public snapshot removes campus-specific runbooks, bindings, measured lab observations, and prior history. It adds a required configurable lab CIDR, exact network-membership checks, and fail-closed management/rehearsal behavior. Host-key migration retains only individually trusted keys, rather than accepting every algorithm returned alongside one recognized key. It preserves the original command names and output style.

No live capture, campus-network connection, AP query, robot operation, or model evaluation was performed for this publication check. These checks do not certify device attribution, capture completeness, classification accuracy, physical safety, or behavior on another lab's hardware. Real collection still requires a verified capture path, scope, and operator record.

The repository contains reusable source and example configuration only. Original lab evidence, internal records, organization repositories, and device inventories remain private. Source publication is not publication of the study's raw data or findings.
