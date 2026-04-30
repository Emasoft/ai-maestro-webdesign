# React + Babel version-lock spec

> When writing React components inside an HTML file, you MUST use this exact CDN set — **never casually upgrade**.

## Required CDN URLs

```html
<script src="https://unpkg.com/react@18.3.1/umd/react.development.js" integrity="sha384-hD6/rw4ppMLGNu3tX5cjIb+uRZ7UkRJ6BPkLpg4hAu/6onKUg4lLsHAs9EBPT82L" crossorigin="anonymous"></script>
<script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js" integrity="sha384-u6aeetuaXnQ38mYT8rp6sbXaQe3NL9t+IBXmnYxwkUI2Hw4bsp2Wvmx4yRQF1uAm" crossorigin="anonymous"></script>
<script src="https://unpkg.com/@babel/standalone@7.29.0/babel.min.js" integrity="sha384-m08KidiNqLdpJqLq95G/LEi8Qvjl/xUYll3QILypMoQ65QorJ9Lvtp2RXYGBFj1y" crossorigin="anonymous"></script>
```

**Forbidden:**
- ❌ react@18 (unpinned patch version)
- ❌ Omitting the `integrity` hash
- ❌ Using `type="module"`

---

## Styles-object naming rule

**Never** use a generic name like `const styles = { ... }`. When multiple Babel files load on the same page, the global-scope `styles` objects overwrite each other and the UI breaks mysteriously.

```jsx
// ❌ Wrong
const styles = { container: { ... } };

// ✅ Right — prefix with the component name
const terminalStyles = { container: { ... } };
const cardStyles = { container: { ... } };

// Or write inline styles directly
<div style={{ padding: 16 }}>...</div>
```

---

## Sharing components across Babel files

Every `<script type="text/babel">` block transpiles into its **own scope**. To define in file A and use in file B:

```jsx
// At the end of components.jsx:
Object.assign(window, {
  Terminal, Line, Spacer,
  Gray, Blue, Green, Bold,
});
```

Then `scenes.jsx` can use `<Terminal />` directly.

---

## Common error map

| Symptom | Cause | Fix |
|------|-----|------|
| "Cannot read property X of undefined" (intermittent) | Multiple styles objects clobbering each other | Prefix each styles with its component name |
| React component not defined | Not exported to window across Babel files | Add `Object.assign(window, {...})` at end of the source file |
| Integrity check failed | CDN upgrade changed the hash | Pin the patch version; don't use react@18 |
