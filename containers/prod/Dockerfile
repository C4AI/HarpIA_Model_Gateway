FROM python:3.11-slim-bookworm

RUN pip install pipx==1.7.1
RUN pipx install poetry==1.2.0
ENV PATH="$PATH:/root/.local/bin:$PATH"

WORKDIR /harpia-gateway
COPY pyproject.toml /harpia-gateway/pyproject.toml
RUN poetry install
COPY src /harpia-gateway

ENTRYPOINT [ "poetry", "run", "python", "-m", "harpia_model_gateway" ]
