# FastAPI URL Shortener

Hello UnitedMasters Manager!

Here’s my attempt at a URL shortener. I took the idea of a “rudimentary solution” to heart and built something intentionally simple, but structured in a way that makes it easy to grow and maintain.

I built a lightweight, developer-friendly URL shortener built with [FastAPI](https://fastapi.tiangolo.com/), [SQLModel](https://sqlmodel.tiangolo.com/), and [SQLite](https://www.sqlite.org/index.html). Designed to be easy to use, read and extend.

---

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLModel](https://sqlmodel.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [SQLite](https://www.sqlite.org/index.html)
- [shortuuid](https://github.com/skorokithakis/shortuuid)

## Project Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/fastapi-url-shortener.git
cd fastapi-url-shortener
```

### 2. Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows (i think?)
pip install -r requirements.txt
```

### 3. Run the app

```bash
fastapi dev app/main.py
```

## API Documentation

Swagger docs: http://127.0.0.1:8000/docs

I am sure you are familiar but Swagger is awesome ! and you should be able to see this API in action there.

## Project Layout

```
app/
├── main.py               # App entrypoint and FastAPI instance
├── config.py             # App settings
├── database.py           # SQLModel + SQLite setup
├── models.py             # Data models
├── routes/               # Route definitions
│   └── url_shortener.py  # Shorten + redirect logic
├── crud/                 # DB interaction logic
```

 ## Future Improvements

Ummm there are a lot that come to mind.

Off the top of my head
- Support for custom aliases
- Support for expiration dates
- Add analytics
- Dockerize the app
- I'm sure there is a smart way to prevent collisions without hitting the DB an extra time
    - Maybe we could store some candidates in memory
