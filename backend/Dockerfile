FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    git gcc g++ make cmake curl

WORKDIR /app

COPY . .

RUN python3 build_shared_lib.py

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
