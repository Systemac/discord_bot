FROM python:3.8
COPY requirements.txt main.py main.sh ./
RUN pip install --no-cache-dir -r /requirements.txt
RUN apt-get update
RUN apt-get -y install curl dirmngr apt-transport-https lsb-release ca-certificates apt-utils
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt install -y nodejs
RUN apt install -y nano
RUN apt -y install gcc g++ make
RUN npm install pm2 -g
#CMD [ "python", "main.py" ]
CMD ["sh", "main.sh"]