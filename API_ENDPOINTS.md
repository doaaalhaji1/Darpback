# Darbak Travel API — API_ENDPOINTS

## 1. معلومات عامة

اسم النظام: دربك — نظام ذكي لإدارة النقل العام بين المحافظات

Backend: Django + Django REST Framework

Authentication: JWT

Base URL:

http://127.0.0.1:8000
جميع روابط الـ API تبدأ بـ:

/api/
---

# 2. أنواع المستخدمين

النظام يحتوي على أربعة أنواع رئيسية:

| User Type          | الوصف            |
| ------------------ | ---------------- |
| PASSENGER        | المسافر          |
| BOOKING_EMPLOYEE | موظف الحجز       |
| COMPANY_MANAGER  | مسؤول شركة النقل |
| SYSTEM_ADMIN     | مسؤول النظام     |

---

# 3. المصادقة Authentication

## 3.1 الحصول على Access Token

### Endpoint

POST /api/token/
### الاستخدام

تسجيل الدخول والحصول على:

* Access Token
* Refresh Token

### Body

{
    "username": "username",
    "password": "password"
}
### Response

{
    "refresh": "JWT_REFRESH_TOKEN",
    "access": "JWT_ACCESS_TOKEN"
}
### استخدام Access Token

في الطلبات التي تحتاج مصادقة:

Authorization: Bearer JWT_ACCESS_TOKEN
---

# 4. تحديث Access Token

### Endpoint

POST /api/token/refresh/
### Body

{
    "refresh": "JWT_REFRESH_TOKEN"
}
### Response

{
    "access": "NEW_ACCESS_TOKEN"
}
---

# 5. تسجيل مستخدم جديد

### Endpoint

POST /api/register/
### Authentication

لا يحتاج تسجيل دخول.

### المستخدم الناتج

التسجيل العام ينشئ مستخدمًا من النوع:

PASSENGER
### Body

{
    "username": "ahmad",
    "first_name": "Ahmad",
    "last_name": "Ali",
    "phone": "0999999999",
    "email": "ahmad@example.com",
    "password": "Password123",
    "gender": "MALE"
}
### Gender

القيم المسموحة:

MALE
FEMALE
### Response

يتم إنشاء:

* User
* PassengerProfile

---

# 6. الملف الشخصي

## 6.1 عرض الملف الشخصي

### Endpoint

GET /api/profile/
### Authentication

مطلوب.

### Header

Authorization: Bearer ACCESS_TOKEN
### Response

{
    "id": 1,
    "username": "ahmad",
    "user_type": "PASSENGER",
    "gender": "MALE"
}
---

# 7. ملف المسافر

## 7.1 تحديث جنس المسافر

### Endpoint

POST /api/passenger-profile/
### Authentication

مطلوب.

### يسمح فقط لـ

PASSENGER
### Body

{
    "gender": "MALE"
}
أو:

{
    "gender": "FEMALE"
}
### Response

{
    "message": "Passenger profile updated successfully."
}
---

# 8. شركات النقل

## 8.1 عرض جميع شركات النقل

### Endpoint

GET /api/companies/
### Authentication

مطلوب.

### Response

مثال:

[
    {
        "id": 1,
        "company_name": "شركة الشام للنقل",
        "phone": "0111234567",
        "description": "شركة نقل بين المحافظات",
        "manager": 5
    }
]
---

# 9. مدن ومحافظات النظام

## 9.1 عرض المدن

### Endpoint

GET /api/cities/
### Authentication

حسب إعدادات الـ View الحالية.

### Response

[
    {
        "id": 1,
        "city_name": "دمشق"
    },
    {
        "id": 2,
        "city_name": "حلب"
    }
]
---

# 10. شركة المستخدم

## 10.1 عرض الشركة التي يديرها المستخدم

### Endpoint

GET /api/my-company/
### Authentication

مطلوب.

### يسمح لـ

COMPANY_MANAGER
SYSTEM_ADMIN
### Response

مثال:

