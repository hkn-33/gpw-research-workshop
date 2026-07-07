# Security Policy

## Scope

This is a local research toolkit: markdown playbooks plus standard-library Python that fetches public market data over HTTPS. It stores no credentials, runs no server and executes no trades.

## Reporting a vulnerability

Open a GitHub security advisory or an issue. Relevant reports include: unsafe handling of fetched data, path traversal in report handling, or anything that could make the tools execute untrusted input.

## User-side notes

- Never commit `portfolio.md` — it is gitignored by default; keep it that way.
- The tools call only `query1.finance.yahoo.com`; skills additionally read public financial news sites listed in `AGENTS.md`.
