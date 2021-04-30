ARG TAG="latest"

FROM teambge/basic-model-python2.7:${TAG}

LABEL maintainer="teambge"
ENV PATH="/code:/code/lib:${PATH}"

RUN pip install -U tornado

WORKDIR /server
COPY ./server/ /server/