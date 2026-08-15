# Habit tracking

Status: shipped. Last reviewed: 2026-08-15.

## What

Scores recurring behaviors from the recorded data so trends are visible: getting up early (earlier = higher score), going to bed early (earlier than target = higher score), and habits derived from time intervals (presence, counts, one-of choices). Visualized in the habit notebook.

## Why

The method is not only accounting; it is behavior change. Habit scores turn raw timestamps into feedback (am I sleeping earlier? exercising?).

## Key design points (settled)

- Bed habit correctly handles going to bed after midnight (a bed time past midnight still belongs to the previous day's evening).
- Getup and bed habits share one scoring concept: signed distance from a target time.

## Honest limitations

- Habit definitions and targets are configured by the developer-owner, not manageable through any user interface.

## History

Supersedes the ad-hoc request note `docs/requirement/support_bedtime_habit.md` (2025; bed habit has since shipped).
