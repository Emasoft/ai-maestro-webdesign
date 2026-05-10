---
name: TECH-classic-namespace-nesting
category: ascii-classic
source: ascii-diagrams-skill-main/references/network-topology.md
also-in: ascii-diagrams-skill-main/SKILL.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# TECH-classic-namespace-nesting — Linux netns + overlay/underlay

## What it does

Renders Linux network-namespace nesting with an overlay and underlay
network, matching the canonical kernel-network-subsystem diagram:
two namespaces (NS0, NS1) each containing an ipsec0 interface connected
via overlay, with veth pairs living on the underlay.

## When to use

- Linux kernel docs explaining network-namespace isolation
- Container networking docs (Docker bridge, K8s CNI) showing the netns
  view
- VPN overlay diagrams (WireGuard, OpenVPN)

## How it works

- Two outer labeled boxes representing the namespaces.
- Inside each, a nested box for the interface with its IP.
- Connectors drop from each outer box into a "overlay network" labeled
  band.
- Below the overlay, a single outer box for the underlay containing veth
  interfaces with their IPs.

## Minimal example

```
// Source: ascii-diagrams-skill-main/references/network-topology.md lines 66-83
  +--- NS0 namespace -----+  +--- NS1 namespace ---+
  |                        |  |                      |
  |  +-- ipsec0 --------+ |  |  +-- ipsec0 ------+  |
  |  | 192.168.1.100    | |  |  | 192.168.1.200  |  |
  |  +------------------+ |  |  +----------------+  |
  |                        |  |                      |
  +-----------|------------+  +----------|----------+
              |                          |
              +--- overlay network ------+
              |                          |
  +-----------|------ underlay ----------|----------+
  |  +--------v----+              +------v-------+  |
  |  | veth01      |              | veth10       |  |
  |  | 172.16.1.100|              | 172.16.1.200 |  |
  |  +-------------+              +--------------+  |
  +------------------------------------------------+
```

## Gotchas

- Nested boxes need corner-alignment validation (`TECH-box-corner-alignment.md`)
  — a one-column drift at the nested box breaks the outer frame too.
- The `|` vertical that crosses the outer box border at `+----|----+` is
  intentional and valid ASCII; modern Unicode box-drawing would need a
  T-junction (`┴` / `┬`) — use `../amw-box-diagram/` for that rendering.

## Cross-references

- [TECH-classic-k8s-topology](./TECH-classic-k8s-topology.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-classic-multi-service-architecture](./TECH-classic-multi-service-architecture.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-box-corner-alignment](../../amw-ascii-validator/references/TECH-box-corner-alignment.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [network-topology](./network-topology.md) (legacy pattern file)
  > Reference
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill
