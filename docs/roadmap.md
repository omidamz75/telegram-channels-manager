# نقشه راه توسعه ربات استخراج و ارسال پیام تلگرام

## فاز 1: تکمیل سیستم احراز هویت ✅
- [x] رفع مشکل ارسال کد اولیه
  - [x] پیاده‌سازی احراز هویت از طریق کنسول
  - [x] حل مشکل ورود رمز در ویندوز
  - [x] بهبود پیام‌های راهنمای کاربر
- [x] پیاده‌سازی مدیریت رمز دو مرحله‌ای
  - [x] اضافه کردن پشتیبانی از 2FA
  - [x] بهبود پیام‌های راهنما
  - [x] مدیریت خطاهای احراز هویت
- [x] ذخیره‌سازی و مدیریت session
  - [x] استفاده از StringSession به جای فایل
  - [x] ذخیره‌سازی در .env و config/session.json
  - [x] حذف سیستم قدیمی مدیریت session
  - [x] اعتبارسنجی session در هر اجرا
- [x] بهبود ساختار کد و لاگینگ
  - [x] پیاده‌سازی سیستم لاگینگ جامع
  - [x] بهبود ساختار هندلرهای دستورات
  - [x] مدیریت بهتر خطاها و استثناها

## فاز 2: سیستم استخراج اعضا
- [x] پیاده‌سازی Channel Validator
  - [x] بررسی اعتبار لینک/آیدی کانال
  - [x] چک کردن دسترسی‌ها
  - [x] بررسی محدودیت‌های کانال
  - [x] برگرداندن اطلاعات اولیه کانال

- [ ] پیاده‌سازی Rate Limiter
  - [ ] مدیریت محدودیت‌های تلگرام
  - [ ] کنترل سرعت درخواست‌ها
  - [ ] مدیریت FloodWait
  - [ ] سیستم تلاش مجدد خودکار

- [ ] پیاده‌سازی Member Extractor
  - [ ] استخراج اعضا با بسته‌های 200 تایی
  - [ ] مدیریت وقفه بین درخواست‌ها
  - [ ] ذخیره وضعیت برای resume
  - [ ] گزارش پیشرفت عملیات

- [ ] پیاده‌سازی Data Storage
  - [ ] راه‌اندازی SQLite با ساختار جدید
  - [ ] ذخیره‌سازی batch اطلاعات
  - [ ] مدیریت وضعیت‌ها
  - [ ] کوئری‌های گزارش‌گیری

- [ ] پیاده‌سازی Export Manager
  - [ ] خروجی CSV و Excel
  - [ ] فیلترینگ و مرتب‌سازی
  - [ ] ارسال فایل به کاربر

## فاز 3: سیستم ارسال پیام
- [ ] مدیریت اکانت‌های ارسال کننده
  - [ ] افزودن و احراز هویت اکانت‌ها
  - [ ] مدیریت session ها
  - [ ] بررسی وضعیت و محدودیت‌ها

- [ ] سیستم ارسال پیام
  - [ ] دریافت و اعتبارسنجی متن پیام
  - [ ] تنظیم سرعت و محدودیت‌ها
  - [ ] توزیع پیام بین اکانت‌ها
  - [ ] مدیریت خطاها و محدودیت‌ها

- [ ] گزارش‌گیری و مانیتورینگ
  - [ ] آمار ارسال موفق
  - [ ] گزارش خطاها و محدودیت‌ها
  - [ ] وضعیت اکانت‌ها

## ساختار دیتابیس

### جداول استخراج اعضا
```sql
-- جدول برای مدیریت عملیات استخراج
CREATE TABLE extraction_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    target_id TEXT,           -- آیدی یا لینک کانال
    target_type TEXT,         -- نوع هدف (کانال، گروه و...)
    total_members INT,        -- تعداد کل اعضا
    extracted_count INT,      -- تعداد استخراج شده
    status TEXT,             -- وضعیت (در حال اجرا، متوقف، تکمیل شده)
    start_time TIMESTAMP,
    last_update TIMESTAMP,
    error_message TEXT,
    settings TEXT            -- تنظیمات استخراج (JSON)
);

-- جدول برای اعضای استخراج شده
CREATE TABLE extracted_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER,          -- ارتباط با عملیات استخراج
    user_id INTEGER,
    access_hash BIGINT,      -- برای ارسال پیام نیاز است
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    is_bot BOOLEAN,
    is_premium BOOLEAN,
    extracted_at TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES extraction_jobs(id)
);

-- جدول برای مدیریت وضعیت استخراج
CREATE TABLE extraction_state (
    job_id INTEGER,
    last_offset INTEGER,     -- آخرین offset برای ادامه استخراج
    last_batch_time TIMESTAMP,
    retry_count INTEGER,
    next_retry_time TIMESTAMP,
    batch_settings TEXT,     -- تنظیمات batch (JSON)
    FOREIGN KEY (job_id) REFERENCES extraction_jobs(id)
);
```

