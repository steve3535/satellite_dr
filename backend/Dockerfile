FROM python:3.11-alpine 
WORKDIR /usr/src 
COPY requirements.txt . 
RUN pip install -r requirements.txt 
COPY backend.py .
EXPOSE 9001
ENTRYPOINT ["python","-u","./backend.py"]