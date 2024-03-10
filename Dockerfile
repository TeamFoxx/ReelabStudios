"""
MIT License

Copyright (c) 2024 Aurel Hoxha

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Build basic python-alpine image
FROM python:3.10-alpine as base
MAINTAINER Aurel Hoxha
LABEL maintainer="hello@aurelhoxha.de"

WORKDIR /svc
COPY requirements.txt /
# RUN apk add --no-cache libjpeg-turbo g++ curl && pip install --no-cache-dir --no-index --find-links=/svc/wheels -r requirements.txt

# add missing packages into stage image
FROM python:3.10-alpine as stage
RUN apk add git
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
MAINTAINER Aurel Hoxha hello@aurelhoxha.de
ENTRYPOINT ["python3", "main.py"]