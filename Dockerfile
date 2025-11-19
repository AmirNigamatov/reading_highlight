FROM python:3.11-slim@sha256:8ef21a26e7c342e978a68cf2d6b07627885930530064f572f432ea422a8c0907
WORKDIR /src
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim@sha256:8ef21a26e7c342e978a68cf2d6b07627885930530064f572f432ea422a8c0907

RUN useradd --create-home --shell /bin/bash appuser
WORKDIR /src
COPY --from=0 /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=0 /usr/local/bin /usr/local/bin
COPY . .
RUN chown -R appuser:appuser /src
USER appuser
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 CMD python -c "import sys; sys.exit(0)"
ENTRYPOINT ["python", "main.py"]
CMD ["--help"]
