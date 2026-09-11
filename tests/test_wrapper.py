# -*- coding: utf-8 -*-
"""Обёртке нечего ломать в своей логике, зато есть чему разойтись с ядром.

Эти тесты проверяют ровно стыки: точка входа существует, версии сходятся,
цифры в README совпадают с каталогом, который реально приедет с зависимостью.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_entry_point_resolves_to_the_real_server():
    import yandex_market_mcp_ru

    assert callable(yandex_market_mcp_ru.main), "точка входа не вызывается"
    assert yandex_market_mcp_ru.main.__module__.startswith("yandex_mcp")


def test_versions_agree():
    import yandex_market_mcp_ru

    py = re.search(r'^version = "([^"]+)"', (ROOT / "pyproject.toml").read_text(encoding="utf-8"),
                   re.M).group(1)
    sj = json.loads((ROOT / "server.json").read_text(encoding="utf-8"))
    assert py == sj["version"] == sj["packages"][0]["version"] == yandex_market_mcp_ru.__version__


def test_dependency_is_pinned_to_the_documented_core():
    py = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert re.search(r'"marketplaces-mcp-ru>=\d+\.\d+\.\d+,<1"', py), \
        "зависимость должна быть закреплена снизу и в пределах мажорной"


def catalog() -> list[dict]:
    import yandex_mcp as pkg

    path = Path(pkg.__file__).parent / "endpoints.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))["endpoints"]


def test_readme_number_matches_the_catalog_that_ships():
    rows = catalog()
    counts = {"read": 0, "write": 0, "destructive": 0}
    for e in rows:
        counts[e.get("safety", "read")] += 1
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert len(rows) == 165, "каталог изменился, пересобери обвязку генератором"
    assert f"**{len(rows)} " in readme
    assert counts == {"read": 109, "write": 49, "destructive": 7}


def test_registry_description_fits():
    sj = json.loads((ROOT / "server.json").read_text(encoding="utf-8"))
    assert len(sj["description"]) <= 100, "реестр отвечает 422, а не обрезает"
    assert (ROOT / "README.md").read_text(encoding="utf-8").count(
        "<!-- mcp-name: " + sj["name"] + " -->") == 1


def test_skill_description_fits_the_spec():
    """Спека Agent Skills режет description на 1024 символах, и лишнее поле во
    фронтматтере это отказ установки, а не предупреждение."""
    text = (ROOT / "skills" / "yandex-market-mcp" / "SKILL.md").read_text(encoding="utf-8")
    head = text.split("---")[1]
    fields = [ln.split(":", 1)[0] for ln in head.splitlines() if ln and not ln.startswith(" ")]
    assert set(fields) == {"name", "description"}, fields
    desc = head.split('description: "', 1)[1].rsplit('"', 1)[0]
    assert len(desc) <= 1024, len(desc)


def test_no_skill_in_repository_root():
    """Корневой SKILL.md заставляет npx skills add считать скиллом весь
    репозиторий и копировать его пользователю целиком."""
    assert not (ROOT / "SKILL.md").exists()
