PASSES = {
    "extractor": {
        "version": "extractor-v1",
        "instruction": """Extract only what is explicitly present in the artifact. Do not add outside knowledge. Return JSON with metadata, explicit_claims, quoted_evidence, and ambiguities. Quotes must be short and traceable.""",
    },
    "categorizer": {
        "version": "categorizer-v1",
        "instruction": """Classify the artifact using evidence from the artifact. Return JSON with primary_category, secondary_categories, confidence, and rationale. Distinguish classification from fact claims.""",
    },
    "relationship_mapper": {
        "version": "relationship-mapper-v1",
        "instruction": """Map relationships explicitly supported inside the artifact. Return JSON with entities, relationships, evidence, and unresolved_relationships. Do not invent external connections.""",
    },
    "claim_checker": {
        "version": "claim-checker-v1",
        "instruction": """Separate analytical statements into source_evidence, interpretation, inference, and unresolved. For every item, provide supporting text or say support is absent. Prefer uncertainty to invention.""",
    },
    "critic": {
        "version": "critic-v1",
        "instruction": """Audit the preceding analysis for unsupported claims, overconfident inference, provenance loss, category mistakes, and omitted ambiguity. Return JSON. Do not silently repair errors: report them.""",
    },
    "synthesizer": {
        "version": "synthesizer-v1",
        "instruction": """Produce a structured research card using only the artifact and prior pass outputs. Keep source evidence, interpretation, inference, and unresolved questions visibly separate.""",
    },
}
