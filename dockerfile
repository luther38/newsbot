FROM python:3.8-slim-buster

ENV DEBIAN_FRONTEND=noninteractive

# https://www.ubuntuupdates.org/package/google_chrome/stable/main/base/google-chrome-stable
ENV CHROME_VERSION=89.0.4389.90-1

# https://chromedriver.chromium.org/downloads
ENV DRIVER_VERSION=89.0.4389.23

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
	&& apt-get install -y \
		curl \
		unzip \
		wget \
		gnupg \
		gnupg2 \
		gnupg1 \
	&& apt-get autoremove \
	&& apt-get clean \
	&& apt-get autoclean

RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
	sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
	apt-get update && \
	apt-get install google-chrome-stable=${CHROME_VERSION} -yf && \
    google-chrome --version

RUN curl https://chromedriver.storage.googleapis.com/${DRIVER_VERSION}/chromedriver_linux64.zip -o /tmp/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin/ &&\
    chmod +x /usr/local/bin/chromedriver && \
	rm /tmp/chromedriver_linux64.zip

CMD [ "python", "app.py" ]