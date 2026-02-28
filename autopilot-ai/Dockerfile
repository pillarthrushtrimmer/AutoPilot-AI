FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml .
COPY src/ src/
COPY plugins/ plugins/
COPY config/ config/
RUN pip install --no-cache-dir -e .
RUN playwright install --with-deps chromium
EXPOSE 8000
CMD ["autopilot", "serve", "--port", "8000"]
