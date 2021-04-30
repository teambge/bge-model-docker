ARG TAG="2.7.13-jessie"

FROM python:${TAG}

LABEL maintainer="teambge"

RUN echo "ALL ALL=NOPASSWD: ALL" >> /etc/sudoers

# Install dev dependencies.
RUN pip install -U six pip setuptools

# Buildin modules from aliyun-fc
RUN pip install oss2==2.6.0 \
    tablestore==4.6.0 \
    aliyun-fc2==2.1.0 \
    aliyun-python-sdk-ecs==4.10.1 \
    aliyun-python-sdk-vpc==3.0.2 \
    aliyun-python-sdk-rds==2.1.4 \
    aliyun-python-sdk-kms==2.5.0 \
    aliyun-mns==1.1.5 \
    aliyun-python-sdk-cdn==2.6.2 \
    aliyun-python-sdk-ram==3.0.0 \
    aliyun-python-sdk-sts==3.0.0 \
    aliyun-python-sdk-iot==7.8.0 \
    aliyun-log-python-sdk==0.6.38 \
    wand==0.4.4 \
    numpy==1.13.3 \
    scipy==1.0.0 \
    matplotlib==2.0.2 \
    scrapy==1.4.0 \
    opencv-python==3.3.0.10 \
    cprotobuf==0.1.9 \
    pydatahub==2.11.2
