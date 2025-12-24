FROM python:3.11.2

WORKDIR /firewall_api

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY firewall_api.py .
EXPOSE 8000
CMD ["uvicorn", "firewall_api:app", "--host", "0.0.0.0", "--port", "8000"]
