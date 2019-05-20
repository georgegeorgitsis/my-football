FROM python:3.5

ENV LOGPATH /var/log

RUN apt-get update && apt-get install -y gcc musl git imagemagick wget libxml2 libxml2-dev libxslt-dev tesseract-ocr-dev tesseract-ocr xvfb gfortran zbar-tools poppler-utils ghostscript wkhtmltopdf xvfb

RUN echo '#!/bin/bash\nxvfb-run -a --server-args="-screen 0, 1024x768x24" /usr/bin/wkhtmltopdf -q $*' > /usr/bin/wkhtmltopdf.sh

RUN chmod a+x /usr/bin/wkhtmltopdf.sh

RUN ln -s /usr/bin/wkhtmltopdf.sh /usr/local/bin/wkhtmltopdf

#RUN mkdir -p /data/db
#
#RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6
#
#RUN echo "deb http://repo.mongodb.org/apt/debian jessie/mongodb-org/3.4 main" | tee /etc/apt/sources.list.d/mongodb-org-3.4.list
#
#RUN apt-get update
#
#RUN apt-get install -y mongodb
#
#RUN pip install pymongo

RUN pip install inquirer

#CMD mongod