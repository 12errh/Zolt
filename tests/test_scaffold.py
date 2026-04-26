"""Phase 6 — pyui new scaffold tests."""

from __future__ import annotations

from pathlib import Path


def test_scaffold_blank_creates_files(tmp_path: Path) -> None:
    import os
    from pyui.scaffold import create_project

    os.chdir(tmp_path)
    project = create_project("my-app", template="blank")

    assert (project / "app.py").exists()
    assert (project / "requirements.txt").exists()
    assert (project / "README.md").exists()


def test_scaffold_app_py_is_valid_python(tmp_path: Path) -> None:
    import ast, os
    from pyui.scaffold import create_project

    os.chdir(tmp_path)
    project = create_project("test-app", template="blank")
    source = (project / "app.py").read_text(encoding="utf-8")
    ast.parse(source)  # raises SyntaxError if invalid


def test_scaffold_dashboard_template(tmp_path: Path) -> None:
    import os
    from pyui.scaffold import create_project

    os.chdir(tmp_path)
    project = create_project("my-dash", template="dashboard")
    source = (project / "app.py").read_text(encoding="utf-8")
    assert "DashboardPage" in source
    assert "Table" in source


def test_scaffold_class_name_from_project_name(tmp_path: Path) -> None:
    import os
    from pyui.scaffold import create_project

    os.chdir(tmp_path)
    project = create_project("cool-project", template="blank")
    source = (project / "app.py").read_text(encoding="utf-8")
    assert "CoolProjectApp" in source


def test_scaffold_existing_dir_raises(tmp_path: Path) -> None:
    import os
    from pyui.scaffold import create_project

    os.chdir(tmp_path)
    create_project("existing", template="blank")
    try:
        create_project("existing", template="blank")
        assert False, "Should have raised FileExistsError"
    except FileExistsError:
        pass


def test_scaffold_requirements_has_pyui(tmp_path: Path) -> None:
    import os
    from pyui.scaffold import create_project

    os.chdir(tmp_path)
    project = create_project("req-test", template="blank")
    reqs = (project / "requirements.txt").read_text(encoding="utf-8")
    assert "zolt" in reqs
