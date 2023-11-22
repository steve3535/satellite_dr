FROM python:alpine
WORKDIR /usr/src
COPY requirements.txt .
RUN pip install -r requirements.txt 
COPY app.py .
ENTRYPOINT ["python","-u","./app.py"]