{
    "id": 1,
    "company_name": "شركة الشام للنقل",
    "phone": "0111234567",
    "description": "شركة نقل بين المحافظات",
    "manager": 5
}
---

# 11. الرحلات

## 11.1 عرض الرحلات

### Endpoint

GET /api/trips/
### Authentication

حسب إعدادات النظام.

### Response

يعرض الرحلات المتاحة وفق Serializer الخاص بالرحلات.

---

# 12. تفاصيل رحلة

### Endpoint

GET /api/trips/<id>/
مثال:

GET /api/trips/5/
### الاستخدام

عرض تفاصيل رحلة محددة.

---

# 13. البحث عن الرحلات

### Endpoint

GET /api/trips/search/
### الاستخدام

البحث عن الرحلات حسب معايير البحث الموجودة في النظام.

مثال:

GET /api/trips/search/?from_city=1&to_city=2
> أسماء معاملات البحث تعتمد على الحقول الموجودة في TripSearchAPIView.

---

# 14. إنشاء رحلة

### Endpoint

POST /api/trips/create/
### Authentication

مطلوب.

### الصلاحية

يجب أن يكون المستخدم مخولًا بإنشاء الرحلات حسب إعدادات الـ View.

### Body

يعتمد على TripSerializer.

مثال عام:

{
    "company": 1,
    "departure_city": 1,
    "arrival_city": 2,
    "departure_time": "2026-08-20T10:00:00",
    "arrival_time": "2026-08-20T14:00:00",
    "price": 150000
}
> يجب استخدام أسماء الحقول الفعلية الموجودة في Serializer الخاص بـ Trip.

---

# 15. تعديل رحلة

### Endpoint

PUT /api/trips/<id>/update/
أو:

PATCH /api/trips/<id>/update/
### مثال

PATCH /api/trips/5/update/
---

# 16. حذف رحلة

### Endpoint

DELETE /api/trips/<id>/delete/
مثال:

DELETE /api/trips/5/delete/
---

# 17. الحجوزات

## 17.1 إنشاء حجز

### Endpoint

POST /api/bookings/create/
### Authentication

مطلوب.

### Body

{
    "trip": 5,
    "seat_number": 12
}
### العمليات التي تتم عند إنشاء الحجز

النظام يقوم بـ:

1. التحقق من البيانات.
2. إنشاء الحجز.
3. إنشاء QR Code.
4. إنشاء Invoice.
5. تخفيض عدد المقاعد المتاحة.

### Response

يعيد بيانات الحجز.

---

# 18. عرض جميع الحجوزات

### Endpoint

GET /api/bookings/
### Authentication

مطلوب.

### الصلاحية الحالية

SYSTEM_ADMIN
### ملاحظة

هذا endpoint يعرض الحجوزات وفق QuerySet الموجود في:

BookingListAPIView
والنسخة الحالية تستخدم:

Booking.objects.all()
لذلك مسؤول النظام يستطيع رؤية جميع الحجوزات.

---

# 19. تفاصيل حجز

### Endpoint

GET /api/bookings/<id>/
مثال:

GET /api/bookings/10/
### الاستخدام

عرض تفاصيل حجز محدد.

---

# 20. إلغاء حجز

### Endpoint

POST /api/bookings/<id>/cancel/
### Authentication

مطلوب.

### الصلاحيات

يسمح حاليًا:

* للمستخدم صاحب الحجز بإلغاء حجزه.
* لمسؤول النظام بإلغاء أي حجز.

### Response

{
    "message": "Cancelled Successfully"
}
---

# 21. حجوزاتي

### Endpoint

GET /api/my-bookings/
### Authentication

مطلوب.

### الوظيفة

يعرض الحجوزات الخاصة بالمستخدم الحالي فقط.

### QuerySet

Booking.objects.filter(
    user=request.user
)
---

# 22. الحجز الجماعي

### Endpoint

POST /api/bookings/group-create/
### Authentication

مطلوب.

### Body

مثال:

{
    "trip": 5,
    "seat_numbers": [10, 11, 12]
}
### الوظيفة

