# Creating image based on official python3 image
FROM python:3.10-slim

# Sets dumping log messages directly to stream instead of buffering
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Creating and putting configurations
RUN mkdir /config
ADD config/ecoinomy/ /config/

# Installing all python dependencies
#COPY /config/requirements.txt /config/
RUN apt-get update && apt-get install -y \
    gnupg2 git gdal-bin binutils libproj-dev libgdal-dev ca-certificates gnupg2 libmagickwand-dev poppler-utils wget && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip && pip install -r /config/requirements.txt

# Open port 8000 to outside world
EXPOSE 8000

# When container starts, this script will be executed.
# Note that it is NOT executed during building
CMD ["sh", "/config/on-container-start.sh"]

# ENV DJANGO_SETTINGS_MODULE chat_app.settings_dev

# Creating and putting application inside container
# and setting it to working directory (meaning it is going to be default)
RUN mkdir /ecoinomy
WORKDIR /ecoinomy
ADD ecoinomy /ecoinomy/