---
name: TECH-class-grammar
category: mermaid-grammar
source: diagrams-skills/Pretty-mermaid-skills-main/references/DIAGRAM_TYPES.md
also-in:
---

# Class diagram grammar

## What it does

UML-style class diagrams — classes, attributes, methods, visibility,
relationships (inheritance, composition, aggregation), cardinality,
abstract/interface markers.

## When to use

- Object model documentation for OOP codebases.
- Public API surface — showing consumers what classes exist.
- Domain modeling during design.

## Class definition

```
classDiagram
    class ClassName {
        +String publicField
        -int privateField
        #bool protectedField
        ~String packageField

        +publicMethod()
        -privateMethod()
        #protectedMethod()
        ~packageMethod()
    }
```

## Visibility markers

```
+   Public
-   Private
#   Protected
~   Package / Internal
```

## Relationship arrows (UML)

```
ClassA --|> ClassB     Inheritance        (solid + triangle)
ClassC --* ClassD      Composition        (solid + filled diamond)
ClassE --o ClassF      Aggregation        (solid + open diamond)
ClassG --> ClassH      Association        (solid arrow)
ClassI -- ClassJ       Link               (solid, no arrow)
ClassK ..> ClassL      Dependency         (dotted arrow)
ClassM ..|> ClassN     Realization        (dotted + triangle)
```

## Cardinality

```
Customer "1" --> "*" Order
Order "1" --> "1..*" OrderItem
```

## Abstract / interface / generic

```
class AbstractClass {
    <<abstract>>
    +abstractMethod()*
}

class Interface {
    <<interface>>
    +method()
}
```

The `*` after a method name also marks it abstract.

## Minimal example

```mermaid
%% source: diagrams-skills/Pretty-mermaid-skills-main/references/DIAGRAM_TYPES.md
classDiagram
    class User {
        +String email
        -String password
        +login(password: String): bool
    }
    class Post {
        +String title
        +String body
    }
    User "1" --> "*" Post: creates
```

## Gotchas

- Relationship arrow direction matters — `ClassA --|> ClassB` means
  A inherits FROM B (A is the subclass).
- Method signatures are free-form strings — the renderer doesn't
  parse types. Typos render as-is.
- Too many methods/fields make the diagram unreadable — show only
  the public surface; elide private details with `...`.

## Cross-references

- `TECH-er-grammar.md` — for database schemas (structurally similar).
- `TECH-flowchart-grammar.md` — for non-class graph structures.
- [`../SKILL.md`](../SKILL.md) — parent skill

