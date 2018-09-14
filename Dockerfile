FROM ubuntu:latest

RUN  apt-get update 
RUN apt-get install -y wget
RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv 
RUN apt-get install -y curl
COPY . /app
WORKDIR /app
RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install wheel
RUN pip install -r requirements.txt
RUN pip install pdfkit
RUN apt-get install -y wkhtmltopdf
RUN pip install -U selenium
RUN pip install pyvirtualdisplay
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/bin/

RUN apt-get install wkhtmltopdf
RUN apt-get install xvfb
# set display port to avoid crash
ENV DISPLAY=:99
RUN pip install xvfbwrapper
RUN pip install python-pdf
ENTRYPOINT ["python3"]
CMD ["app.py"]
