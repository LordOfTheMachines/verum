# ADR-0001: Record architecture decisions

- **Status:** accepted
- **Date:** 2026-07-20

## Context

Verum is a long-lived, multi-phase project developed largely by one maintainer
with AI assistance. Decisions made in Phase 1 (threading model, cache policy,
backend protocol) will constrain Phase 6 work months later, and the reasoning
behind them is exactly what gets lost — from the maintainer's memory and from
any assistant's context window alike.

Commit messages capture *what* changed. They are a poor place to look for *why*
an approach was rejected.

## Decision

Architecturally significant decisions are recorded as ADRs in `docs/adr/`,
numbered sequentially: `NNNN-kebab-case-title.md`.

A decision is architecturally significant if it is expensive to reverse: choice
of a dependency, a public protocol shape, a threading or concurrency model, a
persistence format, a licensing constraint.

Each ADR carries a status (`proposed` / `accepted` / `superseded by ADR-NNNN`),
a date, and the sections Context, Decision, Consequences. ADRs are immutable
once accepted — a changed mind means a new ADR that supersedes the old one, not
an edit.

## Consequences

- Adding an architectural decision costs an extra file in the PR; the PR
  template prompts for it.
- Future contributors and future assistant sessions can reconstruct intent
  without archaeology through the git log.
- ADRs accumulate including obsolete ones; the `superseded by` header is what
  keeps them navigable.
