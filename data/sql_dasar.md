# SQL Dasar untuk Analisis Data

SELECT dipakai untuk memilih kolom dari tabel, dan WHERE untuk menyaring baris sebelum pengelompokan. GROUP BY mengelompokkan baris berdasarkan satu atau beberapa kolom sehingga fungsi agregat seperti COUNT, SUM, dan AVG dapat dihitung per kelompok. HAVING menyaring hasil setelah pengelompokan, sedangkan WHERE menyaring sebelum pengelompokan.

JOIN menggabungkan baris dari dua tabel berdasarkan kolom yang berelasi. INNER JOIN hanya mengembalikan baris yang cocok di kedua tabel. LEFT JOIN mengembalikan semua baris dari tabel kiri beserta pasangan dari tabel kanan jika ada; jika tidak ada, kolom tabel kanan bernilai NULL.

Window function menghitung nilai di atas sekumpulan baris terkait tanpa menggabungkan baris menjadi satu. Contohnya ROW_NUMBER, RANK, dan SUM dengan klausa OVER (PARTITION BY ... ORDER BY ...). Fungsi ini berguna untuk running total, peringkat per kelompok, dan perbandingan dengan baris sebelumnya memakai LAG.

CTE (Common Table Expression) ditulis dengan kata kunci WITH dan membuat query kompleks lebih mudah dibaca karena dipecah menjadi langkah-langkah bernama.
