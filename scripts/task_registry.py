# ============================================================================
# Task Registry — Defines evaluation tracks and their scoring configuration
# ============================================================================
#
# Weight Distribution (must sum to 1.0):
#   - practice_exam:       0.34 (AWS certification-style MCQ knowledge)
#   - architecture_design: 0.33 (Architectural reasoning and diagram tasks)
#   - cdk_synth:           0.33 (Infrastructure-as-code generation)
#
# Equal weighting reflects that all three capabilities are important for
# a well-rounded Solutions Architect evaluation. Weights can be adjusted
# if certain tracks prove more differentiating or reliable.
# ============================================================================

TASKS = {
    "practice_exam": {
        "patterns": ["aws-solutions-architect", "practice_exam"],
        "metric": "choice",
        "pass_values": ["C"],
        "weight": 0.34,
    },
    "architecture_design": {
        "patterns": ["architecture-design", "architecture-interpretation"],
        "metric": "architecture_scorer",
        "weight": 0.33,
    },
    "cdk_synth": {
        "patterns": ["aws-cdk-synth", "aws_cdk_synth", "cdk_synth"],
        "metric": "cdk_verify",
        "pass_values": ["C"],
        "weight": 0.33,
    },
}
