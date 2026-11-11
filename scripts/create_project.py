
import argparse
import re
import sys
import traceback
from pathlib import Path

from cookiecutter.main import cookiecutter
from cookiecutter.exceptions import CookiecutterException


# ==========================================
# PROJECT CONFIGURATION
# ==========================================

ROOT_DIR = Path(__file__).resolve().parent.parent

TEMPLATE_DIR = ROOT_DIR / "templates" / "ai-project-template"

PROJECT_TYPES = {
    "machine-learning": [
        "classification",
        "regression",
        "clustering"
    ],
    "deep-learning": [
        "computer-vision",
        "nlp",
        "neural-networks"
    ],
    "generative-ai": [
        "llm",
        "rag",
        "ai-agents",
        "fine-tuning"
    ],
    "ai-engineering": [
        "mlops",
        "data-pipeline",
        "model-monitoring"
    ]
}


# ==========================================
# DEPENDENCY CONFIGURATION
# ==========================================

BACKEND_DEPENDENCIES = [
    "fastapi",
    "uvicorn[standard]",
    "pydantic",
    "python-dotenv",
    "huggingface_hub"
]


DEPENDENCY_CONFIG = {

    # MACHINE LEARNING
    "machine-learning": {

        "classification": {
            "scikit-learn": [
                "numpy",
                "pandas",
                "scikit-learn",
                "matplotlib",
                "seaborn",
                "joblib"
            ],
            "xgboost": [
                "numpy",
                "pandas",
                "scikit-learn",
                "xgboost",
                "joblib"
            ]
        },

        "regression": {
            "scikit-learn": [
                "numpy",
                "pandas",
                "scikit-learn",
                "matplotlib",
                "seaborn",
                "joblib"
            ],
            "xgboost": [
                "numpy",
                "pandas",
                "scikit-learn",
                "xgboost",
                "joblib"
            ]
        },

        "clustering": {
            "scikit-learn": [
                "numpy",
                "pandas",
                "scikit-learn",
                "matplotlib",
                "seaborn",
                "joblib"
            ]
        }
    },

    # DEEP LEARNING
    "deep-learning": {

        "computer-vision": {
            "pytorch": [
                "numpy",
                "pandas",
                "torch",
                "torchvision",
                "pillow",
                "matplotlib"
            ],
            "tensorflow": [
                "numpy",
                "pandas",
                "tensorflow",
                "pillow",
                "matplotlib"
            ]
        },

        "nlp": {
            "pytorch": [
                "numpy",
                "pandas",
                "torch",
                "transformers",
                "datasets",
                "tokenizers"
            ],
            "tensorflow": [
                "numpy",
                "pandas",
                "tensorflow",
                "transformers",
                "datasets"
            ]
        },

        "neural-networks": {
            "pytorch": [
                "numpy",
                "torch",
                "matplotlib"
            ],
            "tensorflow": [
                "numpy",
                "tensorflow",
                "matplotlib"
            ]
        }
    },

    # GENERATIVE AI
    "generative-ai": {

        "llm": {
            "transformers": [
                "torch",
                "transformers",
                "accelerate",
                "huggingface_hub",
                "sentencepiece"
            ]
        },

        "rag": {
            "langchain": [
                "langchain",
                "langchain-community",
                "langchain-text-splitters",
                "sentence-transformers",
                "faiss-cpu"
            ]
        },

        "ai-agents": {
            "langchain": [
                "langchain",
                "langchain-community",
                "langgraph"
            ]
        },

        "fine-tuning": {
            "transformers": [
                "torch",
                "transformers",
                "datasets",
                "accelerate",
                "peft",
                "trl"
            ]
        }
    },

    # AI ENGINEERING
    "ai-engineering": {

        "mlops": {
            "mlflow": [
                "mlflow",
                "scikit-learn",
                "pandas",
                "joblib"
            ]
        },

        "data-pipeline": {
            "pandas": [
                "pandas",
                "numpy",
                "pyarrow"
            ]
        },

        "model-monitoring": {
            "evidently": [
                "evidently",
                "pandas",
                "scikit-learn"
            ]
        }
    }
}


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def slugify(name):
    """Mengubah nama project menjadi format kebab-case."""

    slug = re.sub(
        r"[^a-z0-9]+",
        "-",
        name.strip().lower()
    )

    return slug.strip("-")


def validate_template():
    """Memastikan template Cookiecutter tersedia."""

    if not TEMPLATE_DIR.is_dir():
        raise FileNotFoundError(
            f"Template tidak ditemukan: {TEMPLATE_DIR}"
        )

    cookiecutter_config = TEMPLATE_DIR / "cookiecutter.json"

    if not cookiecutter_config.is_file():
        raise FileNotFoundError(
            f"cookiecutter.json tidak ditemukan: {cookiecutter_config}"
        )


def validate_project(args):
    """Memvalidasi konfigurasi project."""

    if not args.name.strip():
        raise ValueError("Nama project tidak boleh kosong.")

    if args.category not in PROJECT_TYPES:
        raise ValueError(f"Kategori tidak valid: {args.category}")

    if args.type not in PROJECT_TYPES[args.category]:
        raise ValueError(
            f"Tipe '{args.type}' tidak tersedia "
            f"untuk kategori '{args.category}'."
        )

    if not args.framework.strip():
        raise ValueError("Framework tidak boleh kosong.")

    if not args.author.strip():
        raise ValueError("Nama author tidak boleh kosong.")

    if not args.python_version.strip():
        raise ValueError("Versi Python tidak boleh kosong.")

    project_slug = slugify(args.name)

    if not project_slug:
        raise ValueError("Nama project menghasilkan slug kosong.")

    return project_slug


