TASKS = {
    "practice_exam": {
        "patterns": ["aws-solutions-architect", "practice_exam"],  # ALL aliases
        "metric": "choice",
        "pass_values": ["C"],  # <── use "C" for correct, same as CDK
        "weight": 0.4,
    },
    "architecture_design": {
        "patterns": ["architecture-design", "architecture-interpretation"],
        # The architecture tasks use a custom scorer named architecture_scorer
        # whose Score.value is already a rubric-normalized float in [0,1].
        "metric": "architecture_scorer",
        # No pass_values; treat the value directly as accuracy contribution.
        "weight": 0.6,
    },
    "cdk_synth": {
        "patterns": ["aws-cdk-synth", "cdk_synth"],
        "metric": "cdk_verify",
        "pass_values": ["C"],  # <── should be "C" for correct, not "P"
        "weight": 0.6,
    },
}
