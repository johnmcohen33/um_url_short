# FastAPI URL Shortener

Hello UnitedMasters Manager !

Here’s my take on a URL shortener. I embraced the “rudimentary solution” brief and focused on building something simple, clean, and hopefully easy to extend.

This is a lightweight, developer-friendly app built with [FastAPI](https://fastapi.tiangolo.com/), [SQLModel](https://sqlmodel.tiangolo.com/), and [SQLite](https://www.sqlite.org/index.html).

I spent around **4 hours** on this solution. Originally I tried to create something Dockerized, with a PostgreSQL DB but frankly was running into too many issues for this level of assignment. I probably tinkered with OAuth2 in the final solution way more than necessary, but it was a good learning experience — and I wanted to make sure the app included protected routes and a basic user flow, as that would likely be part of any real system.

**Note on Auth:**  
The `auth.py` file is adapted directly from the FastAPI docs:  
[https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)  
I want to be very clear that I’m not claiming authorship of that portion. I included it to demonstrate that I can integrate and adapt official examples quickly and appropriately for the project context. That is also why it is far less documented than other parts of this.

Thanks so much for reviewing this — I had fun with it, and I’m excited to keep learning.

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

## Usage

Once the app is running, visit the base URL:

**http://127.0.0.1:8000**

Interactive API documentation is available at:

**http://127.0.0.1:8000/docs**

This is the easiest way to explore and test all available endpoints. Below are some special instructions around redirect behavior if you wanna see the shortener in action!

## Redirect Behavior

One feature that may not be immediately obvious is that the app supports **URL redirection** using the generated short links.

### How to Use It:

1. Visit:

   **http://127.0.0.1:8000/urls/**  
   This will return a list of all saved short URLs.

2. Take one of the `short_url` values and append it to the base URL.  
   For example, if the response looks like:

   ```json
   {
       "expiration_date": null,
       "short_url": "4AphGHq",
       "long_url": "https://www.arsenal.com/"
   }
   ```

3.	Navigate to:
http://127.0.0.1:8000/4AphGHq
This will automatically redirect you to https://www.arsenal.com/

## Project Layout

```
app/
├── main.py               # App entrypoint and FastAPI instance
├── config.py             # App settings
├── database.py           # SQLModel + SQLite setup
├── models.py             # Data models
├── routes/               # Route definitions
│   ├── url_shortener.py  # Shorten + redirect logic
│   └── auth.py           # Authentication and user management
├── crud/                 # DB interaction logic
```

## Future Improvements

Ummm there are a lot that come to mind.

Off the top of my head
- TESTING TESTING TESTING
    - I was already way over on time so I didn't add.
    - I did try to organize the project in a way that testing concerns could be seperated.
- Support for custom aliases
- Support for expiration dates
- Ensure URLs are safe
- Ensure URLs map to websites we are comfortable with
- Add analytics
- Dockerize the app
- I'm sure there is a smart way to prevent collisions without hitting the DB an extra time
    - Maybe we could store some candidates in memory?

## Last Notes

This was a fun project to build! I hope it was ok to look through. Please let me know if you have any questions at:

johnmcohen33@gmail.com