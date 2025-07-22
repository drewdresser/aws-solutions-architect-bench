TASKS = {
    "practice_exam": {
        "patterns": ["aws-solutions-architect", "practice_exam"],  # ALL aliases
        "metric": "choice",
        "pass_values": ["C"],  # <── use "C" for correct, same as CDK
        "weight": 0.4,
    },
    "cdk_synth": {
        "patterns": ["aws-cdk-synth", "cdk_synth"],
        "metric": "cdk_verify",
        "pass_values": ["C"],  # <── should be "C" for correct, not "P"
        "weight": 0.6,
    },
}
