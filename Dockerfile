FROM python:3.6

ENV LOGPATH /var/log

RUN apt-get update && apt-get install -y bash gcc musl git imagemagick wget libxml2 libxml2-dev libxslt-dev

RUN echo '#!/bin/bash\nxvfb-run -a --server-args="-screen 0, 1024x768x24" /usr/bin/wkhtmltopdf -q $*' > /usr/bin/wkhtmltopdf.sh

RUN chmod a+x /usr/bin/wkhtmltopdf.sh

RUN ln -s /usr/bin/wkhtmltopdf.sh /usr/local/bin/wkhtmltopdf

RUN pip install pymongo
RUN pip install inquirer
RUN pip install python-dotenv
RUN pip install matplotlib
