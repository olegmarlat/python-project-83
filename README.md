### Hexlet tests and linter status:

[![Actions Status](https://github.com/olegmarlat/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/olegmarlat/python-project-83/actions)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=olegmarlat_python-project-83&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=olegmarlat_python-project-83)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=olegmarlat_python-project-83&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=olegmarlat_python-project-83)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=olegmarlat_python-project-83&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=olegmarlat_python-project-83)

[![SonarQube Cloud](https://sonarcloud.io/images/project_badges/sonarcloud-light.svg)](https://sonarcloud.io/summary/new_code?id=olegmarlat_python-project-83)
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
