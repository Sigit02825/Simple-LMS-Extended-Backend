# Simple LMS Extended Backend

Backend LMS sederhana berbasis Django REST Framework dengan PostgreSQL, JWT, Swagger, Redis, dan role `admin`, `instructor`, `student`.

## Fitur Utama

- Autentikasi JWT dengan endpoint login, refresh token, dan logout blacklist
- Role-based access untuk `admin`, `instructor`, dan `student`
- Endpoint `course`, `lesson`, `enrollment`, dan `lesson-progress`
- Rating, review, wishlist, search, filter, dan sorting course
- Dokumentasi API melalui Swagger dan ReDoc
- Docker Compose untuk menjalankan aplikasi, PostgreSQL, dan Redis
- Seed data akun demo dan data course

## Stack

- Python 3.11
- Django
- Django REST Framework
- Simple JWT
- PostgreSQL
- Redis
- drf-yasg
- Docker Compose

## Menjalankan Project

### Opsi 1: Docker Compose

1. Salin konfigurasi environment:

```powershell
Copy-Item .env.example .env
```

2. Jalankan seluruh service:

```powershell
docker-compose up --build
```

3. Akses aplikasi:
- API root: `http://localhost:8000/api/`
- Swagger: `http://localhost:8000/swagger/`
- ReDoc: `http://localhost:8000/redoc/`
- Django Admin: `http://localhost:8000/admin/`

### Opsi 2: Local Development

1. Buat virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependency:

```powershell
pip install -r requirements.txt
```

3. Salin environment:

```powershell
Copy-Item .env.example .env
```

4. Jika memakai PostgreSQL lokal atau Docker, sesuaikan isi `.env`.

5. Jalankan migration dan seed:

```powershell
python manage.py migrate
python manage.py seed_data
```

6. Jalankan server:

```powershell
python manage.py runserver
```

## Akun Demo

- Admin: `admin` / `admin12345`
- Instructor: `instructor` / `instructor12345`
- Student 1: `student1` / `student12345`
- Student 2: `student2` / `student12345`

## Endpoint Utama

- `POST /api/token/` untuk login JWT
- `POST /api/token/refresh/` untuk refresh access token
- `POST /api/logout/` untuk blacklist refresh token
- `GET /api/users/` untuk data user
- `GET /api/courses/` untuk daftar course
- `GET /api/lessons/` untuk daftar lesson yang boleh diakses user
- `GET /api/enrollments/` untuk daftar enrollment user
- `GET /api/lesson-progress/` untuk progress lesson
- `GET /swagger/` untuk dokumentasi interaktif

## Cara Authorize Di Swagger

1. Buka `POST /api/token/`
2. Masukkan username dan password akun demo
3. Salin nilai `access`
4. Klik tombol `Authorize` di Swagger
5. Isi field dengan format:

```text
Bearer <access_token>
```

## Catatan

- `seed_data` aman dijalankan berulang karena data demo dibuat idempotent.
- Registrasi publik melalui endpoint user otomatis membuat role `student`.
- Role `admin` dapat melihat semua data, `instructor` hanya data course miliknya, dan `student` hanya data yang menjadi hak aksesnya.
