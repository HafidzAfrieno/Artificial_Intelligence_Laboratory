import re
import sys

slug = "{{cookiecutter.project_slug}}"

if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
    print("Project slug must use kebab-case.")
    sys.exit(1)