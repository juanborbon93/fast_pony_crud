FROM python:rc-buster
RUN apt-get update && \
apt-get install -y dos2unix
COPY . /
RUN python3 -m pip install --user --upgrade setuptools wheel && \
python3 setup.py sdist bdist_wheel 
EXPOSE 5000
ENTRYPOINT ["python"]
CMD  ["-m twine upload dist/* -u $USERNAME -p $PASSWORD]
