FROM python:rc-buster
RUN apt-get update && \
apt-get install -y dos2unix
ARG VER=0.0.2
ENV VERSION=$VER
COPY . /
RUN python3 -m pip install --user --upgrade setuptools wheel twine && \
python3 setup.py sdist bdist_wheel 
EXPOSE 5000
RUN dos2unix publish.sh && \
chmod +x /publish.sh
ENTRYPOINT [ "/publish.sh" ]