إنشاء عدة حجوزات في عملية واحدة.

### النظام يتحقق من:

* وجود الرحلة.
* صحة أرقام المقاعد.
* عدم تجاوز سعة المركبة.
* عدم حجز المقعد مسبقًا.

---

# 23. حجز عن طريق موظف الحجز

### Endpoint

POST /api/employee/bookings/create/
### Authentication

مطلوب.

### يسمح فقط لـ

BOOKING_EMPLOYEE
### Body

مثال:

{
    "passenger_phone": "0999999999",
    "trip": 5,
    "seat_number": 10
}
### النظام يقوم بـ:

1. البحث عن المسافر بواسطة رقم الهاتف.
2. التأكد أنه PASSENGER.
3. التأكد أن الرحلة تابعة لشركة الموظف.
4. إنشاء الحجز.
5. إنشاء QR Code.
6. إنشاء Invoice.
7. تخفيض المقاعد المتاحة.

---

# 24. مقاعد الرحلة

### Endpoint

GET /api/trips/<trip_id>/seats/
مثال:

GET /api/trips/5/seats/
### Response

مثال:

{
    "trip_id": 5,
    "vehicle_type": "BUS",
    "capacity": 50,
    "booked_seats": [1, 2, 8],
    "available_seats": [3, 4, 5, 6, 7]
}
---

# 25. مخطط مقاعد الرحلة

### Endpoint

GET /api/trips/<trip_id>/layout/
مثال:

GET /api/trips/5/layout/
### Response

مثال:

{
    "trip_id": 5,
    "vehicle_type": "BUS",
    "layout": [
        [
            {
                "seat_number": 1,
                "booked": false
            },
            {
                "seat_number": 2,
                "booked": true
            }
        ]
    ]
}
---

# 26. الفواتير

## 26.1 عرض الفواتير

### Endpoint

GET /api/invoices/
### Authentication

مطلوب.

### الاستخدام

عرض الفواتير حسب الصلاحيات الموجودة في InvoiceListAPIView.

---

# 27. تفاصيل فاتورة

### Endpoint
GET /api/invoices/<id>/
مثال:

GET /api/invoices/10/
---

# 28. دفع فاتورة

### Endpoint

POST /api/invoices/<id>/pay/
مثال:

POST /api/invoices/10/pay/
### الاستخدام

تغيير حالة الفاتورة إلى مدفوعة وفق منطق InvoicePayAPIView.

---

# 29. لوحة تحكم الشركة

## 29.1 Dashboard

### Endpoint

GET /api/dashboard/
### View

CompanyDashboardAPIView
### الوظيفة

عرض إحصائيات الشركة.

### المستوى

COMPANY_MANAGER
---

# 30. تقرير الإشغال للشركة

### Endpoint

GET /api/dashboard/occupancy/
### View

OccupancyReportAPIView
### الوظيفة

عرض نسبة إشغال الرحلات.

---

# 31. تقرير المدفوعات للشركة

### Endpoint

GET /api/dashboard/payments/
### View

PaymentsReportAPIView
### الوظيفة

عرض بيانات المدفوعات الخاصة بالشركة.

---

# 32. تقرير الإيرادات للشركة

### Endpoint

GET /api/dashboard/revenue/
### View

RevenueDashboardAPIView
### الوظيفة

عرض إيرادات الشركة.

---

# 33. الرحلات الأكثر طلبًا

### Endpoint

GET /api/dashboard/top-trips/
### View

TopTripsReportAPIView
### الوظيفة

عرض الرحلات الأكثر حجزًا داخل الشركة.

---

# 34. رحلات الشركة

### Endpoint

GET /api/my-company/trips/
### View

MyCompanyTripsAPIView
### الوظيفة

عرض الرحلات التابعة لشركة المدير الحالي.

---

# 35. حجوزات شركة المدير

### Endpoint

GET /api/my-company/bookings/
### Authentication

مطلوب.

### الصلاحية

COMPANY_MANAGER
### الوظيفة

عرض الحجوزات التابعة لشركة المدير فقط.

