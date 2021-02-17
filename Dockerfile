FROM python:3.8.7

WORKDIR /Users/i857921/PycharmProjects/playwright

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m playwright install

RUN apt-get -y update
RUN apt-get -y install gdebi-core
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN gdebi -n google-chrome-stable_current_amd64.deb



