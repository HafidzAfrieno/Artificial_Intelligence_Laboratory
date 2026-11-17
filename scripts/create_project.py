import json
import re
import sys
from pathlib import Path

from cookiecutter.main import cookiecutter


# ==========================================
# PATH CONFIGURATION
# ==========================================

ROOT_DIR = Path(__file__).resolve().parent.parent

TEMPLATE_DIR = ROOT_DIR / "templates" / "machine-learning"
OUTPUT_DIR = ROOT_DIR / "projects" / "machine-learning"


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def create_project_slug(project_name: str) -> str:
    """Convert project name into a normalized slug."""

    slug = project_name.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)

    return slug.strip("-")


def create_project_name(project_slug: str) -> str:
    """Convert project slug into a readable project name."""

    return project_slug.replace("-", " ").title()


# ==========================================
# MACHINE LEARNING PROJECT
# ==========================================

def create_machine_learning_project(project_input: str):

    project_slug = create_project_slug(project_input)

    if not project_slug:
        raise ValueError("Nama project tidak boleh kosong.")

    project_name = create_project_name(project_slug)

    project_path = OUTPUT_DIR / project_slug

    if project_path.exists():
        raise FileExistsError(
            f"Project '{project_slug}' sudah tersedia."
        )

    # ==========================================
    # LOAD COOKIECUTTER CONFIGURATION
    # ==========================================

    config_path = TEMPLATE_DIR / "cookiecutter.json"

    with open(config_path, "r", encoding="utf-8") as file:
        context = json.load(file)

    # ==========================================
    # UPDATE PROJECT CONFIGURATION
    # ==========================================

    context.update({
        "project_name": project_name,
        "project_slug": project_slug
    })

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # ==========================================
    # GENERATE PROJECT
    # ==========================================

    cookiecutter(
        template=str(TEMPLATE_DIR),
        output_dir=str(OUTPUT_DIR),
        extra_context=context,
        no_input=True
    )

    print("\n" + "=" * 45)
    print("       PROJECT CREATED SUCCESSFULLY")
    print("=" * 45)
    print(f"Project Name : {project_name}")
    print(f"Project Slug : {project_slug}")
    print(f"Location     : {project_path}")
    print("=" * 45)


# ==========================================
# MAIN
# ==========================================

def main():

    if len(sys.argv) != 3:
        print(
            "\nUsage:"
            "\npython scripts/create_project.py "
            "machine-learning <project-name>"
        )
        sys.exit(1)

    project_type = sys.argv[1]
    project_input = sys.argv[2]

    if project_type != "machine-learning":
        print(f"Project type '{project_type}' belum tersedia.")
        sys.exit(1)

    if not TEMPLATE_DIR.exists():
        print(f"Template tidak ditemukan: {TEMPLATE_DIR}")
        sys.exit(1)

    try:
        create_machine_learning_project(project_input)

    except (ValueError, FileExistsError) as error:
        print(f"\nError: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
