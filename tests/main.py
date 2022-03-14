import subprocess


def main():
    subprocess.run(["poetry", "run", "pytest"])
