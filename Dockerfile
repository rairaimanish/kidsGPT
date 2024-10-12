FROM pytorch/pytorch:2.4.1-cuda12.4-cudnn9-devel

# Update the package list and install Python 3.10 and pip
RUN apt-get update && \
    apt-get install -y python3.10 python3.10-distutils python3-pip

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip3.10 install -r /app/requirements.txt

COPY . /app

CMD ["python3.10", "examples/web/webui.py"]