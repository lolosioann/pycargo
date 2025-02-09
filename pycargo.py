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
        subprocess.run(["git", "init", project_name], stdout=subprocess.DEVNULL, check=True)
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
    subprocess.run(["python", "-m", "venv", venv_path], stdout=subprocess.DEVNULL, check=True)
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
    subprocess.run(["pip", "install", "pre-commit"], stdout=subprocess.DEVNULL, check=True)
    subprocess.run(["pre-commit", "install"], stdout=subprocess.DEVNULL, check=True)

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
import os
import subprocess
import click

@click.group()
def cli():
    """PyCargo: A CLI tool for streamlining Python project development."""
    pass

@click.command()
@click.argument("project_name")
def new(project_name):
    """Create a new Python project."""
    click.echo(click.style(f"🚀 Creating new Python project: {project_name}", fg="cyan", bold=True))

    # Create project structure
    try:
        os.makedirs(f"{project_name}")
    except FileExistsError:
        click.echo(click.style("⚠️ Project already exists.", fg="yellow"))
        return
    
    os.makedirs(f"{project_name}/src/")
    os.makedirs(f"{project_name}/tests/")

    # Create main.py
    with open(f"{project_name}/src/main.py", "w") as f:
        f.write("def main():\n    print('Hello, world!')\n\nif __name__ == '__main__':\n    main()\n")

    # Initialize Git
    try:
        subprocess.run(["git", "init", project_name], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        click.echo(click.style("✅ Git repository initialized!", fg="green"))
    except subprocess.CalledProcessError:
        click.echo(click.style("❌ Git initialization failed. Is Git installed?", fg="red"), err=True)
        return
    
    # Create README.md
    with open(f"{project_name}/README.md", "w") as f:
        f.write(f"# {project_name}\n")
    # Create .gitignore
    with open(f"{project_name}/.gitignore", "w") as f:
        f.write("*.pyc\n__pycache__/\n.venv/\n")

    # Create virtual environment
    venv_path = os.path.join(project_name, ".venv")
    subprocess.run(["python", "-m", "venv", venv_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Determine correct Python executable inside .venv
    python_exec = os.path.join(venv_path, "bin", "python")  # Linux/macOS
    if os.name == "nt":  # Windows
        python_exec = os.path.join(venv_path, "Scripts", "python.exe")

    # Create requirements.txt
    with open(f"{project_name}/requirements.txt", "w") as f:
        f.write("pytest\npre-commit\nblack\nisort\n")

    # Generate pyproject.toml
    pyproject_content = """\
[tool.black]
line-length = 88

[tool.isort]
profile = "black"

[tool.ruff]
extend-ignore = ["E203", "W503"]
"""
    with open(f"{project_name}/pyproject.toml", "w") as f:
        f.write(pyproject_content)

    # Generate .pre-commit-config.yaml
    precommit_content = """\
repos:
  - repo: https://github.com/psf/black
    rev: stable
    hooks:
      - id: black

  - repo: https://github.com/pycqa/isort
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

    # Install dependencies inside the virtual environment
    subprocess.run([python_exec, "-m", "pip", "install", "-r", f"{project_name}/requirements.txt"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Initialize and enable pre-commit inside project directory
    subprocess.run([python_exec, "-m", "pre-commit", "install"], cwd=project_name, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    click.echo(click.style("🎉 Project created successfully!", fg="magenta", bold=True))


@click.command()
def run():
    """Run the project."""
    if not os.path.exists("src/main.py"):
        click.echo(click.style("❌ No src/main.py found!", fg="red"))
        return
    
    python_exec = os.path.join(".venv", "bin", "python") if os.name != "nt" else os.path.join(".venv", "Scripts", "python.exe")

    click.echo(click.style("🚀 Running the project...", fg="cyan"))
    subprocess.run([python_exec, "src/main.py"])


@click.command()
def test():
    """Run tests using pytest."""
    if not os.path.exists("tests/"):
        click.echo(click.style("⚠️ No tests found!", fg="yellow"))
        return

    python_exec = os.path.join(".venv", "bin", "python") if os.name != "nt" else os.path.join(".venv", "Scripts", "python.exe")

    click.echo(click.style("🧪 Running tests...", fg="blue"))
    subprocess.run([python_exec, "-m", "pytest", "tests/"])


@click.command()
def install():
    """Install dependencies from requirements.txt."""
    if not os.path.exists("requirements.txt"):
        click.echo(click.style("❌ No requirements.txt found!", fg="red"))
        return

    python_exec = os.path.join(".venv", "bin", "python") if os.name != "nt" else os.path.join(".venv", "Scripts", "python.exe")

    click.echo(click.style("📦 Installing dependencies...", fg="green"))
    subprocess.run([python_exec, "-m", "pip", "install", "-r", "requirements.txt"])


@click.command()
def fmt():
    """Format code using black and isort."""
    click.echo(click.style("🖌 Formatting code...", fg="yellow"))
    subprocess.run(["black", "src/", "tests/"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["isort", "src/", "tests/"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    click.echo(click.style("✅ Code formatted!", fg="green"))


@click.command()
def check():
    """Run linting checks using ruff."""
    click.echo(click.style("🔍 Checking code with ruff...", fg="blue"))
    result = subprocess.run(["ruff", "check", "src/", "tests/"], capture_output=True, text=True)

    if result.returncode == 0:
        click.echo(click.style("✅ No issues found!", fg="green", bold=True))
    else:
        click.echo(click.style("❌ Issues found:", fg="red", bold=True))
        click.echo(result.stdout)



# Add commands to CLI
cli.add_command(new)
cli.add_command(run)
cli.add_command(test)
cli.add_command(install)
cli.add_command(fmt)
cli.add_command(check)

if __name__ == "__main__":
    cli()
