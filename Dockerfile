# استخدم صورة بايثون الرسمية
FROM python:3.9-slim

# تحديد دليل العمل داخل الحاوية
WORKDIR /Image-Solver

# نسخ محتويات الدليل الحالي إلى دليل العمل في الحاوية
COPY . /Image-Solver

# تثبيت الحزم المطلوبة والمذكورة في requirements.txt
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install transformers

EXPOSE 10000

ENV PORT 10000

# الأمر الذي يتم تنفيذه عند تشغيل الحاوية
CMD ["python", "bot.py"]
