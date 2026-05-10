> Reference library for the ASCII Diagrams Reference skill. Source: CHI'24 paper analysis. Every example validates against ../../bin/amw-validate-ascii.py.

# State Machines

## Table of Contents

- [Reference](#reference)

## Reference

Use for: protocol states, lifecycle management, connection handling.

**TCP-style connection states:**
```
                     +--------+
              +----->| CLOSED |<-----+
              |      +---+----+      |
              |          |           |
              |     open |           | timeout
              |          v           |
              |      +---+----+     |
              |      | OPENING|-----+
              |      +---+----+
              |          |
              |    ready |
              |          v
         close|      +---+-------+
              |      | CONNECTED |
              |      +---+-------+
              |          |
              +----------+
```

**Simple state machine with labeled transitions:**
```
         init        run          done
  IDLE -------> RUNNING -------> COMPLETE
   ^              |
   |    error     |
   +--------------+
```

**Key rules:**
- States in boxes or CAPS
- Transitions labeled on or near the connecting line
- Initial state has an incoming arrow from nowhere (or mark it)
- Terminal states can have double borders or special marking
