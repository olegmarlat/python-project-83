### Hexlet tests and linter status:

[![Actions Status](https://github.com/olegmarlat/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/olegmarlat/python-project-83/actions)

[![Quality gate](https://sonarcloud.io/api/project_badges/quality_gate?project=olegmarlat_python-project-83)](https://sonarcloud.io/summary/new_code?id=olegmarlat_python-project-83)

### Ссылка на сайт проекта:

https://dashboard.render.com/web/srv-cujrealds78s739ip59g

\*\*

## Requirements:

[Python 3.13 +] - (https://www.python.org/downloads/)

[UV 0.7.3 +] - (https://astral.sh)

---

## Installation:

```
git clone git@github.com:https://github.com/olegmarlat/python-project-83
```

```
cd python-project-83
```

```
uv build
```

```
uv tool install dist/*.whl
```

---

Local start:

```
uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
```

---
