# Audit Logging

## What Is Logged

- request ID;
- session ID;
- agent name;
- tool name;
- latency;
- outcome;
- errors;
- safety result.

## Where

Local traces are written to `.traces/`.

## Production

Forward callback events to Cloud Logging and Cloud Trace with principal/user identity and resource labels.

