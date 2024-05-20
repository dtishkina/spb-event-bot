FROM python:3.10-slim

WORKDIR /bot

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
