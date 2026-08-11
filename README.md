# 🕶️ SMS Bomber Pro

<p align="center">
  <img src="https://img.shields.io/github/license/mehrdadmb2/SMS-Bomber-Pro?style=flat-square&color=blue" alt="License">
  <img src="https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/version-2.0.0-brightgreen?style=flat-square" alt="Version">
  <img src="https://img.shields.io/github/stars/mehrdadmb2/SMS-Bomber-Pro?style=social" alt="Stars">
  <img src="https://img.shields.io/github/forks/mehrdadmb2/SMS-Bomber-Pro?style=social" alt="Forks">
</p>

<p align="center">
  <b>ابزاری دوگانه (Python GUI + Web App) برای آموزش تست نفوذ و ارزیابی امنیتی سرویس‌های OTP پیامکی ایران</b><br>
  <sub>🚫 <b>فقط برای اهداف آموزشی و تست مجاز – سوءاستفاده اکیداً ممنوع</b></sub>
</p>

---

## ❗ هشدار حقوقی و اخلاقی (حتماً بخوانید)

<div style="background-color:#ffdddd; border-left:6px solid #f44336; padding:15px; margin:20px 0; border-radius:5px;">
<strong>⚠️ این نرم‌افزار صرفاً جهت آموزش، تحقیق و تست نفوذ مجاز توسعه یافته است.</strong><br>
هرگونه استفاده برای آزار، اسپم، ارسال پیامک ناخواسته به دیگران یا نقض حریم خصوصی <b>غیرقانونی و غیراخلاقی</b> می‌باشد.
مسئولیت هرگونه سوءاستفاده کاملاً بر عهدهٔ کاربر است و توسعه‌دهنده هیچ مسئولیتی نمی‌پذیرد.
<b>لطفاً تنها روی شمارهٔ خودتان یا با اجازهٔ کتبی مالک شماره آزمایش کنید.</b>
</div>

---

## 📑 فهرست مطالب

