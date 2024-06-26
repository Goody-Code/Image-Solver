FROM python:3.9-slim

WORKDIR /app

# نسخ محتويات المشروع
COPY . /app

# تثبيت الأدوات المطلوبة وإنشاء بيئة افتراضية
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    && python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install -r requirements.txt

# تحميل النموذج أثناء بناء الصورة
RUN /opt/venv/bin/python download_model.py

# إعداد البيئة الافتراضية كبيئة افتراضية افتراضية
ENV PATH="/opt/venv/bin:$PATH"

# الأوامر لتشغيل التطبيق
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8443", "app:app"]
