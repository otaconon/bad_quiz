import pytest
import file_io

VALID_QUESTION = (
  "Q\tIle zasad azotowych występuje w DNA?\n"
  "A\t2\n"
  "B\t3\n"
  "C\t4\n"
  "D\t5\n"
  "S\tC\n"
)

@pytest.fixture(autouse=True)
def reset_parser_state():
  if hasattr(file_io, "expected_indicator_idx"):
    #file_io.expected_indicator_idx = 0
    pass


def test_load_questions_valid(tmp_path):
  p = tmp_path / "pytania.txt"
  p.write_text(VALID_QUESTION, encoding="utf-8")
  questions, err = file_io.load_questions(p)
  assert err is None
  assert len(questions) == 1
  assert questions[0]["get_correct_answer"]() == "C"


@pytest.mark.parametrize("bad_content, expected_err", [
  # Brak odpowiedzi C (od razu D)
  ("Q\tPyt\nA\t1\nB\t2\nD\t4\nS\tA\n", "MISSING_ANSWER"),
  # Zbyt duża liczba odpowiedzi (dodatkowa linia E zamiast S)
  ("Q\tPyt\nA\t1\nB\t2\nC\t3\nD\t4\nE\t5\nS\tA\n", "INVALID_LINE_INDICATOR"),
  # Brak informacji o poprawnej odpowiedzi (nowe pytanie zamiast S)
  ("Q\tPyt\nA\t1\nB\t2\nC\t3\nD\t4\nQ\tPyt2\n", "MISSING_CORRECT_ANSWER"),
  # Niepoprawne oznaczenie linii
  ("X\tPyt\nA\t1\nB\t2\nC\t3\nD\t4\nS\tA\n", "INVALID_LINE_INDICATOR"),
  # Poprawna odpowiedź spoza A, B, C, D
  ("Q\tPyt\nA\t1\nB\t2\nC\t3\nD\t4\nS\tE\n", "INVALID_CORRECT_ANSWER"),
  # Urwany plik (mniej niż 6 linii)
  ("Q\tPyt\nA\t1\nB\t2\n", "MISSING_LINES"),
])

def test_load_questions_invalid_structure(tmp_path, bad_content, expected_err):
  p = tmp_path / "pytania.txt"
  p.write_text(bad_content, encoding="utf-8")
  questions, err = file_io.load_questions(p)
  assert questions == []
  assert err == expected_err


def test_load_questions_missing_tab_raises_value_error(tmp_path):
  p = tmp_path / "pytania.txt"
  p.write_text("Q Brak tabulatora\n", encoding="utf-8")
  with pytest.raises(ValueError):
    file_io.load_questions(p)
