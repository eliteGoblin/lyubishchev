# ADR-003: CLI is the API; chat is an agent invoking the CLI

Date: 2026-08-15. Status: accepted.

## Context

The target UX is conversational ("I'm doing X" starts a timer), which suggests building a chat application or an MCP server. That is a large surface to build and maintain before the core habit even exists.

## Decision

The command line is the product's API. Chat ingest is implemented as an agent that invokes the CLI. No MCP server or standalone chatbot app is built until the CLI proves insufficient.

## Consequences

- One interface to test and stabilize; chat gets it for free.
- CLI → HTTP API remains an L2 swap if a service is ever needed.
- Risk accepted: agent-driven chat quality is bounded by what the CLI exposes.
