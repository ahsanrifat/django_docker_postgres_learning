FROM python:3.9-slim
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# installing netcat (nc) since we are using that to listen to postgres server in entrypoint.sh
RUN apt-get update && apt-get install -y --no-install-recommends netcat && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000
#CMD python manage.py runserver 0.0.0.0:8000

# run entrypoint.sh
RUN chmod +x entrypoint.sh
#
ENTRYPOINT ["/app/entrypoint.sh"]