FROM centos:8

ENV PYTHON_VERSION 3.9.2
ENV SOURCE_DIRECTORY /root/project
COPY . $SOURCE_DIRECTORY
WORKDIR $SOURCE_DIRECTORY

RUN dnf upgrade -y && \
    dnf group install -y "Development Tools" && \
    dnf install -y sqlite-devel openssl-devel zlib-devel libffi libffi-devel wget && \
    wget https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tar.xz && \
    tar -xJf Python-$PYTHON_VERSION.tar.xz && \
    cd Python-$PYTHON_VERSION && \
    ./configure --enable-loadable-sqlite-extensions && \
    make && \
    make install

RUN pip3 install --upgrade pip setuptools && \
    pip3 install -r requirements.txt