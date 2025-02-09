import os
import subprocess
import click

@click.group
def cli():
    """PyCargo: A CLI tool for streamlining Python project development."""
    pass

@click.command
@click.argument('project_name')
def new(project_name):
    """Create a new Python project."""
    click.echo(click.style(f"🚀 Creating new Python project: {project_name}", fg="cyan", bold=True))

    # Create the project structure
    try:
        os.makedirs(f"{project_name}")
    except FileExistsError:
        click.echo("Project already exists.")
        return
    
    os.makedirs(f"{project_name}/src/")
    os.makedirs(f"{project_name}/tests/")

    # Create a main.py
    with open(f"{project_name}/main.py", "w") as f:
        f.write("def main():\n    print('Hello, world!')\n\nif __name__ == '__main__':\n    main()\n")

    # Initialize git
    try:
        subprocess.run(["git", "init", project_name], check=True)
    except subprocess.CalledProcessError:
        click.echo("❌ Git initialization failed. Is Git installed?", err=True)
        return
    
    # Create a README.md
    with open(f"{project_name}/README.md", "w") as f:
        f.write(f"# {project_name}\n")
    # Create a .gitignore
    with open(f"{project_name}/.gitignore", "w") as f:
        f.write("*.pyc\n__pycache__/\n")
    # TODO: Create a setup.py

    # Create a virtual environment
    venv_path = os.path.join(project_name, ".venv")
    subprocess.run(["python", "-m", "venv", venv_path], check=True)
    # Determine correct Python executable inside .venv
    python_exec = os.path.join(venv_path, "bin", "python")  # Linux/macOS
    if os.name == "nt":  # Windows
        python_exec = os.path.join(venv_path, "Scripts", "python.exe")
    with open(f"{project_name}/requirements.txt", "w") as f:
        f.write("""
pytest\n
pre-commit""")
    
    # Generate a standard pyproject.toml
    pyproject_content = f"""\
[tool.black]
line-length = 88

[tool.isort]
profile = "black"

[tool.ruff]
extend-ignore = ["E203", "W503"]
"""
    with open(f"{project_name}/pyproject.toml", "w") as f:
        f.write(pyproject_content)

    # generate a pre-commit config
    precommit_content = f"""\
repos:
  - repo: https://github.com/psf/black
    rev: stable
    hooks:
      - id: black

  - repo: https://github.com/PyCQA/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.3.0
    hooks:
      - id: ruff
"""
    with open(os.path.join(project_name, ".pre-commit-config.yaml"), "w") as f:
        f.write(precommit_content)

    # install and enable pre-commit
    subprocess.run(["pip", "install", "pre-commit"], check=True)
    subprocess.run(["pre-commit", "install"], check=True)

    click.echo("✅ Project created successfully.")

cli.add_command(new)
# cli.add_command(test)
# cli.add_command(run)

if __name__ == "__main__":
    cli()

# TODO: Add a command to run tests
# TODO: Add a command to run the project
# TODO: organize configuration into separate files
# TODO: hide the output of subprocess.run
# TODO: add a command to install dependencies
# TODO: add a command to format code
# TODO: add a command to lint code
# TODO: add a command to check code coverage
# TODO: figure out how to make the project a package
