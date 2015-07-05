FROM ubuntu:15.04
 
RUN apt-get update
#RUN apt-get upgrade -y
RUN apt-get install -y python python-dev python-distribute python-pip
 
COPY . /

RUN pip install -r /requirements.txt

EXPOSE 8080
CMD ["python","/application.py"]
