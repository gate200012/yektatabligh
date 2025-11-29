# نمونه خروجی پروژه

این سند نشان می‌دهد اگر بک‌اند و فرانت‌اند را طبق README اجرا کنید، چه خروجی‌ای دریافت می‌کنید. سناریو بر پایهٔ تنظیمات پیش‌فرض (SQLite محلی) و کانکتورهای نمونهٔ توییتر و تلگرام است.

## گام‌های آماده‌سازی
1. ثبت‌نام کاربر مدیر:
   ```bash
   curl -X POST http://localhost:8000/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email":"admin@example.com","password":"secret","role":"admin"}'
   ```
2. ورود و دریافت توکن:
   ```bash
   ACCESS_TOKEN=$(curl -X POST http://localhost:8000/api/auth/login \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin@example.com&password=secret" | jq -r .access_token)
   ```
3. ساخت دو کانکتور فعال (توییتر و تلگرام):
   ```bash
   curl -X POST http://localhost:8000/api/connectors \
     -H "Authorization: Bearer $ACCESS_TOKEN" -H "Content-Type: application/json" \
     -d '{"type":"twitter","name":"X - مانیتور برند","config":{"keywords":["برند","کیفیت"]},"is_active":true}'

   curl -X POST http://localhost:8000/api/connectors \
     -H "Authorization: Bearer $ACCESS_TOKEN" -H "Content-Type: application/json" \
     -d '{"type":"telegram","name":"تلگرام - پشتیبانی","config":{"channels":["کانالالف","کانالب"]},"is_active":true}'
   ```
4. همگام‌سازی دستی هر کانکتور (تولید دادهٔ ساختگی و تحلیل):
   ```bash
   curl -X POST http://localhost:8000/api/connectors/1/sync
   curl -X POST http://localhost:8000/api/connectors/2/sync
   ```

## خروجی‌های نمونه API
### GET /api/dashboard/overview
```json
{
  "total_posts": 4,
  "sentiments": {
    "positive": 1,
    "negative": 1,
    "neutral": 2
  },
  "recent_posts": [
    {"id": 4, "source": "telegram", "author_name": "کانالب", "text": "پیام جدید از کانالب", "language": "fa", "like_count": 0, "share_count": 0, "comment_count": 0},
    {"id": 3, "source": "telegram", "author_name": "کانالالف", "text": "پیام جدید از کانالالف", "language": "fa", "like_count": 0, "share_count": 0, "comment_count": 0},
    {"id": 2, "source": "twitter", "author_name": "demo_user", "text": "کیفیت بد است", "language": "fa", "like_count": 2, "share_count": 1, "comment_count": 1},
    {"id": 1, "source": "twitter", "author_name": "demo_user", "text": "برند عالی است", "language": "fa", "like_count": 0, "share_count": 0, "comment_count": 0}
  ]
}
```

### GET /api/posts
خروجی پیش‌فرض (مرتب‌شده بر اساس زمان درج) مشابه زیر است:
```json
[
  {"id":4,"connector_id":2,"external_id":"tg-1","source":"telegram","author_name":"کانالب","text":"پیام جدید از کانالب","raw_text":"پیام جدید از کانالب","language":"fa","like_count":0,"share_count":0,"comment_count":0,"url":"https://t.me/demo"},
  {"id":3,"connector_id":2,"external_id":"tg-0","source":"telegram","author_name":"کانالالف","text":"پیام جدید از کانالالف","raw_text":"پیام جدید از کانالالف","language":"fa","like_count":0,"share_count":0,"comment_count":0,"url":"https://t.me/demo"},
  {"id":2,"connector_id":1,"external_id":"tw-1","source":"twitter","author_name":"demo_user","text":"کیفیت بد است","raw_text":"کیفیت بد است","language":"fa","like_count":2,"share_count":1,"comment_count":1,"url":"https://twitter.com/demo"},
  {"id":1,"connector_id":1,"external_id":"tw-0","source":"twitter","author_name":"demo_user","text":"برند عالی است","raw_text":"برند عالی است","language":"fa","like_count":0,"share_count":0,"comment_count":0,"url":"https://twitter.com/demo"}
]
```

### GET /api/connectors
بعد از ایجاد کانکتورها:
```json
[
  {"id":1,"type":"twitter","name":"X - مانیتور برند","config":{"keywords":["برند","کیفیت"]},"is_active":true},
  {"id":2,"type":"telegram","name":"تلگرام - پشتیبانی","config":{"channels":["کانالالف","کانالب"]},"is_active":true}
]
```

### GET /api/recommendations
پس از اجرای زمان‌بندی (یا اولین اجرای برنامه که APScheduler را فعال می‌کند)، نمونه خروجی:
```json
[
  {"id":1,"type":"reply_priority","data":{"post_id":2,"reason":"منفی با تعامل بالا"}},
  {"id":2,"type":"best_time_to_post","data":{"source":"twitter","slots":["10:00","14:00","20:00"]}},
  {"id":3,"type":"trending_topic","data":{"category":"عمومی","growth_pct":120}}
]
```

### GET /api/alerts
در صورتی که سهم پست‌های منفی در یک ساعت اخیر زیاد باشد:
```json
[
  {"id":1,"level":"warning","message":"در یک ساعت گذشته بیش از 50٪ پست‌ها منفی بوده‌اند","data":{"window_minutes":60,"negative_ratio":0.55},"is_seen":false}
]
```

## نمای فرانت‌اند
با اجرای `npm install && npm run dev` در پوشهٔ `frontend` و روشن بودن API، صفحهٔ اصلی داشبورد کارت‌های خلاصه (تعداد کل پست‌ها، احساسات مثبت/منفی)، جدول آخرین پست‌ها و بخش «پیشنهادات ساده» را به زبان فارسی نشان می‌دهد.
