FROM python:2.7-slim
# show python logs as they occur
ENV PYTHONUNBUFFERED=0

# get packages
WORKDIR /
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# add files into working directory
COPY static static
COPY templates templates
COPY *.py .

EXPOSE 8080
ENTRYPOINT ["python", "/app.py"]