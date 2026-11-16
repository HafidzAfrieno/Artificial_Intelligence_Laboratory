
from pathlib import Path
import sys
import os
import subprocess

from cookiecutter.main import cookiecutter
from cookiecutter.exceptions import OutputDirExistsException


ROOT = Path(__file__).resolve().parent.parent

def check_environment():

    # Deteksi Conda atau Virtual Environment
    is_conda = (
        bool(os.environ.get("CONDA_PREFIX"))
        or "conda" in sys.executable.lower()
    )

    is_venv = (
        bool(os.environ.get("VIRTUAL_ENV"))
        or sys.prefix != sys.base_prefix
    )

    if not (is_conda or is_venv):
        print("Tidak ada environment Python yang aktif.")
        print("Silakan aktifkan Conda atau Virtual Environment terlebih dahulu.")
        print(f"Python yang digunakan: {sys.executable}")
        return False

    print("\nEnvironment terdeteksi:")
    print(f"Python: {sys.executable}")

    if is_conda:
        print(f"Conda: {os.environ.get('CONDA_PREFIX', sys.prefix)}")
    elif is_venv:
        print(f"Virtual Environment: {os.environ.get('VIRTUAL_ENV', sys.prefix)}")

    return True



def install_project(project_dir):

    print("\nMenginstal project dan dependencies...")

    try:
        # Perintah instalasi package project
        command = [
            sys.executable,
            "-m",
            "pip",
            "install",
            "-e",
            "."
        ]

        # Tambahkan requirements.txt jika tersedia
        requirements = project_dir / "requirements.txt"

        if requirements.exists():
            command.extend(["-r", "requirements.txt"])

        subprocess.run(
            command,
            cwd=project_dir,
            check=True
        )

        print("\nProject berhasil diinstal!")

    except subprocess.CalledProcessError:
        print("\nProject berhasil dibuat, tetapi instalasi gagal.")
        print("Silakan periksa konfigurasi pyproject.toml atau requirements.txt.")


def create_project(category, project_name):

    # Validasi environment
    if not check_environment():
        return

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

        print(f"\nProject berhasil dibuat: {project_dir}")

        # Instalasi otomatis
        install_project(project_dir)

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
