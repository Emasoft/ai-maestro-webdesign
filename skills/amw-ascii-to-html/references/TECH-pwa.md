---
name: TECH-pwa
category: ascii-to-html-progressive-enhancement
source: amw-wireframe-builder-agent §9 (pwa routing rows)
also-in: globalCC skill `pwa-development` for library-specific deep dive
---

# Progressive Web Apps — installable web artifacts

## What it does

Augments the produced HTML wireframe with the four PWA primitives every
modern installable web app needs: a Web App Manifest, a service worker
with appropriate caching strategy, the install-banner UX, and the
platform-specific icon set. This TECH file covers the structural
contract; for library-specific patterns (Workbox / Vite-PWA-plugin /
next-pwa) the user can consult the global Claude Code skill
`pwa-development` — it is NOT a plugin skill, the link is informational.

## Web App Manifest (`manifest.json`)

Minimal valid manifest:

```json
{
  "name": "Brand Long Name",
  "short_name": "Brand",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#0b5fff",
  "description": "One-line app purpose, ≤ 200 chars",
  "icons": [
    { "src": "/icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any" },
    { "src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any" },
    { "src": "/icons/icon-maskable-192.png", "sizes": "192x192", "type": "image/png", "purpose": "maskable" },
    { "src": "/icons/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
  ]
}
```

