FROM python:3.12-slim

WORKDIR /app

# System deps (optional but handy for SSL/root certs)
RUN apt-get update \
  && apt-get install -y --no-install-recommends ca-certificates \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY dify_creator/ /app/dify_creator/
COPY examples/ /app/examples/
COPY README.md /app/README.md

# Default entrypoint: run the CLI module
ENTRYPOINT ["python", "-m", "dify_creator"]


