FROM python:3.10

WORKDIR /src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY entrypoint_dev.sh .
RUN sed -i 's/\r$//g' /src/entrypoint_dev.sh
RUN chmod +x /src/entrypoint_dev.sh

COPY investment_portfolios .

ENTRYPOINT ["/src/entrypoint_dev.sh"]