Field rules:
- `name` ≤ 45 chars (Chrome's installer surface truncates after 45)
- `short_name` ≤ 12 chars (home-screen icon label cap on iOS / Android)
- `start_url` MUST be relative or same-origin
- `display: "standalone"` removes browser chrome; `"fullscreen"` for games; `"minimal-ui"` for hybrids; `"browser"` defeats install affordance
- `background_color` shows during the splash screen on Chrome → match the brand bg token
- `theme_color` colors the OS status bar / Android system UI
- `icons[].purpose: "maskable"` is REQUIRED for Android adaptive icons; provide both `any` and `maskable` (maskable has the brand mark inside the safe zone — 80% of the icon — so the OS can crop to circle/squircle/rounded-square)

Reference HTML link:

```html
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#0b5fff">
```

## Service worker (`sw.js`)

Pick ONE caching strategy per route group. Mixing strategies in one
worker without explicit reasoning produces stale assets.

| Strategy | Use for | Behavior |
|---|---|---|
| **Cache-first** | static assets that change rarely (icons, fonts, CSS, JS bundles versioned by hash) | Serve from cache; only hit network on cache miss |
| **Network-first** | HTML documents, API responses that may have updated content | Try network with timeout; fall back to cache on failure |
| **Stale-while-revalidate** | content that's tolerant of one-version-old (avatars, dashboard stats) | Serve cached immediately; fetch network in background to update cache for next request |
| **Network-only** | sensitive POST / mutation endpoints | Never cache (default for all non-GET requests) |
| **Cache-only** | offline pages / static fallback shells | Never hit network (used as a last-resort fallback after network-first) |

Minimal vanilla service worker (cache-first for assets, network-first
for HTML, with offline fallback):

```js
// sw.js — version every release to invalidate old caches
const VERSION = 'v1.0.0';
const ASSET_CACHE = `assets-${VERSION}`;
const PAGE_CACHE  = `pages-${VERSION}`;
const OFFLINE_URL = '/offline.html';

const CORE_ASSETS = [
  '/',
  '/index.html',
  '/offline.html',
  '/manifest.json',
  // bundle paths injected at build time
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(ASSET_CACHE).then((c) => c.addAll(CORE_ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((k) => !k.endsWith(VERSION))
          .map((k) => caches.delete(k))
      )
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method !== 'GET') return; // never cache mutations

  // Network-first for HTML
  if (request.headers.get('Accept')?.includes('text/html')) {
    event.respondWith(
      fetch(request)
        .then((res) => {
          const copy = res.clone();
          caches.open(PAGE_CACHE).then((c) => c.put(request, copy));
          return res;
        })
        .catch(() =>
          caches
            .match(request)
            .then((cached) => cached || caches.match(OFFLINE_URL))
        )
    );
    return;
  }

  // Cache-first for everything else
  event.respondWith(
    caches.match(request).then((cached) => cached || fetch(request))
  );
});
```

Register from the main thread (in `<head>`):

```html
<script>
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/sw.js').catch((e) =>
        console.error('SW registration failed:', e)
      );
    });
  }
</script>
```

## Install-banner UX

Chrome's `beforeinstallprompt` lets you replace the default mini-infobar
with a brand-aligned button:

```js
let deferredPrompt = null;
const installBtn = document.querySelector('#install-app');

window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;
  installBtn?.removeAttribute('hidden');
});

installBtn?.addEventListener('click', async () => {
  if (!deferredPrompt) return;
  deferredPrompt.prompt();
  const { outcome } = await deferredPrompt.userChoice;
  if (outcome === 'accepted') installBtn.setAttribute('hidden', '');
  deferredPrompt = null;
});

window.addEventListener('appinstalled', () => {
  installBtn?.setAttribute('hidden', '');
  // analytics: 'pwa_installed'
});
```

UX rules:
- The install button starts `hidden` and is unveiled only after
  `beforeinstallprompt` fires — never put a static "Install App" button
  that 404s on iOS (which doesn't fire the event)
- Don't auto-prompt on first load — Lighthouse penalizes this
  ("interruptive prompt"). Wait for explicit user intent (clicked button,
  scrolled past hero, completed first task)
- Provide an iOS install instructions sheet for browsers that lack
  `beforeinstallprompt` (Safari iOS) — a tooltip showing "tap Share →
  Add to Home Screen"

## Apple-touch-icon and platform metadata

Add to `<head>`:

```html
<!-- Apple Touch Icon (iOS home screen icon, when manifest.json is ignored) -->
<link rel="apple-touch-icon" href="/icons/apple-touch-icon-180.png">
<link rel="apple-touch-icon" sizes="152x152" href="/icons/apple-touch-icon-152.png">
<link rel="apple-touch-icon" sizes="167x167" href="/icons/apple-touch-icon-167.png">
<link rel="apple-touch-icon" sizes="180x180" href="/icons/apple-touch-icon-180.png">

<!-- Standalone status-bar style on iOS (when added to home screen) -->
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Brand">

<!-- Microsoft tile (Windows 10/11) -->
<meta name="msapplication-TileColor" content="#0b5fff">
<meta name="msapplication-TileImage" content="/icons/ms-tile-144.png">

<!-- Favicon, ico fallback -->
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/icons/icon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="/icons/icon-16.png" sizes="16x16" type="image/png">
```

iOS does NOT read `manifest.json` for the home-screen icon — it uses
`apple-touch-icon` exclusively. Forgetting this leaves iOS users with a
screenshot-of-the-page as the installed icon.

## Required icon set

For full coverage:

| File | Size | Purpose |
|---|---|---|
| `favicon.ico` | 16/32/48 multi-resolution ICO | Browser tab, bookmarks |
| `icon-16.png` | 16×16 | Modern favicon (some browsers) |
| `icon-32.png` | 32×32 | Modern favicon |
| `icon-48.png` | 48×48 | Windows shortcut |
| `icon-180.png` (apple-touch-icon) | 180×180 | iOS home screen (most common) |
| `icon-192.png` | 192×192 | Android home screen, manifest |
| `icon-512.png` | 512×512 | Android splash, manifest, store listings |
| `icon-maskable-192.png` | 192×192 (with safe zone) | Android adaptive icon |
| `icon-maskable-512.png` | 512×512 (with safe zone) | Android adaptive icon |
| `ms-tile-144.png` | 144×144 | Windows 10 tile |

`amw-asset-generator-agent` is the appropriate plugin agent for
generating this set from a single brand SVG.

## Lighthouse PWA audit thresholds

To pass Lighthouse PWA category:
- Page is served over HTTPS (or `localhost` for dev)
- Manifest is linked, has all required fields, includes 192×192 + 512×512 icons (one of each)
- Service worker registered
- Themed status bar (theme-color meta + manifest theme_color)
- Splash screen colors match (manifest background_color)
- Page is responsive (viewport meta, no horizontal scroll)
- All page assets are reachable without network (offline test)

## What the agent MUST do

1. Generate `manifest.json` with all required fields and a `purpose: maskable` icon variant
2. Inline the service-worker registration script in `<head>` of every wireframe-builder HTML output
3. Link `apple-touch-icon` for iOS coverage
4. Add the `theme-color` meta for status bar
5. Document the install-banner UX as a `recommendations` entry — the actual JS goes inline if the brief calls for an install button
6. Coordinate icon generation with `amw-asset-generator-agent` for the full required set

## What the agent MUST NOT do

- Generate a service worker that caches POST/PUT/DELETE responses
- Auto-prompt the install banner on page load
- Add a static "Install App" button without a `beforeinstallprompt` gate
- Skip the `purpose: maskable` icon variant (Android renders an off-center
  cropped icon without it)
- Cache the manifest itself with a long max-age (manifest changes
  invalidate icons; cache it short)
