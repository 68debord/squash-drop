from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


EVIDENCE_TYPES = (
    "source_evidence",
    "interpretation",
    "inference",
    "unresolved",
)


@dataclass
class PassRecord:
    run_id: str
    artifact_id: str
    pass_name: str
    model: str
    prompt_version: str
    input_hash: str
    timestamp: str
    output: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(cls, **kwargs: Any) -> "PassRecord":
        return cls(
            timestamp=datetime.now(timezone.utc).isoformat(),
            **kwargs,
        )

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, sort_keys=True)