- [ویژگی‌های کلی](#ویژگیهای-کلی)
- [نسخهٔ پایتون (GUI)](#نسخهٔ-پایتون-gui)
  - [پیش‌نیازها و اجرا](#پیشنیازها-و-اجرا)
  - [شخصی‌سازی](#شخصیسازی)
  - [ساخت EXE](#ساخت-exe)
- [نسخهٔ تحت وب (Matrix Ultra)](#نسخهٔ-تحت-وب-matrix-ultra)
  - [راه‌اندازی پروکسی Cloudflare Worker](#راهاندازی-پروکسی-cloudflare-worker)
  - [اجرای اپلیکیشن](#اجرای-اپلیکیشن)
  - [تنظیم کلید دسترسی](#تنظیم-کلید-دسترسی)
  - [راهنمای بخش‌ها](#راهنمای-بخشها)
- [لیست APIها](#لیست-apiها)
- [رفع مشکلات رایج](#رفع-مشکلات-رایج)
- [مشارکت](#مشارکت)
- [مجوز](#مجوز)

---

## ویژگی‌های کلی

- ✅ **دو نسخهٔ متفاوت**: یکی برای دسکتاپ با Python/CustomTkinter و دیگری تحت وب با HTML/CSS/JS.
- 🧪 **تست سریع**: دکمهٔ «Test 10 SMS» در نسخهٔ وب برای اطمینان از عملکرد.
- ⚡ **کنترل نرخ دقیق**: Token Bucket با قابلیت تنظیم از ۱ تا ۲۰ درخواست در ثانیه.
- 🎯 **هدف موفق**: توقف خودکار پس از دریافت تعداد مشخصی پیامک موفق.
- 📊 **آمار و نمودار زنده**: نمایش لحظه‌ای کل، موفق، خطا، نرخ، درصد و زمان باقی‌مانده (وب: نمودار Chart.js).
- 💾 **پروفایل‌ها**: ذخیره و بازیابی تنظیمات در مرورگر (IndexedDB) یا جلسهٔ کاری.
- 🌐 **پروکسی ابری**: استفاده از Cloudflare Worker برای عبور از محدودیت CORS.
- 🌙 **تم تیره/روشن** و حالت تمام‌صفحه.
- 🇮🇷🇬🇧 **پشتیبانی از زبان فارسی و انگلیسی** با چیدمان راست‌چین خودکار.
- 📝 **لاگ کامل** تمام درخواست‌ها.
- 🔐 **محافظت با کلید دسترسی** (در نسخهٔ وب).

---

## نسخهٔ پایتون (GUI)

### پیش‌نیازها و اجرا
- پایتون ۳.۸ یا بالاتر
- کلیه کتابخانه‌ها به‌طور خودکار نصب می‌شوند (`requests`, `customtkinter`).  
  برای پروکسی SOCKS5 نیز `PySocks` نصب می‌گردد.

```bash
# کلون کردن ریپو
git clone https://github.com/mehrdadmb2/SMS-Bomber-Pro.git
cd SMS-Bomber-Pro

# اجرای برنامه
python sms_bomber_pro.py
```

### شخصی‌سازی
- **تغییر نرخ پیش‌فرض**: در کلاس `Engine` پارامتر `rate=5.0` را ویرایش کنید و در GUI خط `self.rate_slider.set(5)` را به روز کنید.
- **عنوان پنجره**: خط `self.title("SMS Bomber Pro - نسخه آموزشی")`.
- **فایل EXE**: در متد `build_exe` نام خروجی را تغییر دهید: `"--name", "SMS_Bomber_Pro"`.

### ساخت EXE
می‌توانید با کلیک روی دکمهٔ «🛠 ساخت فایل EXE» در برنامه، یا به صورت دستی:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name SMS_Bomber_Pro sms_bomber_pro.py
```
فایل اجرایی در پوشهٔ `dist` ایجاد می‌شود و بدون نیاز به پایتون قابل اجراست.

---

## نسخهٔ تحت وب (Matrix Ultra)

### راه‌اندازی پروکسی Cloudflare Worker
مرورگرها به‌دلیل محدودیت CORS نمی‌توانند مستقیماً به APIهای OTP درخواست دهند. یک پروکسی رایگان روی Cloudflare Workers دیپلوی کنید:

1. در [Cloudflare](https://dash.cloudflare.com/sign-up) ثبت‌نام کنید.
2. از بخش **Workers & Pages** یک Worker جدید بسازید.
3. کد زیر را جایگذاری کنید و **Save and Deploy** را بزنید:

```javascript
export default {
  async fetch(request) {
    if (request.method === 'POST') {
      try {
        const { url, method, headers, body } = await request.json();
        const cleanHeaders = {};
        for (const [k, v] of Object.entries(headers || {})) {
          if (!['host', 'origin', 'referer'].includes(k.toLowerCase())) {
            cleanHeaders[k] = v;
          }
        }
        const resp = await fetch(url, {
          method: method || 'GET',
          headers: cleanHeaders,
          body: method === 'POST' ? body : undefined,
        });
        const respHeaders = new Headers(resp.headers);
        respHeaders.set('Access-Control-Allow-Origin', '*');
        return new Response(resp.body, {
          status: resp.status,
          headers: respHeaders,
        });
      } catch (e) {
        return new Response(JSON.stringify({ error: e.message }), {
          status: 500,
          headers: { 'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json' },
        });
      }
    }
    return new Response('Send POST with {url, method, headers, body}', { status: 200 });
  },
};
```

4. آدرس داده‌شده (مثلاً `https://your-worker.workers.dev`) را در متغیر `DEFAULT_PROXY` در فایل `index.html` قرار دهید.

### اجرای اپلیکیشن
- فایل `index.html` را مستقیماً در مرورگر باز کنید یا روی **GitHub Pages** (یا هر هاست استاتیک) میزبانی کنید.
- شماره(های) مقصد را وارد کنید (با کاما، خط جدید یا آپلود فایل `.txt/.csv`).
- نرخ و هدف را تنظیم کنید.
- پروکسی را فعال و آدرس Worker را تأیید کنید.
- برای اطمینان از عملکرد، ابتدا روی **🧪 Test (10 SMS)** کلیک کنید.
- سپس **▶ Start** را بزنید.

### تنظیم کلید دسترسی
برای محافظت از ابزار در برابر دسترسی غیرمجاز، می‌توانید یک کلید عبور تعیین کنید:
- به انتهای URL پارامتر `?key=YOUR_SECRET` را اضافه کنید.  
- اگر این پارامتر وجود نداشته باشد، برنامه از شما کلید می‌خواهد.
- برای حذف موقت این قابلیت (فقط برای تست محلی)، خط مربوط به بررسی `key` را در توابع `startAttack` و `testAttack` حذف کنید.

### راهنمای بخش‌ها
- **Phone Numbers**: ورود شماره‌ها (09xxxxxxxxx) با جداکنندهٔ کاما یا خط جدید. پشتیبانی از بارگذاری فایل.
- **Rate**: درخواست در ثانیه (پیش‌فرض ۵). مقادیر پایین‌تر برای اینترنت ضعیف مناسب‌تر است.
- **Target**: تعداد موفق هدف؛ خالی = ادامه تا توقف دستی.
- **Scheduler**: تأخیر شروع به ثانیه.
- **Proxy**: آدرس Cloudflare Worker. باید فعال باشد.
- **Profiles**: ذخیره و بازیابی سریع تنظیمات (در مرورگر ذخیره می‌شود).
- **Test (10 SMS)**: ارسال ۱۰ درخواست آزمایشی به اولین شمارهٔ واردشده.
- **Chart**: نمایش زندهٔ روند موفق/خطا.

---

## لیست APIها
بیش از ۱۰۰ سرویس ایرانی برای ارسال کد تأیید (OTP) در کدها تعبیه شده است، از جمله:
دیجی‌کالا، دیوار، اسنپ، تپسی، علی‌بابا، نشان، بله، شیپور، ترب، فیدیبو، نماوا، ایسام، دیجی‌استایل، بانی‌مد، خانومی، ازکی، بیمه بازار و ...
برای افزودن API جدید کافیست یک دیکشنری/آبجکت مشابه به لیست در کد اضافه کنید.

---

## رفع مشکلات رایج

<details>
<summary><b>❌ خطای "Access key required in URL"</b></summary>
یعنی کلید عبور تنظیم شده است. به انتهای آدرس URL پارامتر <code>?key=YOUR_SECRET</code> را اضافه کنید.
</details>

<details>
<summary><b>❌ درخواست‌ها ارسال نمی‌شوند (CORS)</b></summary>
پروکسی Cloudflare Worker را به‌درستی دیپلوی کرده و آدرس آن را در فیلد پروکسی وارد کنید. همچنین مطمئن شوید تیک <b>Enable</b> فعال است.
</details>

<details>
<summary><b>❌ خطای اتصال در نسخهٔ پایتون</b></summary>
اتصال اینترنت را بررسی کنید. در صورت استفاده از پروکسی SOCKS5، کتابخانهٔ <code>PySocks</code> به‌طور خودکار نصب می‌شود؛ در غیر این صورت دستی نصب کنید: <code>pip install PySocks</code>.
</details>

<details>
<summary><b>❌ نرخ ارسال پایین‌تر از مقدار تنظیم‌شده است</b></summary>
Token Bucket نرخ را دقیقاً کنترل می‌کند. اگر سرعت اینترنت پایین باشد، نرخ مؤثر کمتر خواهد بود. می‌توانید نرخ را افزایش دهید، اما مراقب مسدود شدن IP باشید.
</details>

---

## مشارکت
پروژه صرفاً برای اهداف آموزشی و تحقیقاتی منتشر شده است. مشارکت‌های مفید شامل بهبود UI، افزایش پایداری و اضافه کردن APIهای معتبر جدید خوش‌آمد است.  
لطفاً پیش از ارسال Pull Request اهداف آموزشی را در نظر بگیرید و از افزودن کدهای مخرب بپرهیزید.

---

## مجوز
این پروژه تحت مجوز **MIT** منتشر می‌شود.  
توسعه‌دهنده هیچگونه مسئولیتی در قبال استفادهٔ نادرست یا غیرقانونی از این ابزار ندارد.

---

<p align="center">
  ساخته‌شده با ❤️ و Code | برای آموزش امنیت سایبری
</p>
