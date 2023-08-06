# zpy-database v0.1.0

> [Zguillez](https://zguillez.io) | Guillermo de la Iglesia

## Pyton database wrapper

# Getting Started

## Install

```
pip install --upgrade zpy-database
```

# Usage

```
from zpy_database import database as db

db.connect({
    'conn': os.environ['DB_HOST'],
    'database': os.environ['DB_NAME'],
    'user': os.environ['DB_USER'],
    'password': os.environ['DB_PASS']
})
```

```
data = db.sql("SELECT id, name FROM my_table")
print(data[0])
```

```
data = db.sql("SELECT id, name FROM my_table", ['id', 'name'])
print(data[0]['name'])
```

```
db.close()
```

# Contributing and issues

Contributors are welcome, please fork and send pull requests! If you have any ideas on how to make this project better
then please submit an issue or [email](mailto:guillermo@delaiglesia.email) me.

# License

©2023 Zguillez.IO

Original code licensed under [MIT](https://en.wikipedia.org/wiki/MIT_License) Open Source projects used within this
project retain their original licenses.

# Changelog

### v0.1.0 (February 13, 2023)

* Initial commit
