FROM python:3.12-slim


WORKDIR /app


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


COPY app .


ARG APP_VERSION=development
ARG BUILD_DATE=unknown
ARG BUILD_BRANCH=unknown
ARG BUILD_COMMIT=unknown


ENV APP_VERSION=$APP_VERSION
ENV BUILD_DATE=$BUILD_DATE
ENV BUILD_BRANCH=$BUILD_BRANCH
ENV BUILD_COMMIT=$BUILD_COMMIT


EXPOSE 5000


CMD ["python","app.py"]
