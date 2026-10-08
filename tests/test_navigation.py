"""Static regression checks for the fixed, always-visible navigation."""
from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parent.parent
APP = ROOT / "app.py"


def _app_tree():
    return ast.parse(APP.read_text(encoding="utf-8"))


def test_all_six_pages_exist():
    tree = _app_tree()
    titles = []
    paths = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "Page":
            if node.args and isinstance(node.args[0], ast.Constant):
                paths.append(node.args[0].value)
            for kw in node.keywords:
                if kw.arg == "title" and isinstance(kw.value, ast.Constant):
                    titles.append(kw.value.value)
    assert titles == ["Overview", "Player DNA", "Player comparison", "Cohort analysis", "Modelling", "Reference"]
    assert len(paths) == 6
    for path in paths:
        assert (ROOT / path).is_file(), f"Missing page: {path}"


def test_custom_navigation_is_not_collapsible():
    tree = _app_tree()
    router_calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute) and node.func.attr == "navigation"]
    assert len(router_calls) == 1
    assert any(kw.arg == "position" and isinstance(kw.value, ast.Constant) and kw.value.value == "hidden"
               for kw in router_calls[0].keywords)
    assert any(isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
               and node.func.attr == "page_link" for node in ast.walk(tree))


def test_three_requested_groups_preserved():
    tree = _app_tree()
    groups = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "pages" for t in node.targets):
            groups = [key.value for key in node.value.keys]
    assert groups == ["Start", "Player analysis", "Modelling & reference"]
