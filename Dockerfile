FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /src

COPY requirements.txt /src

RUN pip install --upgrade pip && \
    pip install -r /src/requirements.txt

COPY ./ /src

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8080"]