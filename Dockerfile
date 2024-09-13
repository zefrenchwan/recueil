FROM python:3.12.6-bookworm

COPY requirements.txt /app/
RUN pip install --requirement /app/requirements.txt
COPY app/ /app/
WORKDIR /app/
EXPOSE 8000
CMD ["fastapi", "run", "main.py", "--port", "8000"]