### ملاحظة مهمة

يجب أن يكون الفلترة على:

booking.trip.company == request.user.managed_company
أو العلاقة الفعلية الموجودة في المشروع.

---

# 36. إدارة المركبات

## المطلوب لمسؤول الشركة

مسؤول الشركة يجب أن يستطيع:

* عرض مركبات شركته.
* إضافة مركبة.
* تعديل مركبة.
* حذف مركبة.

### العمليات

GET    /api/my-company/vehicles/
POST   /api/my-company/vehicles/
PUT    /api/my-company/vehicles/<id>/
PATCH  /api/my-company/vehicles/<id>/
DELETE /api/my-company/vehicles/<id>/
### ملاحظة

هذه endpoints يجب أن تكون مرتبطة بشركة المدير الحالي، بحيث لا يستطيع مدير شركة تعديل مركبة لشركة أخرى.

---

# 37. إدارة موظفي الحجز

## المطلوب لمسؤول الشركة

مسؤول الشركة يجب أن يستطيع:

* عرض موظفي شركته.
* إنشاء موظف حجز.
* تعديل موظف.
* حذف موظف.

### العمليات

GET    /api/my-company/employees/
POST   /api/my-company/employees/
PUT    /api/my-company/employees/<id>/
PATCH  /api/my-company/employees/<id>/
DELETE /api/my-company/employees/<id>/
### User Type

الموظف يجب أن يكون:

BOOKING_EMPLOYEE
ويجب ربطه بالشركة:

company = Company Manager's Company
---

# 38. إدارة المستخدمين — System Admin

مسؤول النظام يجب أن يستطيع إدارة جميع المستخدمين.

### العمليات

GET    /api/admin/users/
POST   /api/admin/users/
GET    /api/admin/users/<id>/
PUT    /api/admin/users/<id>/
PATCH  /api/admin/users/<id>/
DELETE /api/admin/users/<id>/
### الصلاحية

SYSTEM_ADMIN
---

# 39. تغيير نوع المستخدم

### Endpoint المقترح

PATCH /api/admin/users/<id>/type/
### Body

مثال:

{
    "user_type": "COMPANY_MANAGER"
}
القيم:

PASSENGER
BOOKING_EMPLOYEE
COMPANY_MANAGER
SYSTEM_ADMIN
### الصلاحية

SYSTEM_ADMIN
---

# 40. إدارة شركات النقل — System Admin

مسؤول النظام يجب أن يستطيع:

GET    /api/admin/companies/
POST   /api/admin/companies/
GET    /api/admin/companies/<id>/
PUT    /api/admin/companies/<id>/
PATCH  /api/admin/companies/<id>/
DELETE /api/admin/companies/<id>/
---

# 41. إدارة المركبات — System Admin

مسؤول النظام يستطيع إدارة جميع المركبات:

GET    /api/admin/vehicles/
POST   /api/admin/vehicles/
GET    /api/admin/vehicles/<id>/
PUT    /api/admin/vehicles/<id>/
PATCH  /api/admin/vehicles/<id>/
DELETE /api/admin/vehicles/<id>/
---

# 42. جميع الحجوزات — System Admin

### Endpoint

GET /api/bookings/
### الصلاحية

SYSTEM_ADMIN
### الوظيفة

عرض جميع حجوزات النظام.

---
# 43. جميع الفواتير — System Admin

### Endpoint

GET /api/invoices/
### الصلاحية

SYSTEM_ADMIN
يجب أن تعرض جميع فواتير النظام، وليس فواتير مستخدم واحد فقط.

---

# 44. System-wide Dashboard

## 44.1 الإحصائيات العامة

### Endpoint

GET /api/admin/dashboard/
### الصلاحية

SYSTEM_ADMIN
### الوظيفة

يعرض إحصائيات النظام كاملًا، مثل:

* عدد المستخدمين.
* عدد المسافرين.
* عدد موظفي الحجز.
* عدد مدراء الشركات.
* عدد شركات النقل.
* عدد الرحلات.
* عدد الحجوزات.
* عدد الفواتير.

