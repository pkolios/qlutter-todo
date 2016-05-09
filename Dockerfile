FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
ENV PYTHONPATH $PYTHONPATH:/code
ENTRYPOINT ["python"]
CMD ["qlutter_todo/app.py"]
