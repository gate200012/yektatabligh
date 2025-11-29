# سامانه تحلیل شبکه‌های اجتماعی

یک MVP ساده برای جمع‌آوری، پردازش و نمایش داده از توییتر (X) و تلگرام.

## اجرا با Docker Compose

1. یک فایل `.env` بر اساس `.env.example` بسازید.
2. دستور زیر را اجرا کنید:

```bash
docker compose up --build
```

- API در `http://localhost:8000/api`
- رابط وب در `http://localhost:3000`

## ساختار پوشه‌ها

- `backend/` : سرویس FastAPI با زمان‌بندی و ماژول‌های NLP ساده
- `frontend/` : رابط React + TypeScript + Tailwind
- `docker-compose.yml` : راه‌اندازی PostgreSQL، بک‌اند و فرانت‌اند

## نکات کلیدی

- احراز هویت مبتنی بر JWT با نقش‌های `admin`، `analyst` و `viewer`
- کانکتورهای آزمایشی برای توییتر و تلگرام به شکل Mock
- زمان‌بندی جمع‌آوری داده با APScheduler (هر ۱۵ دقیقه یا مقدار `.env`)
- APIهای اصلی: احراز هویت، کانکتورها، پست‌ها، دسته‌ها، داشبورد، پیشنهادها و هشدارها
- تست نمونه برای ماژول NLP در `backend/app/tests`

## توسعه محلی بدون Docker

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

و برای فرانت‌اند:

```bash
cd frontend
npm install
npm run dev
```
