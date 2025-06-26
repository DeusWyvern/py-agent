from functions.run_python_file import run_python_file
from functions.write_file import write_file


def tests():
    print(run_python_file("calculator", "main.py"))
    print(run_python_file("calculator", "tests.py"))
    print(run_python_file("calculator", "../main.py"))
    print(run_python_file("calculator", "nonexistent.py"))

    print(write_file("calculator", "pkg/test.txt", "lorem ipsum dolor sit amet"))


if __name__ == "__main__":
    tests()
