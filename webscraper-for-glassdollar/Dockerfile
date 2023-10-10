FROM python:3.9
WORKDIR /main
COPY . /main
RUN pip install -r requirements.txt
EXPOSE 8000
ENV PYTHONUNBUFFERED 1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

