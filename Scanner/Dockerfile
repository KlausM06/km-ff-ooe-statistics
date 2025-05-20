FROM python:3.11-slim

# You can set the MongoDB API key here
# ENV MDB_API="your_mdb_api_key"

# set the interval in seconds for the scanner to check for new data
ENV SCAN_INTERVAL=3600

# ENV PYTHONUNBUFFERED=1 causes the container to put the print-statement-outputs instantly to the logs
# remove/comment it if you dont care about the logs and want to improve performance slightly by buffering the output
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]