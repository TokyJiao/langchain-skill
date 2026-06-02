import importlib
from pathlib import Path


def load_skills():
    skills = []

    base = Path("skills")

    for skill_dir in base.iterdir():
        if not skill_dir.is_dir():
            continue

        md_file = skill_dir / f"{skill_dir.name}.md"
        py_module = f"skills.{skill_dir.name}.{skill_dir.name}"

        # 读取 md
        description = md_file.read_text(encoding="utf-8")

        # import py
        module = importlib.import_module(py_module)

        skills.append({
            "name": skill_dir.name,
            "description": description,
            "func": module.run
        })

    return skills