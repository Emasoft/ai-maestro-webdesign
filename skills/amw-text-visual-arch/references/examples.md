# amw-text-visual-arch — Diagram framing examples

## Table of Contents

- [1. Context diagram](#1-context-diagram)
- [2. Container diagram](#2-container-diagram)
- [3. Component diagram](#3-component-diagram)

This file holds the three full zoom-level examples (context, container, component) for layered ASCII architecture diagrams. The parent `SKILL.md` references this file when concrete examples are needed.

## 1. Context diagram

Outer boundary = "the system"; everything outside is users or external systems.

```
+-----------------+       +-----------------+
|     User        |------>|  The System     |
| (web, mobile)   |       |                 |
+-----------------+       +--------+--------+
                                   |
                                   v
                         +-----------------+
                         |  Payment API    |
                         |  (3rd party)    |
                         +-----------------+
```

## 2. Container diagram

Inside "the system", break out services and data stores.

```
+-------------------+     HTTP      +-------------------+
|  Web Frontend     | ============> |  API Gateway      |
|  [React, CDN]     |               |  [AWS ALB]        |
+-------------------+               +---------+---------+
                                              |
                         +--------------------+--------------------+
                         |                    |                    |
                         v                    v                    v
                +-----------------+  +-----------------+  +-----------------+
                |  Auth Service   |  |  Orders Service |  |  Billing Service|
                |  [Node, k8s]    |  |  [Go, k8s]      |  |  [Python, k8s] |
                +--------+--------+  +--------+--------+  +--------+--------+
                         |                    |                    |
                         v                    v                    v
                +-----------------+  +-----------------+  +-----------------+
                |  Users DB       |  |  Orders DB      |  |  Stripe API     |
                |  [Postgres]     |  |  [Postgres]     |  |  (external)     |
                +-----------------+  +-----------------+  +-----------------+
```

## 3. Component diagram

Inside one service, break out modules / packages / classes.

```
+-------------------------- Orders Service -----------------------+
|                                                                 |
|  +---------------+   +---------------+   +----------------+     |
|  |  HTTP Handler | ->|  Order Domain | ->|  Repository    |     |
|  |  [REST]       |   |  [pure Go]    |   |  [Postgres]    |     |
|  +---------------+   +---------------+   +--------+-------+     |
|                              |                    |             |
|                              v                    v             |
|                      +---------------+   +----------------+     |
|                      |  Event Bus    |   |  Read Model    |     |
|                      |  [Kafka out]  |   |  [Redis cache] |     |
|                      +---------------+   +----------------+     |
+-----------------------------------------------------------------+
```
