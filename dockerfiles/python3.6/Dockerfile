ARG TAG="3.6.3-jessie"

FROM python:${TAG}

LABEL maintainer="teambge"
ENV PATH="/code:/code/lib:${PATH}"
RUN echo "ALL ALL=NOPASSWD: ALL" >> /etc/sudoers

# Install dev dependencies.
RUN pip install -U six pip setuptools tornado

WORKDIR /server
COPY ./server/ /server/

# Buildin modules from aliyun-fc
RUN pip install -r ./requirements.txt