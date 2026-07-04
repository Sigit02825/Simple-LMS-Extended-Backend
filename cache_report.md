# Redis Caching Report

## Skenario

Project menggunakan Redis sebagai cache backend untuk menyimpan response publik daftar course dan detail course.

Endpoint yang dicache:

- `GET /api/courses/`
- `GET /api/courses/{id}/`

## Implementasi

- Cache backend dikonfigurasi pada `config/settings.py`
- Helper cache key dan invalidasi ada pada `courses/services.py`
- Endpoint publik course memakai cache pada `courses/views.py`
- Cache di-invalidasi saat data course atau rating berubah

## Cara Menjalankan Uji Cache

1. Pastikan Redis aktif
2. Jalankan migration dan seed data
3. Jalankan:

```powershell
python test_cache.py
```

## Hasil Yang Diharapkan

- Request pertama lebih lambat karena data diambil dari database
- Request kedua lebih cepat karena response sudah tersedia di cache Redis

## Nilai Tambah

- Mengurangi beban query untuk akses publik course
- Menambah fondasi performa dari tugas sebelumnya
- Bisa ditunjukkan saat presentasi sebagai bukti implementasi Redis caching yang nyata
