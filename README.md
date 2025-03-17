# Stock Log Backend / Stock Control Backend

## Hakkında / About

**TÜRKÇE:**  
Bu proje, stok takibi ve yönetimi için geliştirilmiş bir backend servisidir. Django tabanlı yapısı sayesinde, stok işlemlerinin kaydı, yönetimi ve raporlanması gibi işlevleri sağlamayı hedefler. Proje, Docker desteğiyle konteynerize edilmiştir ve üretim ortamlarında supervisord kullanılarak süreç yönetimi yapılmaktadır.

**ENGLISH:**  
This project is a backend service developed for stock control and management. Built on Django, it aims to provide functionalities such as recording, managing, and reporting stock operations. The project is containerized with Docker and utilizes Supervisor for process management in production environments.

---

## Özellikler / Features

**TÜRKÇE:**  
- Django tabanlı sağlam ve esnek yapı  
- REST API endpoint'leri ile stok işlemlerinin yönetimi  
- Docker desteği ile kolay dağıtım ve izolasyon  
- Supervisor entegrasyonu ile süreç yönetimi  
- Modüler yapı sayesinde genişletilebilir mimari

**ENGLISH:**  
- Robust and flexible Django-based architecture  
- Stock management via REST API endpoints  
- Docker support for easy deployment and isolation  
- Process management with Supervisor integration  
- Modular architecture enabling easy extensibility

---

## Kurulum ve Çalıştırma / Installation and Running

### Yerel Ortamda Çalıştırma / Running Locally

**TÜRKÇE:**
1. Repoyu klonlayın:
   ```bash
   git clone https://github.com/dorukcancakir/stock-log-backend.git
   ```
2. Proje dizinine geçin:
   ```bash
   cd stock-log-backend
   ```
3. (Opsiyonel) Sanal ortam oluşturup aktif hale getirin:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows için: venv\Scripts\activate
   ```
4. Gerekli paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
5. Veritabanı migrasyonlarını uygulayın:
   ```bash
   python manage.py migrate
   ```
6. Geliştirme sunucusunu başlatın:
   ```bash
   python manage.py runserver
   ```

**ENGLISH:**
1. Clone the repository:
   ```bash
   git clone https://github.com/dorukcancakir/stock-log-backend.git
   ```
2. Navigate to the project directory:
   ```bash
   cd stock-log-backend
   ```
3. (Optional) Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows için: venv\Scripts\activate
   ```
4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
5. Apply the database migrations:
   ```bash
   python manage.py migrate
   ```
6. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Docker ile Çalıştırma / Running with Docker

**TÜRKÇE:**
1. Docker imajını oluşturun:
   ```bash
   docker build -t stock-log-backend .
   ```
2. Konteyneri başlatın:
   ```bash
   docker run -p 8000:8000 stock-log-backend
   ```

**ENGLISH:**
1. Build the Docker image:
   ```bash
   docker build -t stock-log-backend .
   ```
2. Run the container:
   ```bash
   docker run -p 8000:8000 stock-log-backend
   ```

### Yapılandırma / Configuration
TÜRKÇE:
Proje, core ve stock_log olmak üzere iki ana modüle ayrılmıştır. Uygulamanın yapılandırma ayarları, gizli bilgileri ve ortam değişkenleri üzerinden yönetilebilir. Gerekli ayarları settings.py dosyası ve/veya ortam değişkenleri aracılığıyla yapılandırabilirsiniz.

ENGLISH:
The project is organized into two main modules: core and stock_log. Configuration settings, sensitive data, and environment variables can be managed through configuration files (such as settings.py) or directly via environment variables.

### Süreç Yönetimi / Process Management
TÜRKÇE:
Üretim ortamında, süreç yönetimi için supervisord.conf dosyası kullanılmaktadır. Bu yapılandırma, uygulamanın farklı bileşenlerinin (örneğin, web sunucusu, background işlemler vb.) Supervisor tarafından kontrol edilmesini sağlar.

ENGLISH:
In production, the supervisord.conf file is used for process management. This configuration ensures that various components of the application (such as the web server and background processes) are managed by Supervisor.

### Katkıda Bulunma / Contributing
TÜRKÇE:
Katkıda bulunmak isterseniz, lütfen proje sahibiyle iletişime geçiniz. Bu proje "All Rights Reserved" lisansı kapsamında korunmaktadır; dolayısıyla izinsiz dağıtım, değiştirme veya yeniden dağıtım yapılması yasaktır.

ENGLISH:
If you wish to contribute, please contact the project owner. This project is protected under an "All Rights Reserved" license, so unauthorized use, modification, or distribution is prohibited.

### Lisans / License
TÜRKÇE:
Bu proje, "All Rights Reserved" (Tüm Hakları Saklıdır) lisansı altında yayınlanmıştır. Yazılı izin olmadan kullanımı, dağıtımı veya değiştirilmesi kesinlikle yasaktır.

ENGLISH:
This project is published under an "All Rights Reserved" license. Unauthorized use, distribution, or modification is strictly prohibited without written permission.
