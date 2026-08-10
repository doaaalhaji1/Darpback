# Darbak Transportation System API Documentation

## Base URL

```http
http://127.0.0.1:8000/api/
```

---

# Authentication

## Register Passenger

### Endpoint

```http
POST /register/
```

### Body

```json
{
    "username": "ahmad",
    "first_name": "Ahmad",
    "last_name": "Ali",
    "phone": "0999999999",
    "password": "123456",
    "gender": "MALE"
}
```

---

## Login

### Endpoint

```http
POST /token/
```

### Body

```json
{
    "username": "ahmad",
    "password": "123456"
}
```

### Response

```json
{
    "refresh": "...",
    "access": "..."
}
```

---

## Refresh Token

### Endpoint

```http
POST /token/refresh/
```

### Body

```json
{
    "refresh": "..."
}
```

---

# User Profile

## Profile

```http
GET /profile/
```

### Response

```json
{
    "id": 1,
    "username": "ahmad",
    "user_type": "PASSENGER",
    "gender": "MALE"
}
```

---

## Passenger Profile

```http
GET /passenger-profile/
```

---

# Dashboard & Reports

## Company Dashboard

```http
GET /dashboard/
```

---

## Revenue Report

```http
GET /dashboard/revenue/
```

---

## Occupancy Report

```http
GET /dashboard/occupancy/
```

---

## Payments Report

```http
GET /dashboard/payments/
```

---

## Top Trips Report

```http
GET /dashboard/top-trips/
```

---

# Company

## My Company

```http
GET /my-company/
```

---

# Trips

## List Trips

```http
GET /trips/
```

---

## Search Trips

```http
GET /trips/search/
```

Example:

```http
GET /trips/search/?from_city=Damascus&to_city=Aleppo
```

---

## Trip Details

```http
GET /trips/{id}/
```

---

## Create Trip

```http
POST /trips/create/
```

---

## Update Trip

```http
PUT /trips/{id}/update/
```

---

## Delete Trip

```http
DELETE /trips/{id}/delete/
```

---

## Company Trips

```http
GET /my-company/trips/
```

---

# Seat Management

## Available Seats

```http
GET /trips/{trip_id}/seats/
```

### Response

```json
{
    "trip_id": 6,
    "capacity": 50,
    "booked_seats": [1,2,3],
    "available_seats": [4,5,6]
}
```

---

## Seat Layout

```http
GET /trips/{trip_id}/layout/
```

### Response

```json
{
    "trip_id": 6,
    "vehicle_type": "BUS",
    "layout": [
        [
            {
                "seat_number": 1,
                "booked": true
            },
            {
                "seat_number": 2,
                "booked": false
            }
        ]
    ]
}
```

---

# Booking

## Create Booking

```http
POST /bookings/create/
```

### Body

```json
{
    "trip": 6,
    "seat_number": 5
}
```

---

## Booking Details

```http
GET /bookings/{id}/
```

---

## List All Bookings

```http
GET /bookings/
```

---

## Cancel Booking

```http
POST /bookings/{id}/cancel/
```

---

## My Bookings

```http
GET /my-bookings/
```

---

# Group Booking

## Create Group Booking

```http
POST /bookings/group-create/
```

### Body

```json
{
    "trip": 6,
    "seat_numbers": [5,6,7]
}
```

---

# Booking Employee

## Create Booking For Passenger

```http
POST /employee/bookings/create/
```

### Body

```json
{
    "passenger_phone": "0999999999",
    "trip": 6,
    "seat_number": 8
}
```

### Rules

* Only BOOKING_EMPLOYEE can access.
* Employee must belong to the trip company.
* Gender validation is applied.
* Seat validation is applied.

---

# Invoices

## List Invoices

```http
GET /invoices/
```

---

## Invoice Details

```http
GET /invoices/{id}/
```

---

## Pay Invoice

```http
POST /invoices/{id}/pay/
```

---

# QR Code

QR Code is automatically generated after booking creation.

Example:

```json
{
    "qr_code": "/media/qr_codes/booking_15.png"
}
```

---

# Business Rules

## Booking Rules

* Seat duplication is not allowed.
* Only available trips can be booked.
* Available seats must be greater than zero.
* Group booking validates every selected seat.
* Employee booking validates passenger existence.

## Gender Rules

* Passenger gender is mandatory.
* Adjacent seat gender validation is applied.

## Invoice Rules

* Invoice is automatically created after booking.
* Invoice amount equals trip price.
* Payment status defaults to PENDING.

## QR Rules

* QR Code is automatically generated after successful booking.

---

# User Types

```text
PASSENGER
BOOKING_EMPLOYEE
COMPANY_MANAGER
SYSTEM_ADMIN
```

---

# Project Status

Backend Completion: 100%

Modules Implemented:

* Authentication
* Passenger Management
* Companies
* Vehicles
* Trips
* Trip Search
* Seat Layout
* Seat Availability
* Booking
* Group Booking
* Booking Employee
* Gender Validation
* QR Code
* Invoices
* Dashboard Reports
* Revenue Reports
* Occupancy Reports
* Payment Reports
* Top Trips Reports
