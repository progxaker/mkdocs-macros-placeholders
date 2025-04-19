FROM python:3.11

WORKDIR /app

ENV PIP_ROOT_USER_ACTION=ignore
RUN pip install --upgrade pip && pip install mkdocs && pip install mkdocs-macros-plugin

EXPOSE 8000

CMD ["mkdocs", "serve", "--dev-addr=0.0.0.0:8000"]
