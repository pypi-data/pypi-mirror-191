import inquirer
import subprocess

mirrors = [
    'https://pypi.org/simple'
    'https://pypi.tuna.tsinghua.edu.cn/simple',
    'https://pypi.mirrors.ustc.edu.cn/simple',
    'https://test.pypi.org/simple'
]

questions = [
    inquirer.List('mirror',
                  message="Which mirror do you want to use?",
                  choices=mirrors)
]

def main():
    answers = inquirer.prompt(questions)
    subprocess.run(["pip", "config", "set", "global.index-url", answers['mirror']])
