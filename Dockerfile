FROM python:3.8
COPY requirements.txt main.py ./app/
RUN pip install --no-cache-dir -r /app/requirements.txt
CMD ["cd /app/"]
CMD [ "python", "main.py" ]