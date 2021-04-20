ARG TAG="2.7.13-jessie"

FROM python:${TAG}

LABEL maintainer="teambge"
ENV PATH="/code:/code/lib:${PATH}"
RUN echo "ALL ALL=NOPASSWD: ALL" >> /etc/sudoers

WORKDIR /server
COPY ./server/ /server/

# Install dev dependencies.
RUN pip install -U six pip setuptools tornado

# Buildin modules from aliyun-fc
RUN pip install -r ./requirements.txt