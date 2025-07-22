from inspect_ai import Task, task
from inspect_ai.dataset import FieldSpec, json_dataset
from inspect_ai.solver import multiple_choice  # asks model to pick a letter
from inspect_ai.scorer import choice


@task
def aws_solutions_architect():
    """
    Evaluates basic AWS Solutions-Architect multiple-choice questions.
    • Works with *either* single-answer targets
      (e.g.  "B") *or* multi-answer targets
      (e.g. ["B","D"]).

    • Add new questions to aws_sa.jsonl; no other
      changes are required.
    """
    dataset = json_dataset(
        "aws_sa.jsonl",
        sample_fields=FieldSpec(
            input="input",
            choices="choices",
            target="target",
        ),
        auto_id=True,
        shuffle=True,
        shuffle_choices=True,
    )

    return Task(
        dataset=dataset,
        solver=[multiple_choice(multiple_correct=True)],  # <-- key change
        scorer=choice(),  # handles lists automatically
    )
