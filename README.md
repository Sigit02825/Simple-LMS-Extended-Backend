# Simple LMS Extended Backend

Backend Learning Management System (LMS) berbasis Django REST Framework dengan autentikasi JWT, PostgreSQL, Redis, dokumentasi API, dan role `admin`, `instructor`, `student`.

## Ringkasan Fitur

- Login JWT, refresh token, dan logout blacklist
- Role-based access untuk `admin`, `instructor`, dan `student`
- Manajemen `course`, `lesson`, `enrollment`, dan `lesson progress`
- Rating, review, dan wishlist course
- Search, filter, sorting, dan pagination course
- Dokumentasi API melalui Swagger dan ReDoc
- Docker Compose untuk aplikasi, PostgreSQL, Redis, Celery, Beat, dan Flower
- Seed data untuk akun demo dan data course

## Stack Teknologi

- Python 3.11
- Django
- Django REST Framework
- Simple JWT
- PostgreSQL
- Redis
- drf-yasg
- Docker Compose
- Celery, Celery Beat, dan Flower

## Menjalankan Project

### Opsi 1: Docker Compose

```powershell
docker compose --env-file .env.example up -d --build
```

Setelah container aktif, buka:

- API Root: `http://localhost:8000/api/`
- Swagger: `http://localhost:8000/swagger/`
- ReDoc: `http://localhost:8000/redoc/`
- Django Admin: `http://localhost:8000/admin/`
- Flower: `http://localhost:5555/`

### Opsi 2: Local Development

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

## Akun Demo

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin12345` |
| Instructor | `instructor` | `instructor12345` |
| Student 1 | `student1` | `student12345` |
| Student 2 | `student2` | `student12345` |

## Endpoint Utama

- `POST /api/token/` untuk login JWT
- `POST /api/token/refresh/` untuk refresh access token
- `POST /api/logout/` untuk logout dan blacklist refresh token
- `GET /api/users/` untuk data user
- `GET /api/courses/` untuk daftar course
- `GET /api/lessons/` untuk daftar lesson yang dapat diakses
- `GET /api/enrollments/` untuk daftar enrollment user
- `GET /api/lesson-progress/` untuk progress lesson

## Fitur Tambahan UAS

| Fitur | Keterangan |
|-------|------------|
| Rating, Review, Wishlist | Menambah interaksi user pada course |
| Search, Filter, Sorting | Mempermudah pencarian dan penelusuran course |
| JWT Refresh Rotation dan Blacklist | Menambah keamanan autentikasi |
| Redis Caching | Mempercepat response endpoint publik course |
| Swagger/OpenAPI | Mempermudah dokumentasi dan presentasi API |

## Cara Authorize Di Swagger

1. Buka `POST /api/token/` di Swagger.
2. Login menggunakan salah satu akun demo.
3. Salin nilai `access` dari response.
4. Klik tombol `Authorize`.
5. Masukkan token dengan format berikut:

```text
Bearer <access_token>
```

## Bukti Pengujian

- Screenshot pengujian akhir disimpan pada folder `images/`.
- Ringkasan bukti dan urutannya dijelaskan pada `FINAL_PROJECT_REPORT.md`.

## File Pendukung

- `FINAL_PROJECT_REPORT.md` berisi ringkasan hasil akhir project dan bukti pengujian
- `LMS_Postman_Collection.json` berisi collection Postman untuk pengujian API
- `cache_report.md` berisi ringkasan implementasi Redis caching
- `query_optimization_demo.py` berisi contoh optimasi query
- `test_cache.py` berisi contoh pengujian cache

## Catatan Penting

- `seed_data` aman dijalankan berulang karena dibuat idempotent.
- Registrasi publik otomatis menghasilkan role `student`.
- Field `instructor` pada pembuatan course diisi otomatis dari `request.user`.
- `PUT` memerlukan seluruh field utama, sedangkan `PATCH` hanya field yang ingin diubah.
- Flower merupakan nilai tambah untuk monitoring task queue dan tidak mengubah endpoint utama API.
