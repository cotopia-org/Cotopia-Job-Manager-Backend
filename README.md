- git pull
- Create a db inside postgres
- python -m venv .venv
- source .venv/bin/activate
- pip install -r requirements.txt
- build .env
- alembic revision --autogenerate
- alembic upgrade head
- pm2 start "uvicorn main:app --port 4242" --name jm-api
