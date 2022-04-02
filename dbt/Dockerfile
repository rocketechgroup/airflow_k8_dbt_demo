FROM python:3.8.13

ARG DBT_HOME=/home/dbtuser

# Update and install system packages
RUN apt-get update -y && \
  apt-get install --no-install-recommends -y -q \
  git libpq-dev python-dev && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN groupadd -g 999 dbtuser && useradd -r -u 999 -g dbtuser dbtuser
WORKDIR ${DBT_HOME}

RUN chown -R dbtuser:dbtuser ${DBT_HOME}

USER dbtuser

RUN mkdir ${DBT_HOME}/.dbt

# Install DBT
RUN pip install -U pip

ENV VIRTUAL_ENV=${DBT_HOME}/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install dbt-core==1.0.4 dbt-bigquery==1.0.0

COPY --chown=dbtuser:dbtuser ./dbt/profiles.yml ${DBT_HOME}/.dbt
COPY --chown=dbtuser:dbtuser ./dbt/dbt_k8_demo ${DBT_HOME}/dbt_k8_demo
