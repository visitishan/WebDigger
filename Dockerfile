FROM python:3

ADD digfile.py /

ADD bannerfile.py /

COPY requirements.txt /tmp

COPY digfile.py /tmp

COPY bannerfile.py /tmp

WORKDIR /tmp

RUN pip3 install -r requirements.txt

CMD [ "python", "./digfile.py" ]