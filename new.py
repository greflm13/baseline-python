#!/usr/bin/env python
import os
import readline
from subprocess import run

import tomlkit

readline.set_startup_hook()
try:
    name = input("Project Name: ")
    name = name.replace(" ", "-").lower()
    description = input("Description: ")
    python_version = input("Python Version: ")
    author = input("Author: ")
    setup_virtualenv = input("Setup pyenv virtualenv? [Y/n]: ").strip().lower() in ("", "y", "yes")
finally:
    readline.set_startup_hook()

run(["git", "clone", "https://github.com/greflm13/baseline-python", name])
run(["rm", "-rf", os.path.join(name, ".git")])

path = os.path.join(name, "pyproject.toml")
with open(path, encoding="utf-8") as f:
    pyproject = tomlkit.loads(f.read())

pyproject["project"]["name"] = name
pyproject["project"]["description"] = description
pyproject["project"]["requires-python"] = f">={python_version}"
pyproject["project"]["authors"] = tomlkit.array()
authors = tomlkit.inline_table()
authors.add("name", author)
pyproject["project"]["authors"].append(authors)
pyproject["project"]["scripts"] = tomlkit.table()
pyproject["project"]["scripts"].add(name, "main:main")
pyproject["tool"]["setuptools"]["package-data"] = tomlkit.table()
pyproject["tool"]["setuptools"]["package-data"].add(name, tomlkit.array())
pyproject["tool"]["ruff"]["target-version"] = f"py{python_version.replace('.', '')}"

with open(path, "w", encoding="utf-8") as f:
    f.write(tomlkit.dumps(pyproject))

if setup_virtualenv:
    run(["pyenv", "install", python_version])
    run(["pyenv", "virtualenv", python_version, name])

with open(os.path.join(name, ".python-version"), "w", encoding="utf-8") as f:
    if setup_virtualenv:
        f.write(name)
    else:
        f.write(python_version)

run(["git", "init"], cwd=name)
