# نقشه راه توسعه ربات مدیریت کانال تلگرام

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
- [x] تست و اطمینان از پایداری سیستم
  - [x] تست موفق در ویندوز و لینوکس
  - [x] بهبود مدیریت خطاها
  - [x] به‌روزرسانی مستندات راهنما
- [x] بهبود ساختار کد و لاگینگ
  - [x] پیاده‌سازی سیستم لاگینگ جامع
  - [x] بهبود ساختار هندلرهای دستورات
  - [x] مدیریت بهتر خطاها و استثناها

## فاز 2: استخراج اعضای کانال
- [ ] طراحی سیستم استخراج با بسته‌های 200 تایی
  - [ ] پیاده‌سازی GetParticipants با محدودیت 200 نفر
  - [ ] سیستم صف‌بندی درخواست‌ها
  - [ ] مدیریت وقفه بین درخواست‌ها
- [ ] مدیریت محدودیت‌های تلگرام
  - [ ] پیاده‌سازی سیستم FloodWait
  - [ ] مدیریت خطاهای دسترسی
  - [ ] سیستم تلاش مجدد خودکار
- [ ] ذخیره‌سازی در دیتابیس موجود
  - [ ] بهینه‌سازی ساختار دیتابیس
  - [ ] اضافه کردن جداول مورد نیاز
  - [ ] پیاده‌سازی عملیات Batch Insert
- [ ] پیاده‌سازی ConversationHandler برای مدیریت خطا
  - [ ] طراحی فرآیند گام به گام استخراج
  - [ ] نمایش پیشرفت عملیات
  - [ ] امکان توقف و ادامه فرآیند
- [ ] ایجاد فایل خروجی و ارسال به کاربر
  - [ ] پشتیبانی از فرمت‌های CSV و Excel
  - [ ] فیلترینگ و مرتب‌سازی داده‌ها
  - [ ] امکان انتخاب فیلدهای خروجی

### ساختار دیتابیس پیشنهادی برای استخراج اعضا
```sql
-- اضافه کردن به جدول channels
ALTER TABLE channels ADD COLUMN last_export_date TIMESTAMP;
ALTER TABLE channels ADD COLUMN total_members INT;
ALTER TABLE channels ADD COLUMN last_export_status TEXT;
ALTER TABLE channels ADD COLUMN export_in_progress BOOLEAN DEFAULT FALSE;

-- جدول جدید برای اعضای استخراج شده
CREATE TABLE channel_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel_id TEXT,
    user_id INTEGER,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    phone TEXT,
    is_bot BOOLEAN,
    is_premium BOOLEAN,
    joined_date TIMESTAMP,
    last_seen_date TIMESTAMP,
    export_date TIMESTAMP,
    status TEXT, -- member, admin, creator
    FOREIGN KEY (channel_id) REFERENCES channels(channel_id)
);

CREATE INDEX idx_channel_members_user ON channel_members(channel_id, user_id);
CREATE INDEX idx_channel_members_export ON channel_members(export_date);

-- جدول برای نگهداری وضعیت استخراج
CREATE TABLE export_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel_id TEXT,
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    total_exported INT,
    status TEXT, -- running, completed, failed, paused
    last_offset INT,
    error_message TEXT,
    batch_size INT DEFAULT 200,
    retry_count INT DEFAULT 0,
    next_retry_time TIMESTAMP,
    FOREIGN KEY (channel_id) REFERENCES channels(channel_id)
);

CREATE INDEX idx_export_sessions_channel ON export_sessions(channel_id);
CREATE INDEX idx_export_sessions_status ON export_sessions(status);

-- جدول برای نگهداری آمار و گزارشات
CREATE TABLE export_statistics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel_id TEXT,
    export_session_id INTEGER,
    total_members INT,
    active_members INT,
    bot_count INT,
    premium_users INT,
    export_duration INT, -- in seconds
    success_rate FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (channel_id) REFERENCES channels(channel_id),
    FOREIGN KEY (export_session_id) REFERENCES export_sessions(id)
);
```

## فاز 3: سیستم ارسال تبلیغات
- [ ] مدیریت چند اکانت
  - [ ] ذخیره‌سازی اطلاعات اکانت‌ها
  - [ ] سیستم سوئیچ خودکار بین اکانت‌ها
- [ ] مدیریت ارسال پیام
  - [ ] تنظیم سرعت ارسال
  - [ ] مدیریت محدودیت‌ها
  - [ ] تشخیص ریپورت و بلاک
- [ ] سیستم گزارش‌گیری
  - [ ] آمار ارسال موفق
  - [ ] آمار خطاها و ریپورت‌ها

### ساختار دیتابیس پیشنهادی برای سیستم تبلیغات
```sql
CREATE TABLE user_accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone TEXT UNIQUE,
    session_file TEXT,
    is_active BOOLEAN,
    last_used TIMESTAMP,
    daily_sends INT,
    total_sends INT,
    is_limited BOOLEAN
);

CREATE TABLE advertising_campaigns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    message_text TEXT,
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    status TEXT,
    total_target INT,
    successful_sends INT,
    failed_sends INT
);

CREATE TABLE message_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id INTEGER,
    user_account_id INTEGER,
    target_user_id INTEGER,
    send_date TIMESTAMP,
    status TEXT,
    error_message TEXT,
    FOREIGN KEY (campaign_id) REFERENCES advertising_campaigns(id),
    FOREIGN KEY (user_account_id) REFERENCES user_accounts(id)
);
```

## فاز 4: رابط کاربری
- [ ] طراحی منوهای inline
- [ ] اضافه کردن دکمه‌های شیشه‌ای
- [ ] بهبود پیام‌های راهنما
- [ ] اضافه کردن تصاویر و ایموجی‌های مناسب

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
