#Dockerfile defines images
#build
FROM python:3-onbuild 
RUN printf "deb http://archive.debian.org/debian/ jessie main\ndeb-src http://archive.debian.org/debian/ jessie main\ndeb http://security.debian.org jessie/updates main\ndeb-src http://security.debian.org jessie/updates main" > /etc/apt/sources.list
#install redis CLI
#CMD ["python", "pip install pandas"]
WORKDIR coe-332-final-project
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install -y redis-tools

RUN apt-get update && apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y build-essential

COPY requirements.txt /

RUN /bin/bash -c "source activate myenv  && pip install --trusted-host pypi.python.org -r /requirements.txt"

FROM library/python:3.6-stretch

COPY requirements.txt /
RUN pip install -r /requirements.txt

EXPOSE 5000
CMD ["python", "./main.py"]
