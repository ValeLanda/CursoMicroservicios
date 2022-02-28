FROM python:3.9

RUN apt-get update && \
    apt-get install -y \
        iputils-ping && \
    apt-get install -y \
        telnet &&\
    apt-get install -y \
        traceroute
    
COPY ./app /app

RUN pip install -r /app/requirements.pip

WORKDIR /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--limit-concurrency", "300"]
