# NERF Harness v0.1

Append-only research harness for repeated, inspectable model analysis.

## What it does

1. Ingest one text artifact.
2. Run a fixed sequence of analytical passes.
3. Separate source evidence, interpretation, inference, and unresolved questions.
4. Write every model response as an immutable JSONL record.
5. Produce a consolidated run summary.

The harness is deliberately not an autonomous agent swarm. Passes do not overwrite one another.

## Layout

```text
src/nerf_harness/
  cli.py
  schema.py
  prompts.py
  runner.py
samples/
runs/
```

## Run

```bash
nerf run samples/nollidruj-006.txt --model gpt-4.1-mini --repeat 3
```

Each run writes `records.jsonl` and `summary.json`.

## Passes

- `extractor` — explicit statements and metadata only
- `categorizer` — categories and confidence
- `relationship_mapper` — internal relationships only
- `claim_checker` — evidence / interpretation / inference / unresolved
- `critic` — unsupported claims and overreach
- `synthesizer` — structured research card

## Record rule

Every substantive output carries artifact ID, run ID, pass name, model, prompt version, input hash, timestamp, and structured output.

**The model is not the source of truth. The artifact is.**
