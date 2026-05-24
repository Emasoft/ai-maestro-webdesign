# vecui — Vector API

> Authoritative `Vec` method reference, taken from the source `lib/main.ts`, not the README.

## Table of Contents

- [Value model](#value-model)
- [Constructors](#constructors)
- [Vec members](#vec-members)
- [Missing operators](#missing-operators)

## Value model

- **Immutable.** `v.add(...)` and every other op return a fresh value; the receiver is never modified. `x`/`y` are `readonly`.
- **Chaining.** Because every op returns a new `Vec`, calls chain fluently: `r.o.add(r.d.x, 0).add(8, 0)`.
- **Overloaded inputs.** Most vector ops accept either another `Vec` or loose `(x, y)` scalar components, so `v.add(other)` and `v.add(8, 0)` are interchangeable.

Treat vectors like number primitives — never present an in-place-mutation pattern.

## Constructors

### `vec(...)` overloads

```typescript
vec(1, 2)          // (x, y)
vec(100)           // single number → both components: vec(100, 100)
vec([1, 2])        // [x, y] tuple
vec({ x: 1, y: 2 })// { x, y } object
```

When called with a single number, **both** components are set to it (`vec(100)` ⇒ `{x:100, y:100}`) — handy for square dimensions and uniform scaling. A user who wants a one-axis vector needs `vec(100, 0)` or `vec(0, 100)`.

## Vec members

Every method is on a `Vec` instance and returns a new value (immutable). Methods marked **overloaded** also accept loose `(x, y)` scalars in place of a `Vec` argument.

| Member | Signature → returns | Notes |
|---|---|---|
| `x` / `y` | `readonly number` | Components. |
| `yx` | `Vec` (getter) | Components swapped: `vec(1,2).yx ⇒ vec(2,1)`. |
| `setX(x)` / `setY(y)` | `Vec` | New vector with one component replaced. |
| `map(fn)` | `Vec` | `fn(x, y) => [nx, ny]` (must return length-2 array, else throws). |
| `reduce(fn)` | `T` | `fn(x, y) => T` collapse to a scalar/any value: `vec(1,2).reduce((x,y)=>x+y) ⇒ 3`. |
| `add(v)` / `add(x, y?)` | `Vec` | Vector addition. **overloaded** |
| `sub(v)` / `sub(x, y?)` | `Vec` | Vector subtraction. **overloaded** |
| `mul(v)` / `mul(x, y)` / `mul(scalar)` | `Vec` | Element-wise (Hadamard) product, **or** scalar scale when given one number. This is the scaling operator — there is no separate `scale`. **overloaded** |
| `div(scalar)` / `div(v)` / `div(x, y)` | `Vec` | Element-wise division, or divide by one scalar. `vec(d).div(-2)` centers a box of dimension `d`. **overloaded** |
| `dot(v)` / `dot(x, y)` | `number` | Dot product `x·x' + y·y'`. **overloaded** |
| `cross(v)` / `cross(x, y?)` | `number` | 2D cross product `x·y' − y·x'` (a scalar, the signed z of the 3D cross). **overloaded** |
| `len()` | `number` | L2 norm (length). `vec(3,4).len() ⇒ 5`. |
| `norm()` | `Vec` | Unit vector (divides by `len()`). `vec(3,4).norm() ⇒ vec(0.6, 0.8)`. |
| `rotRad(radians)` | `Vec` | Rotate counterclockwise by radians. |
| `rotDeg(degrees)` | `Vec` | Rotate counterclockwise by degrees (`rotRad(deg·π/180)`). |
| `angleTo(target)` | `number` | Unsigned angle (radians) between the two vectors via `acos`. |
| `lookAt(target, front?)` | `number` | Rotation (radians) so an object at this point faces `target`. `front` ∈ `"x" \| "y" \| "-x" \| "-y"`, default `"x"`. Built on `atan2`; used in the demo to rotate an element toward the cursor. |
| `asArray()` | `[number, number]` | Tuple form. |
| `isInRect(rect)` / `isInRect(input)` / `isInRect(o, d)` | `boolean` | Point-in-rectangle test; accepts a `Rect`, an `InputRect` object, or `(origin, dimension)` vectors. |
| `equals(v)` / `equals(x, y)` | `boolean` | Strict component equality. **overloaded** |

## Missing operators

There is **no `lerp`** and **no `scale`** method in this library. Interpolate by hand (`a.add(b.sub(a).mul(t))`), scale via `mul(scalar)`, and compute distance with `b.sub(a).len()`. There is no 3D `vec3`, no matrix type, and no mutable setter. Do not fabricate a richer API from generic vector-library knowledge.