def get_dependencies(category, project_type, framework):
    """
    Mengambil dependency berdasarkan kategori,
    tipe project, dan framework.
    """

    try:
        dependencies = DEPENDENCY_CONFIG[
            category
        ][project_type][framework]

    except KeyError:
        raise ValueError(
            f"Framework '{framework}' belum didukung "
            f"untuk kategori '{category}' "
            f"dengan tipe '{project_type}'."
        )

    return sorted(set(dependencies))


def generate_requirements(project_dir, dependencies):
    """
    Membuat requirements.txt secara otomatis
    untuk backend dan model.
    """

    backend_dir = project_dir / "backend"
    model_dir = project_dir / "model"

    # Pastikan folder tersedia
    if not backend_dir.is_dir():
        raise FileNotFoundError(
            f"Folder backend tidak ditemukan: {backend_dir}"
        )

    if not model_dir.is_dir():
        raise FileNotFoundError(
            f"Folder model tidak ditemukan: {model_dir}"
        )

    # Backend requirements
    backend_requirements = backend_dir / "requirements.txt"

    backend_requirements.write_text(
        "\n".join(BACKEND_DEPENDENCIES) + "\n",
        encoding="utf-8"
    )

    # Model requirements
    model_requirements = model_dir / "requirements.txt"

    model_requirements.write_text(
        "\n".join(dependencies) + "\n",
        encoding="utf-8"
    )

    print("\nDEPENDENCIES GENERATED")

    print("\nBackend:")
    for dependency in BACKEND_DEPENDENCIES:
        print(f"  - {dependency}")

    print("\nModel:")
    for dependency in dependencies:
        print(f"  - {dependency}")


# ==========================================
# PROJECT GENERATOR
# ==========================================

def create_project(args):

    # 1. Validate template
    validate_template()

    # 2. Validate project configuration
    project_slug = validate_project(args)

    category = args.category
    project_type = args.type
    framework = args.framework.strip().lower()

    # 3. Get project dependencies
    dependencies = get_dependencies(
        category,
        project_type,
        framework
    )

    # 4. Determine output directory
    output_dir = (
        ROOT_DIR
        / "projects"
        / category
        / project_type
    )

    project_dir = output_dir / project_slug

    # 5. Prevent duplicate project
    if project_dir.exists():
        raise FileExistsError(
            f"Project sudah ada:\n{project_dir}\n"
            "Gunakan nama lain atau periksa folder tersebut terlebih dahulu."
        )

    # 6. Create parent directory
    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # 7. Cookiecutter context
    context = {
        "project_name": args.name.strip(),
        "project_slug": project_slug,
        "project_description": args.description,
        "author_name": args.author,
        "category": category,
        "project_type": project_type,
        "model_framework": framework,
        "huggingface_model_id": args.huggingface_model_id,
        "python_version": args.python_version
    }

    # 8. Generate project
    result = cookiecutter(
        str(TEMPLATE_DIR),
        output_dir=str(output_dir),
        extra_context=context,
        no_input=True
    )

    # 9. Generate requirements files
    generate_requirements(
        Path(result),
        dependencies
    )

    # 10. Success message
    print("\n" + "=" * 45)
    print("       PROJECT CREATED SUCCESSFULLY")
    print("=" * 45)

    print(f"Project Name : {args.name}")
    print(f"Category     : {category}")
    print(f"Project Type : {project_type}")
    print(f"Framework    : {framework}")
    print(f"Location     : {result}")

    print("\nNext steps:")
    print("1. Masuk ke folder project.")
    print("2. Periksa file .env.example.")
    print("3. Install dependencies backend dan model.")
    print("4. Jalankan pengujian.")
    print("5. Jalankan Docker Compose jika diperlukan.")

    return result


# ==========================================
# CLI
# ==========================================

def main():

    parser = argparse.ArgumentParser(
        description="AI Engineering Lab Project Generator"
    )

    parser.add_argument(
        "--name",
        required=True,
        help="Nama project"
    )

    parser.add_argument(
        "--category",
        required=True,
        choices=PROJECT_TYPES.keys(),
        help="Kategori project"
    )

    parser.add_argument(
        "--type",
        required=True,
        help="Tipe project"
    )

    parser.add_argument(
        "--framework",
        default="scikit-learn",
        help="Framework yang digunakan"
    )

    parser.add_argument(
        "--description",
        default="AI-powered application",
        help="Deskripsi project"
    )

    parser.add_argument(
        "--author",
        default="AI Engineering Lab",
        help="Nama author"
    )

    parser.add_argument(
        "--huggingface-model-id",
        default="",
        help="Hugging Face Model ID"
    )

    parser.add_argument(
        "--python-version",
        default="3.11",
        help="Versi Python"
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Menampilkan traceback ketika terjadi error"
    )

    args = parser.parse_args()

    try:
        create_project(args)

    except FileExistsError as error:
        print(f"\n[ERROR] {error}", file=sys.stderr)
        sys.exit(1)

    except (ValueError, FileNotFoundError) as error:
        print(f"\n[ERROR] {error}", file=sys.stderr)
        sys.exit(1)

    except CookiecutterException as error:
        print(
            f"\n[ERROR] Cookiecutter gagal: {error}",
            file=sys.stderr
        )

        if args.debug:
            traceback.print_exc()

        sys.exit(1)

    except Exception as error:
        print(
            f"\n[ERROR] Terjadi kesalahan: {error}",
            file=sys.stderr
        )

        if args.debug:
            traceback.print_exc()

        sys.exit(1)


if __name__ == "__main__":
    main()
