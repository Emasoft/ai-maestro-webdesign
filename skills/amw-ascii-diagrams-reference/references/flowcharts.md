> Reference library for the ASCII Diagrams Reference skill. Source: CHI'24 paper analysis. Every example validates against ../../bin/amw-validate-ascii.py.

# Flowcharts and Control Flow

Use for: conditional paths, decision trees, request processing pipelines.

**Basic decision flow:**
```
                    +----------+
                    |  Input   |
                    +----+-----+
                         |
                    +----v-----+
                    | Validate |
                    +----+-----+
                         |
                   +-----+------+
                   | Valid?     |
                   +--+------+--+
                      |      |
                   yes|      |no
                      |      |
                 +----v--+ +-v------+
                 | Store | | Reject |
                 +-------+ +--------+
```

**Pipeline with branching (real pattern from Chromium):**
```
  Request
    |
    v
  +-------------------+
  | Parse Headers     |
  +--------+----------+
           |
     +-----+------+
     |            |
     v            v
  +------+    +-------+
  | HTTP |    | HTTP2 |
  +--+---+    +---+---+
     |            |
     +-----+------+
           |
           v
  +--------+----------+
  | Route to Handler  |
  +-------------------+
```

**Key rules:**
- Center the flow vertically when possible
- Keep decision branches clearly left/right or labeled
- Use `+` for every corner and junction
- Arrow `v` on the line going into the next box
