import argparse
import file_io
from game import game_create

def build_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(prog="quiz")
  parser.add_argument("-q", "--questions_path", type=str, default="quizzes/pytania.txt")
  return parser

def main(argv: list[str] | None = None):
  parser = build_parser()
  args = parser.parse_args(argv)
  try:
    questions, err = file_io.load_questions(args.questions_path)
  except OSError:
    print("ERROR: Failed to open questions file: ", args.questions_path)
    exit(1)
  
  if err != None:
    print("ERROR: ", err)
    exit(1)
  
  game = game_create(questions)
  game["play"]()

if __name__ == "__main__":
  main()