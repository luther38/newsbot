FROM python:3.8-slim-buster

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive && \
	apt-get install -y curl unzip

RUN curl https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o /tmp/chrome.deb \
	&& dpkg -i /tmp/chrome.deb || apt-get install -yf \
	&& rm /tmp/chrome.deb

RUN curl https://chromedriver.storage.googleapis.com/85.0.4183.87/chromedriver_linux64.zip -o /tmp/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver

CMD [ "python", "app.py" ]