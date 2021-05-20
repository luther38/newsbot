# Chrome Stable = https://www.ubuntuupdates.org/package/google_chrome/stable/main/base/google-chrome-stable
# Chrome Driver = https://chromedriver.chromium.org/downloads
FROM python:3.8-slim-buster

ENV DEBIAN_FRONTEND=noninteractive
ARG CHROME_VERSION
ARG DRIVER_VERSION

COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN echo deb http://deb.debian.org/debian/ unstable main contrib non-free >> /etc/apt/sources.list && \
	apt-get update && export DEBIAN_FRONTEND=noninteractive \
	&& apt-get install -y --fix-missing \
		git \
		make \
		curl \
		unzip \
		wget \
		gnupg \
		gnupg2 \
		gnupg1 \
		firefox-esr \
	&& apt-get autoremove -y \
	&& apt-get clean \
	&& apt-get autoclean

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-linux64.tar.gz && \
	tar xf geckodriver-v0.29.1-linux64.tar.gz && \
	chmod +x geckodriver && \
	mv geckodriver /usr/local/bin && \
	rm geckodriver-v0.29.1-linux64.tar.gz

#RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
#	sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
	#apt-get update && \
	#apt-get install google-chrome-stable=${CHROME_VERSION} -yf && \
    #google-chrome --version
#RUN curl https://chromedriver.storage.googleapis.com/${DRIVER_VERSION}/chromedriver_linux64.zip -o /tmp/chromedriver_linux64.zip && \
    #unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin/ &&\
    #chmod +x /usr/local/bin/chromedriver && \
	#rm /tmp/chromedriver_linux64.zip

CMD [ "python", "app.py" ]