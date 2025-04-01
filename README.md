# FastAPI URL Shortener

Hello UnitedMasters Manager!

Here’s my attempt at a URL shortener. I took the idea of a “rudimentary solution” to heart and built something intentionally simple, but structured in a way that makes it easy to grow and maintain.

I built a lightweight, developer-friendly URL shortener built with [FastAPI](https://fastapi.tiangolo.com/), [SQLModel](https://sqlmodel.tiangolo.com/), and [SQLite](https://www.sqlite.org/index.html). Designed to be easy to use, read and extend.

---

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLModel](https://sqlmodel.tiangolo.com/) (SQLAlchemy + Pydantic = ❤️)
- [Uvicorn](https://www.uvicorn.org/)
- [SQLite](https://www.sqlite.org/index.html)
- [shortuuid](https://github.com/skorokithakis/shortuuid)

## Project Setup

## 1. Clone the repo

```bash
git clone https://github.com/your-username/fastapi-url-shortener.git
cd fastapi-url-shortener
```

## 2. Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows (i think?)
pip install -r requirements.txt
```

## 3. Run the app

```bash
fastapi dev app/main.py
```