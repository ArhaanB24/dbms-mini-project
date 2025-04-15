FROM python:3.11-slim
COPY . /main
WORKDIR /main
RUN pip install --upgrade pip
RUN pip install -r requirements.txt 
EXPOSE 5001 
ENTRYPOINT [ "python" ] 
CMD ["main.py"]