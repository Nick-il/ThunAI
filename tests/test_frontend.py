from pathlib import Path


def test_frontend_files_exist():
    root = Path(__file__).parents[1]
    assert (root / "frontend/index.html").is_file()
    assert (root / "frontend/styles.css").is_file()
    assert (root / "frontend/app.js").is_file()


def test_frontend_contains_design_tokens():
    root = Path(__file__).parents[1]
    styles = (root / "frontend/styles.css").read_text()
    markup = (root / "frontend/index.html").read_text().lower()
    assert "#f8fafc" in styles.lower()
    assert "#2563eb" in styles.lower()
    assert "space grotesk" in styles.lower()
    assert "jetbrains mono" in styles.lower()
    assert "service status" not in markup


def test_frontend_behavior_contracts_exist():
    source = (Path(__file__).parents[1] / "frontend/app.js").read_text()
    assert "fetch('/chat'" in source or 'fetch("/chat"' in source
    assert "response.json()" in source
    assert "textContent" in source
    assert "navigator.clipboard" in source
    assert "shiftKey" in source


def test_root_route_returns_html():
    import importlib.util

    root = Path(__file__).parents[1]
    spec = importlib.util.spec_from_file_location("thunai_main", root / "main.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    response = module.home()
    assert str(response.path) == str(root / "frontend/index.html")
    markup = (root / "frontend/index.html").read_text().lower()
    assert "thunai" in markup
    assert "service status" not in markup


def test_landing_page_has_no_polar_engine_suggestions_or_footer():
    root = Path(__file__).parents[1]
    markup = (root / "frontend/index.html").read_text().lower()
    styles = (root / "frontend/styles.css").read_text().lower()
    script = (root / "frontend/app.js").read_text().lower()
    reference = (root / "ui-design.md").read_text().lower()
    assert "polar engine" not in markup
    assert "polar engine" not in styles
    assert "polar engine" not in script
    assert "polar engine" not in reference
    assert "example-prompt" not in markup
    assert "example-prompt" not in styles
    assert "example-prompt" not in script
    assert "<footer" not in markup
    assert ".site-footer" not in styles
    assert "thunai minimal" not in reference

