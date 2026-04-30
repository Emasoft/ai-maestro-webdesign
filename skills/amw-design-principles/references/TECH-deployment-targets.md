---
name: TECH-deployment-targets
category: design-principles-deployment
source: ai-maestro-webdesigner-main-agent §15 (Production deployment doctrine)
also-in: globalCC skills `vercel-development`, `netlify-development`, `cloudflare-development` for platform-specific deep dives
---

# Production deployment targets

## What it does

When the user asks "where do I deploy this?" after a Phase B build completes, the main-agent surfaces this catalog. The plugin produces unbuilt HTML/CSS/JS by default; deployment is out of plugin scope but the recommendations below let main-agent orient the user without inventing platform-specific advice.

## When this is relevant

Main-agent §15 mentions "production deployment" as out-of-scope, but a complete user experience expects guidance. Surface this catalog under "Next steps" in the final job-completion report.

## Catalog

| Platform | Best for | Build step required | Notes |
|---|---|---|---|
| **Vercel** | Next.js / React / static; preview deploys per branch; serverless functions on `/api/*` | Auto-detected (Next.js, Astro, Vite, etc.) | Best DX for `target_stack=shadcn+next`; auto-imports environment variables; Edge runtime available. |
| **Netlify** | Static / Jamstack; preview deploys; serverless functions; forms via Netlify Forms | Auto-detected (most frameworks); `_redirects` and `netlify.toml` give precise control | Best for `target_stack=static-html` or `tailwind-vanilla`; built-in form handling without server. |
| **Cloudflare Pages** | Static / Workers; global CDN; lowest cold-start; Pages Functions on `/functions/` | Auto-detected; `wrangler.toml` for Workers integration | Best for performance-critical pages and global audiences; Workers integration unique. |
| **GitHub Pages** | Static-only; free; integrates with GitHub Actions | Manual via Actions or CI | Best for documentation sites, demos, OSS landing pages. No serverless / no env vars. |
| **Render** | Full-stack with managed databases; auto-deploys from git | Detected per stack | Good for monolithic apps; cheaper than Vercel for heavy traffic. |
| **AWS Amplify Hosting** | Production-grade with AWS integration (Cognito, AppSync) | Auto-detected | Best when the rest of the stack is AWS. More config than Vercel/Netlify. |
| **Self-hosted (nginx / Caddy)** | Full control; no vendor lock-in | Manual | Use when compliance / data-sovereignty rules out hosted PaaS. |

## Decision tree

```
What stack did wireframe-builder produce?
├── target_stack=static-html
│   └── User priority?
│       ├── Free → GitHub Pages
│       ├── Best DX → Netlify
│       ├── Best perf → Cloudflare Pages
│       └── Already on Vercel → Vercel
├── target_stack=shadcn+next or shadcn+vite
│   └── Vercel (default) or Netlify or Cloudflare Pages
├── target_stack=tailwind-vanilla or tailwind-v4
│   └── Same as static-html
└── Custom server-side requirements (booking engine, payment)
    └── Render / AWS Amplify / self-hosted
```

## What main-agent surfaces

A single line in the final report's "Next steps" section:

> **Deployment:** This is a `<target_stack>` artifact. Recommended platforms for your needs:
> - <platform-1> — <one-line reason>
> - <platform-2> — <one-line reason>
>
> See `skills/amw-design-principles/references/TECH-deployment-targets.md` for the full catalog and decision tree.

## What main-agent MUST NOT do

- Pick ONE platform without surfacing trade-offs to the user
- Run a deployment command on the user's behalf (deployment requires credentials and explicit authorization)
- Recommend AWS Amplify when the user has zero AWS context (per "explicit assumption beats silent guess")
- Skip the recommendation entirely (the user may not know which platform fits)

## Plugin-scope boundary

Deployment automation is OUT of plugin scope. The plugin produces the artifact; the user (or a downstream tool) ships it. If the user asks for deployment automation, main-agent surfaces:
- The platform catalog above
- Pointers to the global Claude Code skills `vercel-development`, `netlify-development`, `cloudflare-development` (these are NOT plugin skills)
- A caveat that automation requires the user's credentials and is best done outside this plugin's scope
