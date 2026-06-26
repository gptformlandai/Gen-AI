# Sessions, State, And Memory

## What It Is

Session state is transient per-request context. Memory is durable resolution knowledge that should survive across sessions.

## Where It Appears

- Session: `sessions/session_manager.py`
- Memory: `memory/memory_service.py`
- Runner state updates: `runner.py`

## Why It Matters

Investigation context should not pollute long-term memory. Useful resolution notes should.

## Extend It

Use a database-backed session service and Vertex AI Memory Bank or another persistent memory store.

