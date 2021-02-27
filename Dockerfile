FROM python:3.8.7

WORKDIR /root

RUN git clone https://github.com/lincolnsmithy/playwright.git

RUN echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list
RUN apt-get install wget
RUN wget https://dl.google.com/linux/linux_signing_key.pub
RUN apt-get install gnupg
RUN apt-key add linux_signing_key.pub

RUN apt-get -y update
RUN apt-get install -y google-chrome-stable
RUN apt-get install -yqq unzip curl
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

#RUN apt-get -y install gdebi-core
#RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
#RUN gdebi -n google-chrome-stable_current_amd64.deb
RUN pip3 install --no-cache-dir -r playwright/requirements.txt
RUN python3 -m playwright install





