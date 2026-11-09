import pytest
from question import question_create


@pytest.mark.parametrize("correct", ["A", "B", "C", "D"])
def test_question_lifeline_keeps_two_sorted_answers(correct):
  lines = [
    ("Q", "Treść?"),
    ("A", "Odp A"),
    ("B", "Odp B"),
    ("C", "Odp C"),
    ("D", "Odp D"),
    ("S", correct),
  ]
  q = question_create(lines)
  q["use_lifeline"]()
  answers = q["get_answers"]()

  assert len(answers) == 2
  assert correct in answers
  assert list(answers.keys()) == sorted(answers.keys())
