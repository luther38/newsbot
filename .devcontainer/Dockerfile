# Update the VARIANT arg in docker-compose.yml to pick a Python version: 3, 3.8, 3.7, 3.6 
ARG VARIANT=3
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}
#FROM python:3.8.5-slim-buster

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive
ENV CHROME_VERSION=90.0.4430.85-1
ENV DRIVER_VERSION=90.0.4430.24

# Update args in docker-compose.yaml to set the UID/GID of the "vscode" user.
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN if [ "$USER_GID" != "1000" ] || [ "$USER_UID" != "1000" ]; then \
        groupmod --gid $USER_GID vscode \
        && usermod --uid $USER_UID --gid $USER_GID vscode \
        && chmod -R $USER_UID:$USER_GID /home/vscode; \
    fi

RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
	sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
	apt-get update && \
	apt-get install google-chrome-stable=${CHROME_VERSION} -yf && \
    google-chrome --version

RUN curl https://chromedriver.storage.googleapis.com/${DRIVER_VERSION}/chromedriver_linux64.zip -o /tmp/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver
