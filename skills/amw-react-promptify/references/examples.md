# react-promptify worked examples

## Table of Contents

- [Stateful prompt with a custom modal host](#stateful-prompt-with-a-custom-modal-host)
- [Stateless confirm-style prompt](#stateless-confirm-style-prompt)
- [Bring-your-own-modal (shadcn Dialog) host](#bring-your-own-modal-shadcn-dialog-host)

## Stateful prompt with a custom modal host

A custom modal host plus a stateful prompt extracted into its own component — the correct pattern when the prompt needs hooks (see the no-hooks-in-render caveat in [api](./api.md#the-no-hooks-in-render-caveat)).

```tsx
import { useState } from "react";
import { createPrompter, CallbackFn } from "react-promptify";

const { Prompter, prompt } = createPrompter();

// Define ONCE where/how prompts render.
function App() {
  return (
    <>
      <Prompter>
        {({ children, open, cancel }) =>
          open ? (
            <div className="modal-backdrop">
              <div className="modal">
                {children}
                <button onClick={cancel}>Cancel</button>
              </div>
            </div>
          ) : null
        }
      </Prompter>
      <Settings />
    </>
  );
}

// Hooks are NOT allowed inside the prompt() render fn — extract a component.
function NameForm({ done }: { done: CallbackFn<string | null> }) {
  const [value, setValue] = useState("");
  return (
    <form onSubmit={(e) => { e.preventDefault(); done(value); }}>
      <input value={value} onChange={(e) => setValue(e.target.value)} autoFocus />
      <button type="submit">Submit</button>
    </form>
  );
}

// Call prompt() anywhere, get the value RIGHT here.
function Settings() {
  const [name, setName] = useState("");
  async function edit() {
    const result = await prompt<string>((done) => <NameForm done={done} />);
    setName(result ?? name); // handle the cancel (null) branch
  }
  return (
    <div>
      <p>Name: {name}</p>
      <button onClick={edit}>Edit name</button>
    </div>
  );
}
```

## Stateless confirm-style prompt

For a confirm-style prompt with no state, inline the render function directly (no extracted component needed) and call `done(true)` / `done(false)`:

```tsx
const ok = await prompt<boolean>((done) => (
  <div>
    <p>Delete this item?</p>
    <button onClick={() => done(true)}>Delete</button>
    <button onClick={() => done(false)}>Keep</button>
  </div>
));
if (ok) await remove(); // ok is true | false | null
```

## Bring-your-own-modal (shadcn Dialog) host

A shadcn `Dialog` (see [shadcn-ui](../../amw-shadcn-ui/SKILL.md)) is a natural host inside `Prompter` — pass `open` straight through and wire `cancel` to its dismiss:

```tsx
<Prompter>
  {({ children, open, cancel }) => (
    <Dialog open={open} onOpenChange={(o) => { if (!o) cancel(); }}>
      <DialogContent>{children}</DialogContent>
    </Dialog>
  )}
</Prompter>
```

This skill drives the async value flow; shadcn renders the box. Wiring `cancel` to `onOpenChange` means Escape / backdrop click / Close resolve the promise with `null` rather than leaving it pending.
