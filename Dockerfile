FROM python:3.8
COPY requirements.txt main.py ./
RUN pip install --no-cache-dir -r /requirements.txt
CMD [ "python", "main.py" ]