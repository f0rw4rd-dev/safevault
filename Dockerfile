FROM python:3.11.2

# create staticfiles & mediafiles folders and set dir
ENV HOME=/var/www/safevault
RUN mkdir /var/www && mkdir $HOME
RUN mkdir $HOME/static && mkdir $HOME/media
WORKDIR $HOME

# set up python environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# upgrade packages
RUN pip install --upgrade pip

# create a local virtual environment
RUN pip install virtualenv && virtualenv venv

# install all requirements
COPY ./requirements.txt .
RUN . venv/bin/activate && pip install -r requirements.txt

RUN apt-get update && apt-get -y install gettext

# copy project files
COPY . $HOME

#COPY --chown=root . /var/www/safevault
#RUN chmod +x /var/www/safevault/entrypoint.sh
ENTRYPOINT ["/var/www/safevault/entrypoint.sh"]