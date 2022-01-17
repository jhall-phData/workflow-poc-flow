FROM python:3.7
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash
RUN /usr/local/bin/python -m pip install --upgrade pip
WORKDIR /opt/prefect
# COPY flow_utilities/ /opt/prefect/flow_utilities/
COPY requirements.txt .
COPY setup.py .
RUN pip install .
