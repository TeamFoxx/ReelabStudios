# Build basic python-alpine image
FROM python:3.10-alpine as base
MAINTAINER Aurel Hoxha
LABEL maintainer="info@aurelhoxha.de"

WORKDIR /svc
COPY . /
RUN apk add --no-cache libjpeg-turbo g++ curl build-base musl-dev linux-headers python3-dev
# RUN pip install --no-cache-dir --no-index -r requirements.txt

# add missing packages into stage image
FROM python:3.10-alpine as stage
RUN apk add git gcc musl-dev linux-headers python3-dev
COPY --from=base /svc /usr/local
COPY --from=base /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY requirements.txt /
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Setup final Image
FROM python:3.10-alpine
# Copy all pip packages to the new image!
COPY --from=stage /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
# Add needed programs
# RUN apk add --no-cache tzdata py3-lxml libjpeg-turbo freetype-dev curl
# Set working directory
WORKDIR /bot
# Setup Environment Variables


# Sync Timezone with Host
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

USER 1000:1000


# Start Image
# ENTRYPOINT [ "tail", "-f", "/dev/null" ]
MAINTAINER Aurel Hoxha info@aurelhoxha.de
ENTRYPOINT ["python3", "main.py"]