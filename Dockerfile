# pull official base image
FROM python:3-alpine


# set work directory
WORKDIR /shop

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install dependencies
RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/

# copy project
COPY . .

EXPOSE 8000