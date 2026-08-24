from __future__ import annotations

import hashlib
import json
import re
import uuid
from pathlib import Path
from typing import Any

from openai import OpenAI

from .prompts import PASSES
from .schema import PassRecord


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def parse_json(text: str) -> dict[str, Any]:
    """Parse model JSON while tolerating common Markdown code fences.

    The harness asks for JSON-only output, but models may still wrap otherwise
    valid JSON in ```json ... ``` fences. Preserve a parse error only after
    trying the raw text, a fenced block, and a decodable JSON object/array
    embedded in surrounding whitespace or prose.
    """
    candidates = [text.strip()]

    fenced = re.fullmatch(
        r"\s*```(?:json)?\s*\n?(.*?)\n?```\s*",
        text,
        re.DOTALL | re.IGNORECASE,
    )
    if fenced:
        candidates.append(fenced.group(1).strip())

    for candidate in candidates:
        try:
            value = json.loads(candidate)
            return value if isinstance(value, dict) else {"raw": value}
        except json.JSONDecodeError:
            pass

    # Last resort: recover the first complete JSON value from surrounding text.
    decoder = json.JSONDecoder()
    for index, char in enumerate(text):
        if char not in "{[":
            continue
        try:
            value, _ = decoder.raw_decode(text[index:])
            return value if isinstance(value, dict) else {"raw": value}
        except json.JSONDecodeError:
            continue

    return {"raw": text, "parse_error": True}


def run_artifact(
    artifact_path: str | Path,
    model: str,
    repeat: int = 1,
    output_root: str | Path = "runs",
) -> Path:
    artifact_path = Path(artifact_path)
    artifact = artifact_path.read_text(encoding="utf-8")
    artifact_id = artifact_path.stem
    input_hash = sha256(artifact)
    run_id = f"nerf-{uuid.uuid4().hex[:12]}"
    run_dir = Path(output_root) / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    records_path = run_dir / "records.jsonl"

    client = OpenAI()
    summary: list[dict[str, Any]] = []

    with records_path.open("a", encoding="utf-8") as log:
        for iteration in range(repeat):
            prior_outputs: dict[str, Any] = {}
            for pass_name, spec in PASSES.items():
                context = json.dumps(prior_outputs, ensure_ascii=False)
                user_content = (
                    f"ARTIFACT ID: {artifact_id}\n\n"
                    f"ARTIFACT:\n{artifact}\n\n"
                    f"PRIOR PASS OUTPUTS:\n{context}\n\n"
                    "Return valid JSON only."
                )
                response = client.responses.create(
                    model=model,
                    instructions=spec["instruction"],
                    input=user_content,
                )
                output = parse_json(response.output_text)
                prior_outputs[pass_name] = output
                record = PassRecord.create(
                    run_id=run_id,
                    artifact_id=artifact_id,
                    pass_name=f"{pass_name}:{iteration + 1}",
                    model=model,
                    prompt_version=spec["version"],
                    input_hash=input_hash,
                    output=output,
                )
                log.write(record.to_json() + "\n")
                log.flush()
                summary.append(json.loads(record.to_json()))

    (run_dir / "summary.json").write_text(
        json.dumps(
            {
                "run_id": run_id,
                "artifact_id": artifact_id,
                "artifact_path": str(artifact_path),
                "model": model,
                "repeat": repeat,
                "input_hash": input_hash,
                "records": summary,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return run_dir
