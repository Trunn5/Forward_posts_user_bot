FROM python:3.11

WORKDIR /forwardpost
COPY ./ ./

RUN rm -rf /etc/localtime
RUN ln -s /usr/share/zoneinfo/Europe/Moscow /etc/localtime
RUN echo "Europe/Moscow" > /etc/timezone

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python","-u", "main.py"]
#CMD ["python","-u", "db/connection.py"]
