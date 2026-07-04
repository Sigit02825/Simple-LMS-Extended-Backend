# Final Project Report - Simple LMS

## Identitas

- Nama: Sigit Ilham Pambudi
- NIM: A11.2023.15329
- Kelas: A11.4618
- URL Repository: https://github.com/Sigit02825/Simple-LMS-Extended-Backend.git

## Deskripsi Project

Project ini adalah backend sistem Learning Management System (LMS) sederhana yang dikembangkan menggunakan Django dan Django REST Framework. Project ini mencakup fitur-fitur dasar seperti manajemen pengguna dengan role (admin, instructor, student), manajemen course dan lesson, sistem enrollment, progress tracking, dan beberapa fitur tambahan seperti rating dan wishlist, caching dengan Redis, dan dokumentasi API dengan Swagger.

## Fitur Dasar yang Sudah Berjalan

1. **Autentikasi dan Otorisasi (JWT)
2. **Manajemen Pengguna dengan Role (Admin, Instructor, Student)
3. **Manajemen Course dan Lesson
4. **Sistem Enrollment
5. **Progress Tracking Per Lesson
6. **Dokumentasi API Swagger
7. **Seed Data Demo
8. **Docker Support

## Fitur Tambahan yang Dipilih

| No | Fitur | Kategori | Poin | Status |
|----|-------|----------|------|--------|
| 1 | Rating, Review, dan Wishlist Course | Course & Learning Experience | 12 | Selesai |
| 2 | Search, Filter, dan Sorting Course | Course & Learning Experience |12 | Selesai |
|3| Refresh Token Rotation dan Logout Blacklist | Authentication & Authorization & Security |15| Selesai |
|4| Redis Caching untuk Course | Redis, Caching, dan Performance |12| Selesai |
|5| Swagger/OpenAPI Documentation | API Quality & Developer Experience |10| Selesai |
| Total | | |61| |

## Penjelasan Implementasi Fitur Tambahan

1. **Rating, Review, dan Wishlist Course:
   - Model Rating untuk memberikan rating dan komentar pada course
   - Model Wishlist untuk menyimpan course favorit
   - API endpoint untuk CRUD rating dan wishlist

2. **Search, Filter, dan Sorting Course:
   - Menggunakan Django Filter dan Django REST Framework filters
   - Filter berdasarkan kategori, level, status, dan instructor
   - Search berdasarkan judul dan deskripsi
   - Sorting berdasarkan tanggal dibuat, judul, dan rata-rata rating

3. **Refresh Token Rotation dan Logout Blacklist:
   - Menggunakan Django REST Framework Simple JWT
   - Refresh token diganti setiap penggunaan
   - Logout dengan menambahkan refresh token ke blacklist

4. **Redis Caching:
   - Menggunakan Django Redis sebagai cache backend
   - Konfigurasi di settings.py

5. **Swagger/OpenAPI Documentation:
   - Menggunakan DRF Yasg
   - Dokumentasi API interaktif di /swagger/ dan /redoc/

## Cara Menjalankan Project

### Local Development
```bash
# 1. Buat virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

#3. Jalankan migrations
python manage.py migrate

#4. Seed data
python manage.py seed_data

#5. Jalankan server
python manage.py runserver
```

### Docker Compose
```bash
# Build dan jalankan container
docker-compose up --build
```

## Akun Demo

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin12345 |
| Instructor | instructor | instructor12345 |
| Student 1 | student1 | student12345 |
| Student 2 | student2 | student12345 |

## Endpoint Penting

- Admin Panel: http://localhost:8000/admin/
- API Root: http://localhost:8000/api/
- Swagger Docs: http://localhost:8000/swagger/
- ReDoc Docs: http://localhost:8000/redoc/
- Token: http://localhost:8000/api/token/
- Token Refresh: http://localhost:8000/api/token/refresh/

## Kendala dan Solusi

Tidak ada kendala berarti selama pengembangan.

## Kesimpulan

Project Simple LMS ini berhasil dikembangkan dengan fitur-fitur yang memenuhi persyaratan dan beberapa fitur tambahan. Project ini siap diuji dan dikembangkan lebih lanjut.
