# RestAPISQLalchemyContactsManager

I'm using MySQL, MySQL Workbench and XAMPP programmes

## Installation

1. Sklonuj repozytorium: `git clone https://github.com/Camilleus/RestAPISQLalchemyContactsManagerV4.git`
2. Przejdź do folderu projektu: `cd RestAPISQLalchemyContactsManagerV4`
3. Zainstaluj zależności: `poetry install`
4. Uruchom serwer: `uvicorn main:app --host localhost --port 8000 --reload`

## Requirements

Everything in poetry files

## Contributions

Nie potrzebuję ale spoko jeśli takie sie ukażą

## Project Structure

```
RestAPISQLAlchemyContactManagerV4
├─ .gitattributes
├─ api
│  ├─ apis.py
│  ├─ config.py
│  ├─ endpoints.py
│  ├─ routes.py
│  └─ __init__.py
├─ auth
│  ├─ auths.py
│  ├─ jwts.py
│  └─ __init__.py
├─ db
│  ├─ data_faker.py
│  ├─ data_sender.py
│  ├─ dbs.py
│  └─ __init__.py
├─ docker-compose.yaml
├─ main.py
├─ models.py
├─ poetry.lock
├─ pyproject.toml
├─ README.md
├─ requirements.txt
├─ schemas.py
├─ static
│  └─ styles.css
├─ templates
│  ├─ base.html
│  ├─ contacts.html
│  ├─ index.html
│  ├─ login,html
│  ├─ register.html
│  ├─ verify.html
│  └─ welcome.html
└─ __init__.py
```
