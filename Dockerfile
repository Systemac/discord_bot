FROM python:3.8
COPY requirements.txt main.py ./
ENV TZ "Europe/Paris"
RUN echo $TZ > /etc/timezone && \
apt-get update && apt-get install -y tzdata && \
rm /etc/localtime && \
ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
dpkg-reconfigure -f noninteractive tzdata && \
apt-get clean
RUN pip install --no-cache-dir -r /requirements.txt
RUN apt-get update
RUN apt-get -y install curl dirmngr apt-transport-https lsb-release ca-certificates apt-utils
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt install -y nodejs
RUN apt -y install gcc g++ make
RUN npm install pm2 -g
RUN apt autoremove -y
RUN apt clean
RUN pm2 start main.py
CMD ['pm2', 'monit']