---

# 45. System-wide Occupancy

### Endpoint

GET /api/admin/dashboard/occupancy/
### الصلاحية

SYSTEM_ADMIN
### الوظيفة

عرض نسبة إشغال الرحلات على مستوى النظام كاملًا.

### Response

مثال:

[
    {
        "trip_id": 1,
        "company_id": 1,
        "company_name": "شركة الشام",
        "capacity": 50,
        "booked_seats": 20,
        "available_seats": 30,
        "occupancy_rate": 40.0
    }
]
---

# 46. System-wide Revenue

### Endpoint

GET /api/admin/dashboard/revenue/
### الصلاحية

SYSTEM_ADMIN
### الوظيفة

عرض الإيرادات على مستوى النظام كاملًا.

---

# 47. System-wide Payments

### Endpoint

GET /api/admin/dashboard/payments/
### الصلاحية

SYSTEM_ADMIN
### الوظيفة

عرض المدفوعات على مستوى النظام كاملًا.

---

# 48. System-wide Top Trips

### Endpoint

GET /api/admin/dashboard/top-trips/
### الصلاحية

SYSTEM_ADMIN
### الوظيفة

عرض الرحلات الأكثر حجزًا على مستوى النظام كاملًا.

---

# 49. صلاحيات المستخدمين

## Passenger

المسافر يستطيع:

POST /api/token/
POST /api/token/refresh/
POST /api/register/
GET  /api/profile/
POST /api/passenger-profile/
GET  /api/trips/
GET  /api/trips/<id>/
GET  /api/trips/search/
POST /api/bookings/create/
POST /api/bookings/group-create/
GET  /api/my-bookings/
POST /api/bookings/<id>/cancel/
GET  /api/trips/<trip_id>/seats/
GET  /api/trips/<trip_id>/layout/
GET  /api/invoices/
GET  /api/invoices/<id>/
POST /api/invoices/<id>/pay/
---

# 50. Booking Employee

موظف الحجز يستطيع:

POST /api/token/
POST /api/token/refresh/
GET  /api/profile/
GET  /api/trips/
GET  /api/trips/<id>/
GET  /api/trips/search/
POST /api/employee/bookings/create/
GET  /api/trips/<trip_id>/seats/
GET  /api/trips/<trip_id>/layout/
ويجب ألا يستطيع إنشاء حجز لرحلة تابعة لشركة أخرى.

---

# 51. Company Manager

مسؤول الشركة يستطيع:

POST /api/token/
POST /api/token/refresh/
GET  /api/profile/
GET  /api/my-company/
GET  /api/my-company/trips/
GET  /api/my-company/bookings/
GET  /api/dashboard/
GET  /api/dashboard/occupancy/
GET  /api/dashboard/payments/
GET  /api/dashboard/revenue/
GET  /api/dashboard/top-trips/
بالإضافة إلى إدارة:

Vehicles
Employees
Trips
Company Bookings
ضمن شركته فقط.

---

# 52. System Admin

مسؤول النظام يستطيع:

POST /api/token/
POST /api/token/refresh/

GET    /api/profile/

GET    /api/bookings/
GET    /api/bookings/<id>/

GET    /api/invoices/
GET    /api/invoices/<id>/

GET    /api/admin/users/
POST   /api/admin/users/
GET    /api/admin/users/<id>/
PUT    /api/admin/users/<id>/
PATCH  /api/admin/users/<id>/
DELETE /api/admin/users/<id>/

GET    /api/admin/companies/
POST   /api/admin/companies/
GET    /api/admin/companies/<id>/
PUT    /api/admin/companies/<id>/
PATCH  /api/admin/companies/<id>/
DELETE /api/admin/companies/<id>/

GET    /api/admin/vehicles/
POST   /api/admin/vehicles/
GET    /api/admin/vehicles/<id>/
PUT    /api/admin/vehicles/<id>/
PATCH  /api/admin/vehicles/<id>/
DELETE /api/admin/vehicles/<id>/

PATCH  /api/admin/users/<id>/type/

