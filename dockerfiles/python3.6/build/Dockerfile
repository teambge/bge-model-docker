ARG TAG="latest"

FROM teambge/basic-model-python3.6:${TAG}

LABEL maintainer="teambge"
ENV PATH="/code:/code/lib:${PATH}"

RUN pip install -U tornado

WORKDIR /code
COPY ./server/ /server/
