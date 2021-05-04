FROM python:3.8

WORKDIR /simple_fastapi_app
COPY . .
RUN python -m pip install -r requirements.txt

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]