GET    /api/admin/dashboard/
GET    /api/admin/dashboard/occupancy/
GET    /api/admin/dashboard/revenue/
GET    /api/admin/dashboard/payments/
GET    /api/admin/dashboard/top-trips/
---

# 53. HTTP Status Codes
| Code  | المعنى                                  |
| ----- | --------------------------------------- |
| 200 | العملية نجحت                            |
| 201 | تم إنشاء مورد جديد                      |
| 400 | البيانات المرسلة غير صحيحة              |
| 401 | غير مصادق / Token غير موجود أو غير صالح |
| 403 | المستخدم ليس لديه الصلاحية              |
| 404 | العنصر غير موجود                        |
| 500 | خطأ داخلي في السيرفر                    |

---

# 54. أخطاء Authentication الشائعة

## Authentication credentials were not provided

{
    "detail": "Authentication credentials were not provided."
}
الحل:

Authorization: Bearer ACCESS_TOKEN
---

## No active account found

{
    "detail": "No active account found with the given credentials"
}
يعني أن بيانات تسجيل الدخول غير صحيحة أو أن المستخدم غير فعال.

---

## Permission denied

{
    "detail": "You do not have permission to perform this action."
}
يعني أن المستخدم مسجل الدخول، لكن user_type الخاص به لا يسمح بالوصول إلى الـ endpoint.

---

# 55. قواعد الأمان

## JWT

لا يتم إرسال كلمة المرور مع كل Request.

يتم تسجيل الدخول مرة واحدة:

POST /api/token/
ثم استخدام:

Authorization: Bearer ACCESS_TOKEN
---

# 56. قاعدة ملكية البيانات

## Company Manager

يجب أن يرى ويعدل بيانات شركته فقط.

مثال:

Company A Manager
        ↓
Company A Vehicles
Company A Employees
Company A Trips
Company A Bookings
ولا يستطيع الوصول إلى:

Company B Vehicles
Company B Employees
Company B Trips
Company B Bookings
---

# 57. System Admin

مسؤول النظام يعمل على مستوى النظام كاملًا:

System
 ├── Users
 ├── Companies
 ├── Vehicles
 ├── Trips
 ├── Bookings
 ├── Invoices
 └── Reports
---

# 58. العلاقة بين العمليات

تسلسل الحجز الطبيعي:

Login
  ↓
GET Trips
  ↓
GET Trip Details
  ↓
GET Seat Layout
  ↓
Select Seat
  ↓
POST Booking
  ↓
Generate QR
  ↓
Create Invoice
  ↓
Payment
---

# 59. تسلسل تسجيل المستخدم

POST /api/register/
        ↓
User Created
        ↓
PassengerProfile Created
        ↓
POST /api/token/
        ↓
Access Token
        ↓
GET /api/profile/
---

# 60. تسلسل موظف الحجز

Login
  ↓
Employee Token
  ↓
GET Trips
  ↓
Select Trip
  ↓
Enter Passenger Phone
  ↓
Select Seat
  ↓
POST /api/employee/bookings/create/
  ↓
Booking
  ↓
QR Code
  ↓
Invoice
---

# 61. تسلسل Company Manager

Login
  ↓
GET /api/my-company/
  ↓
GET /api/my-company/trips/
  ↓
GET /api/my-company/bookings/
  ↓
Dashboard
  ├── Revenue
  ├── Occupancy
  ├── Payments
  └── Top Trips
---

# 62. تسلسل System Admin

Login
  ↓
System Admin Token
  ↓
Users
  ↓
Companies
  ↓
Vehicles
  ↓
Trips
  ↓
Bookings
  ↓
Invoices
  ↓
System Dashboard
  ├── Revenue
  ├── Occupancy
  ├── Payments
  └── Top Trips
---

# 63. ملاحظات مهمة للمطور Frontend

الـ Frontend يجب ألا يعتمد على أسماء العلاقات بدل IDs عند إرسال البيانات.

مثال صحيح:

