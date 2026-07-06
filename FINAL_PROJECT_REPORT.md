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

## Dokumentasi API dan Cara Membacanya

Project menyediakan dokumentasi API dalam dua tampilan:

1. **Swagger (`/swagger/`)**
   - Tujuan: dokumentasi interaktif untuk mencoba endpoint dengan tombol **Try it out**.
   - Cocok untuk pengujian langsung saat presentasi karena bisa mengirim request dan melihat response.
   - Pada bagian bawah halaman, Swagger juga menampilkan **Models** (schema) yang menjelaskan struktur data.

2. **ReDoc (`/redoc/`)**
   - Tujuan: dokumentasi yang lebih nyaman dibaca untuk melihat deskripsi endpoint, request body, dan response.
   - Cocok untuk menjelaskan struktur API secara keseluruhan kepada dosen/penguji.

### Cara Authorize di Swagger (JWT)

1. Buka `POST /api/token/` di Swagger.
2. Klik **Try it out**, isi akun demo, lalu **Execute**.
3. Salin nilai `access` dari response.
4. Klik tombol **Authorize** di bagian atas Swagger.
5. Masukkan:

```text
Bearer <access_token>
```

Setelah berhasil authorize, endpoint yang butuh login (misalnya create/update/delete course) dapat diakses.

## Panduan Pengujian Singkat (Urutan Presentasi)

Urutan ini sesuai bukti screenshot pada folder `images/` dan mudah diikuti saat demo:

1. **Login JWT**
   - Endpoint: `POST /api/token/`
   - Target: mendapat `access` dan `refresh`.
2. **Create Course**
   - Endpoint: `POST /courses/`
   - Target: `201 Created` dan course baru terbentuk.
3. **List Course**
   - Endpoint: `GET /courses/`
   - Target: `200 OK`, response berisi pagination `count`, `next`, `previous`, `results`.
4. **Filter**
   - Endpoint: `GET /courses/?category=Programming`
   - Target: `200 OK`, hasil hanya course dengan kategori terkait.
5. **Search**
   - Endpoint: `GET /courses/?search=python`
   - Target: `200 OK`, hasil mengandung kata `python` pada `title/description`.
6. **Sorting**
   - Endpoint: `GET /courses/?ordering=title`
   - Target: `200 OK`, data terurut berdasarkan judul.
7. **Update Course**
   - Endpoint: `PUT /courses/{id}/`
   - Target: `200 OK`, data course berubah sesuai payload.
8. **Delete Course**
   - Endpoint: `DELETE /courses/{id}/`
   - Target: `204 No Content`, course terhapus.
9. **Validasi UI Pendukung**
   - Swagger aktif: `/swagger/`
   - ReDoc aktif: `/redoc/`
   - Admin aktif: `/admin/`
   - Flower aktif: `/` pada port `5555`

## Bukti Pengujian Akhir

Screenshot bukti pengujian disimpan pada folder `images/`. Folder ini memuat bukti utama dan bukti tambahan agar proses pengujian UAS dapat dilihat lebih lengkap.

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

## Lampiran Screenshot Tambahan

Selain bukti utama, tersedia juga screenshot tambahan yang memperlihatkan detail hasil pengujian dan tampilan dokumentasi.

| File Screenshot | Kategori | Penjelasan Singkat |
|---|---|---|
| `images/Login_POST_apitoken_detail.png` | JWT | Detail response `POST /api/token/` berisi token `access` dan `refresh`. |
| `images/Create_Course_POST_courses_detail.png` | Course | Detail response `POST /courses/` (contoh hasil `201 Created`). |
| `images/List_Course_GET_courses_detail.png` | Course | Detail response `GET /courses/` (contoh hasil `200 OK` dengan pagination). |
| `images/Update_Course_PUT_course_{id}_detail.png` | Course | Detail response update `PUT /courses/{id}/` (contoh hasil `200 OK`). |
| `images/Update_Course_PUT_course_{id}_detail_2.png` | Course | Detail lanjutan update `PUT /courses/{id}/` (bagian response yang menampilkan field lengkap). |
| `images/Swagger_Enrollments_LessonProgress_Lessons.png` | Swagger | Tampilan daftar endpoint pada Swagger untuk `enrollments`, `lesson-progress`, dan `lessons`. |
| `images/Swagger_Token_Users_Wishlist.png` | Swagger | Tampilan daftar endpoint pada Swagger untuk `token`, `users`, dan `wishlist`. |
| `images/Swagger_Models.png` | Swagger | Tampilan bagian `Models` pada Swagger (schema model seperti User, Course, Enrollment, LessonProgress, Lesson, Rating, Wishlist). |
| `images/Swagger_Additional_Section.png` | Swagger | Tampilan tambahan Swagger untuk memperlihatkan bagian endpoint lain/scroll lanjutan. |
| `images/ReDoc_Courses_Schema.png` | ReDoc | Contoh tampilan schema dan request/response pada ReDoc untuk endpoint course. |
| `images/Flower_Tasks_Dashboard.png` | Flower | Halaman monitoring task (contoh task `warm_public_course_cache` dan `generate_course_report_snapshot`). |
| `images/Admin_Dashboard.png` | Admin | Tampilan dashboard Django Admin setelah login (daftar model yang terdaftar). |
| `images/Admin_Users_List.png` | Admin | Tampilan daftar user di Django Admin (membuktikan akun demo dan role). |

## Referensi Folder Images

Seluruh file bukti pengujian dan dokumentasi disimpan pada folder `images/` di root repository. Folder ini berisi bukti utama dan detail tambahan sesuai urutan pengujian UAS.

## Catatan Penting Saat Demo

- Token `access` memiliki masa berlaku. Jika muncul `401 Unauthorized` dengan pesan token expired, lakukan login ulang di `POST /api/token/` dan authorize ulang.
- `POST /courses/` tidak membutuhkan field `instructor` pada input karena diisi otomatis dari user login.
- `PUT` memerlukan seluruh field utama, sedangkan `PATCH` hanya field yang ingin diubah.

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
