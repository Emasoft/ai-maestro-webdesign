> Reference library for the ASCII Diagrams Reference skill. Source: CHI'24 paper analysis. Every example validates against ../../bin/amw-validate-ascii.py.

# Trees and Hierarchies

Use for: file systems, org charts, class hierarchies, DOM trees.

**File tree:**
```
  project/
  |
  +-- src/
  |   +-- main.py
  |   +-- utils/
  |   |   +-- helpers.py
  |   |   +-- validators.py
  |   +-- models/
  |       +-- user.py
  |       +-- order.py
  |
  +-- tests/
  |   +-- test_main.py
  |   +-- test_utils.py
  |
  +-- README.md
  +-- pyproject.toml
```

**Class hierarchy (from LLVM-style codebases):**
```
          Value
          |
    +-----+------+
    |             |
  User        Constant
    |             |
  +--+--+     +--+---+
  |     |     |      |
 Inst  Arg  GlobVar  Func
```

**Key rules:**
- Use `+--` for branches, `|` for vertical continuation
- Last child doesn't need the continuing `|` on the parent line
- Indent consistently (3-4 spaces per level)