### جداول ارسال پیام
```sql
-- جدول اکانت‌های ارسال کننده
CREATE TABLE sender_accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone TEXT UNIQUE,
    session_string TEXT,
    is_active BOOLEAN,
    daily_limit INT,
    used_today INT,
    last_used TIMESTAMP,
    status TEXT,            -- وضعیت (فعال، محدود شده، بلاک و...)
    error_count INT,
    last_error TEXT
);

-- جدول عملیات‌های ارسال پیام
CREATE TABLE sending_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_text TEXT,
    target_count INT,       -- تعداد کل اعضای هدف
    sent_count INT,         -- تعداد ارسال شده
    failed_count INT,       -- تعداد خطا
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    status TEXT,
    settings TEXT          -- تنظیمات ارسال (JSON)
);

-- جدول لاگ ارسال پیام‌ها
CREATE TABLE message_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER,
    account_id INTEGER,
    user_id INTEGER,
    status TEXT,
    error_message TEXT,
    sent_at TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES sending_jobs(id),
    FOREIGN KEY (account_id) REFERENCES sender_accounts(id)
);
```

## اولویت‌بندی و زمان‌بندی
1. ✅ تکمیل سیستم احراز هویت (انجام شده)
   - پیاده‌سازی موفق احراز هویت از طریق کنسول
   - حل مشکلات 2FA و مدیریت session
   - بهبود امنیت و پایداری سیستم

2. 🔄 استخراج اعضا (3-4 هفته)
   - هفته 1: پیاده‌سازی سیستم پایه و مدیریت محدودیت‌ها
   - هفته 2: توسعه سیستم ذخیره‌سازی و پایگاه داده
   - هفته 3: پیاده‌سازی رابط کاربری و مدیریت خطاها
   - هفته 4: تست، بهینه‌سازی و مستندسازی

3. 📅 سیستم ارسال تبلیغات (4 هفته)
   - برنامه‌ریزی دقیق پس از تکمیل فاز 2

4. 📅 بهبود رابط کاربری (2 هفته)
   - برنامه‌ریزی دقیق پس از تکمیل فاز 3

## ملاحظات فنی برای فاز 2
1. مدیریت محدودیت‌ها
   - رعایت محدودیت 200 کاربر در هر درخواست
   - پیاده‌سازی تاخیر مناسب بین درخواست‌ها (حداقل 2 ثانیه)
   - مدیریت هوشمند FloodWait با افزایش تدریجی تاخیر

2. بهینه‌سازی عملکرد
   - استفاده از Batch Insert برای کاهش فشار بر دیتابیس
   - ذخیره‌سازی موقت داده‌ها در حافظه
   - پیاده‌سازی سیستم Resume برای توقف و ادامه فرآیند

3. مدیریت خطا
   - ثبت لاگ کامل خطاها و وضعیت‌ها
   - سیستم Retry با تاخیر افزایشی
   - ذخیره وضعیت برای بازیابی در صورت قطعی

4. امنیت و حفظ حریم خصوصی
   - رمزنگاری داده‌های حساس در دیتابیس
   - محدود کردن دسترسی به اطلاعات کاربران
   - پاک‌سازی خودکار داده‌های قدیمی

## نکات مهم
- تست مداوم در هر مرحله
- مستندسازی کد و API ها
- پشتیبان‌گیری منظم از دیتابیس
- رعایت محدودیت‌های تلگرام
- حفظ امنیت داده‌ها
- گزارش‌گیری و مانیتورینگ عملکرد
