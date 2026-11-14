# TypeScript monorepo from scratch; Python code archived as reference

Status: accepted (2026-11-08)

The product is rebuilt from scratch as a TypeScript monorepo with a Next.js web app (UI, API routes and chat in one deployable). The existing Python code (Clockify fetcher, validators, parser, habits, notebooks) moves to `archive/python/` unchanged. It is read-only reference: its behaviour and tests describe what the new domain code must do, but it is not imported or maintained. We chose TypeScript over extending Python because the Python code needed a large refactor anyway, JavaScript has the strongest interactive chart libraries, and one language for UI, API and domain keeps the later multi-user web app simple.

## Layout

The layout is chosen so an AI agent can work on one package at a time: each package has one job, a short README with its rules, and tests next to the code.

```
CLAUDE.md            root map: packages, commands, rules
CONTEXT.md           domain glossary
docs/adr/            decisions
apps/web/            Next.js: pages, API routes, chat UI
packages/core/       entities, pure functions, use cases, ports (no I/O dependencies)
packages/db/         SQLite adapter and migrations
packages/clockify/   Clockify import adapter
packages/agent/      chat tools (schemas and handlers) and chat loop
archive/python/      old code, read-only (moved with git mv to keep history)
```

Tooling: pnpm workspaces, strict TypeScript, Vitest, ESLint. A lint rule enforces that `packages/core` imports no other workspace package. No Turborepo until build time needs it.

## Consequences

- Jupyter analysis, if still needed, reads the new SQLite file; it does not use the archived Python domain code.
- The Python CI (format, lint, mypy, pytest) and the notebook pre-commit hook stop applying to the active code.