{
    "company": 1,
    "trip": 5,
    "seat_number": 12
}
أي أن العلاقات يتم إرسالها بواسطة:

ID
أما عند العرض للمستخدم فيمكن إظهار:

شركة الشام
بدل:

1
---

# 64. قاعدة التعامل مع IDs

### Request

يستخدم:

{
    "trip": 5
}
### Response

يمكن أن يحتوي:

{
    "trip": 5
}
أو Serializer مخصص يمكنه عرض بيانات الرحلة بشكل أوسع.

لكن الـ ID هو المفتاح الأساسي للعلاقات داخل قاعدة البيانات.

---

# 65. ملاحظة عن حالة الـ API

الـ endpoints التالية موجودة فعليًا في المشروع حسب الـ URL configuration الذي تم توثيقه:

`text
/api/bookings/
/api/bookings/<int:pk>/
/api/bookings/<int:pk>/cancel/
/api/bookings/create/
/api/bookings/group-create/
/api/dashboard/
/api/dashboard/occupancy/
/api/dashboard/payments/
/api/dashboard/revenue/
/api/dashboard/top-trips/
/api/employee/bookings/create/
/api/invoices/
/api/invoices/<int:pk>/
/api/invoices/<int:pk>/pay/
/api/my-bookings/
/api/my-company/
/api/my-company/trips/
/api/passenger-profile/
/api/profile/
/api/register/
/api/token/
/api/token/refresh/
/api/trips/
/api/trips/<int:pk>/
/api/trips/<int:pk>/delete/
/api/trips/<int:pk>/update/
/api/trips/<int:pk>/layout/
/api/trips/<int:pk>/seats/
/api/trips/create/
/api/trips/search/

أما endpoints الإدارة التالية:

text
/api/admin/users/
/api/admin/companies/
/api/admin/vehicles/
/api/admin/users/<id>/type/

فهي **جزء من متطلبات النظام التي يجب تنفيذها** وليست ضمن قائمة الـ URLs الأصلية التي أرسلتها.

وبالمثل:

text
/api/admin/dashboard/
/api/admin/dashboard/occupancy/
/api/admin/dashboard/revenue/
/api/admin/dashboard/payments/
/api/admin/dashboard/top-trips/

هي endpoints خاصة بالـ **System-wide Dashboard** التي نعمل عليها.

---

# 66. قاعدة مهمة

لا يعتبر وجود endpoint في هذا الملف دليلًا على أنه منفذ في Backend.

للتأكد من وجود أي Endpoint:

1. افتح `urls.py`.
2. ابحث عن `path`.
3. تأكد من الـ View المرتبط به.
4. اختبره باستخدام Postman.
5. تأكد من الصلاحيات.
6. تأكد من Response.

---

# 67. Endpoints الرئيسية الجاهزة للاختبار

text
POST /api/token/
POST /api/token/refresh/

POST /api/register/

GET /api/profile/
POST /api/passenger-profile/

GET /api/companies/
GET /api/my-company/

GET /api/trips/
GET /api/trips/<id>/
GET /api/trips/search/
POST /api/trips/create/
PUT/PATCH /api/trips/<id>/update/
DELETE /api/trips/<id>/delete/

POST /api/bookings/create/
POST /api/bookings/group-create/
GET /api/bookings/
GET /api/bookings/<id>/
POST /api/bookings/<id>/cancel/
GET /api/my-bookings/

POST /api/employee/bookings/create/

GET /api/trips/<trip_id>/seats/
GET /api/trips/<trip_id>/layout/

GET /api/invoices/
GET /api/invoices/<id>/
POST /api/invoices/<id>/pay/

GET /api/my-company/trips/

GET /api/dashboard/
GET /api/dashboard/occupancy/
GET /api/dashboard/payments/
GET /api/dashboard/revenue/
GET /api/dashboard/top-trips/

GET /api/admin/dashboard/
GET /api/admin/dashboard/occupancy/
GET /api/admin/dashboard/revenue/
GET /api/admin/dashboard/payments/
GET /api/admin/dashboard/top-trips/
`

# End of Darbak API Documentation