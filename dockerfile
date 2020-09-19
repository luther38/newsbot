FROM python:3.8

RUN apt install libglib2 libnss3 libgconf libfontconfig1

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

RUN curl https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o /chrome.deb
RUN dpkg -i /chrome.deb || apt-get install -yf
RUN rm /chrome.deb

RUN wget https://chromedriver.storage.googleapis.com/86.0.4240.22/chromedriver_linux64.zip && \
	unzip ./chromedriver_linux64.zip && \
	rm ./chromedriver_linux64.zip

CMD [ "python", "app.py" ]