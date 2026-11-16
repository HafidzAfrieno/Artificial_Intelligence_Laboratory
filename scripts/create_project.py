
from pathlib import Path
import sys
from cookiecutter.main import cookiecutter
from cookiecutter.exceptions import OutputDirExistsException

ROOT = Path(__file__).resolve().parent.parent

def create_project(category, project_name):

    template = ROOT / "templates" / category
    output = ROOT / "projects" / category
    project_dir = output / project_name

    # Validasi template
    if not template.exists():
        print("Kategori atau template tidak ditemukan.")
        return

    # Validasi project sudah ada
    if project_dir.exists():
        print("Project sudah ada.")
        return

    try:
        cookiecutter(
            str(template),
            output_dir=str(output),
            no_input=True,
            extra_context={"project_slug": project_name}
        )

        print(f"Project berhasil dibuat: {project_dir}")

    except OutputDirExistsException:
        print("Project sudah ada.")

    except Exception as error:
        print(f"Terjadi kesalahan: {error}")


if __name__ == "__main__":

    # Validasi command
    if len(sys.argv) != 3:
        print("Command ada yang salah!")
        print("Format: python scripts/create_project.py <kategori> <nama-project>")
        sys.exit(1)

    category, project_name = sys.argv[1:3]

    create_project(category, project_name)
