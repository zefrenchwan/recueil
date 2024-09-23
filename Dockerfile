FROM python:3.12.6-bookworm

COPY requirements.txt /app/
RUN pip install gunicorn 
RUN pip install --requirement /app/requirements.txt
COPY app/ /app/
COPY bootstrap/ /storage/bootstrap/
VOLUME logs/ /app/logs/
WORKDIR /app/
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "main:app"]