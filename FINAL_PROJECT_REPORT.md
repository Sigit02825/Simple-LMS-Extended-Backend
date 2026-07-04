# Final Project Report - Simple LMS Extended Backend

## Identitas

- Nama: Sigit Ilham Pambudi
- NIM: A11.2023.15329
- Kelas: A11.4618
- Repository: https://github.com/Sigit02825/Simple-LMS-Extended-Backend.git

## Ringkasan Project

Project ini merupakan backend Learning Management System (LMS) berbasis Django dan Django REST Framework. Sistem menyediakan autentikasi JWT, pengelolaan pengguna berbasis role, manajemen course dan lesson, enrollment, progress tracking, serta beberapa fitur tambahan untuk meningkatkan kualitas project UAS seperti rating, wishlist, search/filter/sorting, Redis caching, dan dokumentasi API.

## Stack Teknologi

- Django
- Django REST Framework
- PostgreSQL
- Redis
- Simple JWT
- drf-yasg
- Docker Compose
- Celery, Celery Beat, dan Flower

## Fitur Wajib Yang Berjalan

1. Autentikasi JWT
2. Manajemen pengguna dengan role `admin`, `instructor`, dan `student`
3. Manajemen course dan lesson
4. Enrollment course
5. Progress tracking lesson
6. Dokumentasi API
7. Seed/demo data
8. Docker support

## Fitur Tambahan Yang Dipilih

| No | Fitur | Kategori | Poin | Status |
|----|-------|----------|------|--------|
| 1 | Rating, Review, dan Wishlist Course | Course & Learning Experience | 12 | Selesai |
| 2 | Search, Filter, dan Sorting Course | Course & Learning Experience | 12 | Selesai |
| 3 | Refresh Token Rotation dan Logout Blacklist | Authentication, Authorization, and Security | 15 | Selesai |
| 4 | Redis Caching untuk Course | Redis, Caching, and Performance | 12 | Selesai |
| 5 | Swagger/OpenAPI Documentation | API Quality and Developer Experience | 10 | Selesai |
| Total |  |  | 61 |  |

## Implementasi Fitur Tambahan

### 1. Rating, Review, dan Wishlist

- User dapat memberikan rating dan komentar pada course yang diikuti.
- User dapat menyimpan course ke wishlist.
- Endpoint rating dan wishlist tersedia untuk kebutuhan pengujian API.

### 2. Search, Filter, dan Sorting

- Endpoint `GET /api/courses/` mendukung filter berdasarkan `category`, `level`, `status`, dan `instructor`.
- Search menggunakan parameter `search` pada field `title` dan `description`.
- Sorting didukung melalui parameter `ordering`, misalnya `title` dan `-created_at`.

### 3. JWT Security

- Login menggunakan `POST /api/token/`.
- Refresh token menggunakan `POST /api/token/refresh/`.
- Logout menggunakan blacklist refresh token melalui `POST /api/logout/`.
- Access token digunakan pada Swagger dengan format `Bearer <access_token>`.

### 4. Redis Caching

- Redis digunakan sebagai cache backend.
- Cache diterapkan pada response publik daftar course dan detail course.
- Cache di-invalidasi saat data course atau rating berubah.
- Ringkasan implementasi tersedia pada `cache_report.md`.

### 5. Dokumentasi API

- Dokumentasi interaktif tersedia di Swagger dan ReDoc.
- Swagger dipakai untuk pengujian endpoint secara langsung.
- ReDoc dipakai untuk tampilan dokumentasi yang lebih terstruktur saat presentasi.

### 6. Fondasi Background Task

- Celery worker, Celery Beat, dan Flower disertakan sebagai fondasi tambahan dari tugas sebelumnya.
- Flower digunakan sebagai bukti monitoring task queue.
- Fitur ini bersifat nilai tambah dan tidak mengubah endpoint utama project.

## Akun Demo

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin12345 |
| Instructor | instructor | instructor12345 |
| Student 1 | student1 | student12345 |
| Student 2 | student2 | student12345 |

## Cara Menjalankan Project

### Opsi 1: Docker Compose

```powershell
docker compose --env-file .env.example up -d --build
```

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

## URL Penting

- API Root: `http://localhost:8000/api/`
- Swagger: `http://localhost:8000/swagger/`
- ReDoc: `http://localhost:8000/redoc/`
- Django Admin: `http://localhost:8000/admin/`
- Token JWT: `http://localhost:8000/api/token/`
- Token Refresh: `http://localhost:8000/api/token/refresh/`
- Flower: `http://localhost:5555/`

## Bukti Pengujian Akhir

Screenshot bukti pengujian disimpan pada folder `images/`. Agar ringkas dan relevan untuk penilaian UAS, hanya bukti utama yang dipertahankan.

| No | Bukti | Hasil | File Screenshot |
|----|-------|-------|-----------------|
| 1 | Login JWT `POST /api/token/` | `200 OK` | `images/Login_POST_apitoken.png` |
| 2 | Create Course `POST /courses/` | `201 Created` | `images/Create_Course_POST_courses.png` |
| 3 | List Course `GET /courses/` | `200 OK` | `images/List_Course_GET_courses.png` |
| 4 | Filter Course `GET /courses/?category=Programming` | `200 OK` | `images/FilterGET_coursescategory_Programming.png` |
| 5 | Search Course `GET /courses/?search=python` | `200 OK` | `images/SearchGET_coursessearch_python.png` |
| 6 | Sorting Course `GET /courses/?ordering=title` | `200 OK` | `images/GETcoursesordering=title (1).png` |
| 7 | Update Course `PUT /courses/{id}/` | `200 OK` | `images/Update_Course_PUT_course_{id}.png` |
| 8 | Delete Course `DELETE /courses/{id}/` | `204 No Content` | `images/Delete_Course_DELETE_course_{id}.png` |
| 9 | Swagger | Aktif | `images/Swagger.png` |
| 10 | ReDoc | Aktif | `images/ReDoc.png` |
| 11 | Django Admin | Aktif | `images/admindjango.png` |
| 12 | Flower | Aktif | `images/Flower.png` |

## File Deliverables

- `README.md`
- `FINAL_PROJECT_REPORT.md`
- `.env.example`
- `Dockerfile`
- `docker-compose.yml`
- `LMS_Postman_Collection.json`
- `cache_report.md`
- folder `images/` berisi bukti pengujian

## Kesimpulan

Project Simple LMS Extended Backend telah memenuhi komponen inti backend LMS dan menambahkan beberapa fitur bernilai tambah yang relevan dengan penilaian UAS. Dokumentasi, akun demo, konfigurasi Docker, dan bukti pengujian telah disiapkan agar project mudah dijalankan, diuji, dan dipresentasikan.
