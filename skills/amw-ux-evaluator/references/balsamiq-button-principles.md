## Table of Contents

- [Core Principles](#core-principles)
  - [1. Use Conventional Labels](#1-use-conventional-labels)
  - [2. Say Exactly What Happens](#2-say-exactly-what-happens)
  - [3. Primary and Secondary Should Look Different](#3-primary-and-secondary-should-look-different)
  - [4. Primary Action on the Right](#4-primary-action-on-the-right)
  - [5. Use Adequate Spacing](#5-use-adequate-spacing)
  - [6. Make Buttons Look Clickable](#6-make-buttons-look-clickable)
  - [7. Size Appropriately](#7-size-appropriately)
  - [8. Use Icons Wisely](#8-use-icons-wisely)
  - [9. Consider Loading States](#9-consider-loading-states)
  - [10. Error Prevention](#10-error-prevention)
- [Button Hierarchy Summary](#button-hierarchy-summary)
- [Common Mistakes](#common-mistakes)

# Balsamiq Button Design Best Practices

Source: https://balsamiq.com/blog/button-design-best-practices/

## Core Principles

### 1. Use Conventional Labels
- Use words and phrases users expect
- "Sign Up" not "Get Started" or "Join"
- "Sign In" not "Login" or "Enter"
- "Submit" for forms, "Save" for persistence

### 2. Say Exactly What Happens
- Button text should describe the action outcome
- "Delete Account" not "Proceed" or "Continue"
- "Send Message" not "Submit"
- "Create Project" not "Next"

### 3. Primary and Secondary Should Look Different
- Primary: Filled, prominent, brand color
- Secondary: Ghost/outline, less prominent
- Don't make them compete for attention

### 4. Primary Action on the Right
- Following natural reading flow (LTR languages)
- [Cancel] [Submit] - not [Submit] [Cancel]
- [Sign In] [Sign Up] - secondary left, primary right

### 5. Use Adequate Spacing
- Prevent accidental clicks
- Create clear visual grouping
- Minimum 8px between buttons in a group
- Minimum 24px between button groups

### 6. Make Buttons Look Clickable
- Use visual affordances (shadows, borders, fills)
- Hover states provide feedback
- Disabled states clearly different

### 7. Size Appropriately
- Touch targets: 44x44px minimum on mobile
- Desktop can be smaller but still easily clickable
- Primary buttons can be slightly larger

### 8. Use Icons Wisely
- Only when meaning is universally clear
- Sun/Moon for theme toggle = good
- Abstract icons without labels = risky

### 9. Consider Loading States
- Show progress for async actions
- Disable button during processing
- Provide feedback on completion

### 10. Error Prevention
- Destructive actions need confirmation
- Double-check before irreversible operations
- Use color to signal danger (red for delete)

## Button Hierarchy Summary

```
Visual Hierarchy (most to least prominent):
1. Primary CTA - Filled, shadow, brand color
2. Secondary - Outline/ghost, no fill
3. Tertiary - Text only, minimal styling
4. Utility - Icon only, subtle
```

## Common Mistakes

| Mistake | Example | Fix |
|---------|---------|-----|
| Creative labels | "Let's Go!" | "Sign Up" |
| Same styling | Both buttons filled | Primary filled, secondary ghost |
| Wrong order | [OK] [Cancel] | [Cancel] [OK] |
| Too close | 4px gap | 8-12px gap minimum |
| Unclear action | "Continue" | "Create Account" |
