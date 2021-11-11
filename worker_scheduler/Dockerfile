FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python-dev

WORKDIR /app
RUN pip3 install requests==2.26.0
RUN pip3 install AWSIoTPythonSDK==1.4.9

COPY src/ /app/

EXPOSE 6000

ENTRYPOINT ["python3"]
CMD ["weather_worker.py"]