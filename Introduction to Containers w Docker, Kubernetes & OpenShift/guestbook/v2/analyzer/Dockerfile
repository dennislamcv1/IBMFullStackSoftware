FROM phusion/baseimage:latest-amd64

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && \
    apt-get install -y -q --no-install-recommends \
    openssl python2.7 python-pip build-essential python-dev \
    fakeroot dpkg-dev libcurl4-openssl-dev librtmp-dev libssl-dev
RUN pip install --upgrade pip setuptools
RUN pip install requests Flask Flask-Cache
RUN pip install ndg-httpsclient

RUN pip install pyopenssl
RUN pip install pyasn1
RUN pip install retry

RUN mkdir ~/python-pycurl-openssl && \
    cd ~/python-pycurl-openssl && \
    curl https://files.pythonhosted.org/packages/e8/e4/0dbb8735407189f00b33d84122b9be52c790c7c3b25286826f4e1bdb7bde/pycurl-7.43.0.2.tar.gz -L -O && \
    tar -xzvf pycurl-7.43.0.2.tar.gz && \
    cd pycurl-7.43.0.2 && \
    python2.7 setup.py --with-ssl install

# https://serverfault.com/questions/348815/how-to-change-libcurl-ssl-backend-from-gnutls-to-openssl-on-ubuntu-server

# application source code including static files, templates, etc
ADD src /app/src

EXPOSE 5000

ENTRYPOINT ["python", "-u", "/app/src/app.py"]
