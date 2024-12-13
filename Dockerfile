# Python 3.13 tabanlı bir Docker imajı
FROM python:3.13-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Gereksinim dosyasını kopyala
COPY requirements.txt .

# Python bağımlılıklarını yükle
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyala
COPY . .

# Django uygulaması için başlangıç komutu
CMD ["uvicorn", "stock_log.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
