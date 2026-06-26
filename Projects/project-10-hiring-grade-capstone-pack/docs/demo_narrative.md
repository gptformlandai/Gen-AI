# 3-Minute Demo Narrative

## Opening

"This capstone is about RAG reliability, not just RAG mechanics. I start with a baseline assistant, show where it fails, then walk through how I diagnosed and fixed the system with measured before-vs-after results."

## Minute 1: System

"The user sends a question and role. The system first checks guardrails. If the request is unsafe or unauthorized, it refuses before retrieval. If it is allowed, the system rewrites the query, retrieves candidates, reranks evidence, and answers only from cited context."

## Minute 2: Failure

"The baseline looked okay on direct matches, but failed realistic questions with synonyms. For example, 'How should operators triage an incident?' ranked an administrator-permissions document first. The correct incident-response document was present but ranked second, so this was not a corpus coverage issue. It was a retrieval-ranking issue."

## Minute 3: Fix And Results

"I added one targeted intervention: reranking with title, tag, synonym, and phrase features. I kept the answer synthesizer unchanged so the improvement is attributable to retrieval. The debugging case study improved from 58.33% to 100.00%, and retrieval failures dropped from 5 to 0. The broader advanced RAG project improved from 76.00% to 100.00% across 25 scenarios."

## Close

"The reason this is useful hiring evidence is that the failures are visible, the tradeoffs are documented, and the improvement is measured. It shows I can build the system and debug it like an engineer."

