# Kualitas dan Pembersihan Data

Sebelum analisis, periksa kualitas data: nilai yang hilang, duplikat, tipe data yang salah, format tanggal yang tidak konsisten, dan outlier. Data cleaning biasanya memakan sebagian besar waktu proyek analisis.

Nilai yang hilang (missing value) dapat dihapus, diisi dengan nilai statistik seperti median, atau dibiarkan jika ketiadaannya bermakna. Pilihan ini harus dicatat karena memengaruhi hasil analisis.

Outlier adalah nilai yang jauh dari pola data lainnya. Salah satu cara mendeteksinya adalah aturan IQR: nilai di bawah Q1 dikurangi 1,5 kali IQR atau di atas Q3 ditambah 1,5 kali IQR dianggap outlier. Outlier tidak selalu salah; periksa dulu apakah ia kesalahan input atau kejadian nyata.

Data leakage terjadi ketika informasi yang tidak tersedia saat prediksi ikut dipakai untuk membangun model, sehingga performa tampak terlalu bagus. Selalu pisahkan data latih dan data uji sebelum melakukan transformasi yang mempelajari statistik dari data.
