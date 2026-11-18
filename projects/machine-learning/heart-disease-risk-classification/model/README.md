# Heart Disease Risk Classification

> **Status Proyek:** Tahap 1 - Problem Framing & Business Understanding  
> **Author:** Hafidz Akmal Afrieno (@HafidzAfrieno)  
> **Tanggal:** 2026-11-18

---

## 1. Latar Belakang & Tujuan Bisnis
* **Masalah yang Dihadapi:** Penyakit jantung dan gagal jantung sering kali berkembang tanpa gejala awal yang disadari pasien, sementara pemeriksaan kardiologi lanjutan (seperti ekokardiografi atau kateterisasi) membutuhkan biaya tinggi dan fasilitas khusus. Tanpa alat skrining awal yang cepat, pasien berisiko tinggi sering terlambat mendapatkan penanganan medis.
* **Tujuan Utama:** Membangun sistem klasifikasi risiko penyakit jantung berbasis *Machine Learning* yang terintegrasi ke dalam aplikasi kesehatan untuk melakukan deteksi dini (*early screening*) berdasarkan data klinis dasar pasien.
* **Tindakan / Keputusan (*Actionability*):** 
  * Jika probabilitas risiko tinggi (`risk_score >= threshold`), aplikasi akan menampilkan peringatan dini (*early warning*), memberikan rekomendasi perubahan gaya hidup, serta mengarahkan pengguna/tenaga medis untuk segera menjadwalkan konsultasi dokter spesialis jantung dan pemeriksaan EKG lanjutan.
  * Jika probabilitas risiko rendah, aplikasi memberikan ringkasan pemantauan kesehatan rutin.

---

## 2. Formulasi Masalah Machine Learning
* **Tipe Tugas ML:** `Binary Classification`
* **Definisi Target ($y$):** 
  * **Variabel Target:** `target`
  * **Definisi Eksak:** `1` jika pasien terindikasi memiliki penyakit jantung / risiko tinggi gagal jantung berdasarkan rekam klinis diagnostik, dan `0` jika pasien tidak memiliki indikasi penyakit jantung (normal).
* **Unit Analisis (*Granularity*):** Satu baris data merepresentasikan satu sesi pemeriksaan klinis unik dari seorang pasien yang diidentifikasi oleh `patientid`.

---

## 3. Rencana Data & Kandidat Fitur ($X$)
* **Sumber Data:** Dataset klinis penyakit jantung (*Cardiovascular / Heart Disease Dataset*) dengan 14 atribut terstruktur.
* **Kolom Identifier (Dikecualikan dari Pelatihan Model):**
  * `patientid`: ID unik pasien (hanya digunakan untuk pelacakan baris dan *Group Split* jika terdapat pasien berulang; wajib dibuang sebelum masuk ke model agar tidak terjadi *memorization*).
* **Kandidat Fitur Awal ($X$):**
  * `age`: Usia pasien (tahun).
  * `gender`: Jenis kelamin biologis pasien (`0` = perempuan, `1` = laki-laki).
  * `chestpain`: Tipe nyeri dada yang dialami pasien (`0` = *typical angina*, `1` = *atypical angina*, `2` = *non-anginal pain*, `3` = *asymptomatic*).
  * `restingBP`: Tekanan darah istirahat (*resting blood pressure* dalam mm Hg).
  * `serumcholestrol`: Kadar kolesterol serum (*serum cholesterol* dalam mg/dl).
  * `fastingbloodsugar`: Indikator gula darah puasa > 120 mg/dl (`1` = ya, `0` = tidak).
  * `restingrelectro`: Hasil elektrokardiografi saat istirahat (*resting ECG*: normal, kelainan gelombang ST-T, atau hipertrofi ventrikel kiri).
  * `maxheartrate`: Detak jantung maksimum yang dicapai pasien (*maximum heart rate achieved*).
  * `exerciseangia`: Indikator angina yang dipicu oleh aktivitas fisik/olahraga (`1` = ya, `0` = tidak).
  * `oldpeak`: Nilai depresi segmen ST yang dipicu oleh olahraga relatif terhadap kondisi istirahat.
  * `slope`: Kemiringan (*slope*) segmen ST pada puncak latihan fisik (*upsloping*, *flat*, *downsloping*).
  * `noofmajorvessels`: Jumlah pembuluh darah utama (0–3) yang terdeteksi melalui pewarnaan fluoroskopi.
* **Audit Anti-Leakage:** Seluruh fitur input di atas digunakan untuk memprediksi `target` pada waktu evaluasi klinis ($t_0$). Pada tahap *preprocessing* dan *deployment* aplikasi, perlu diperhatikan bahwa `noofmajorvessels` merupakan hasil pemeriksaan fluoroskopi lanjutan—jika aplikasi ditujukan untuk skrining mandiri pengguna awam di rumah (tanpa akses hasil fluoroskopi), fitur ini harus dievaluasi ulang ketersediaannya atau ditangani sebagai fitur opsional.

---

## 4. Metrik Evaluasi & Kriteria Sukses

| Kategori | Metrik | Target Minimal (*Success Criteria*) | Alasan Pemilihan |
| :--- | :--- | :--- | :--- |
| **Metrik Bisnis (KPI)** | Tingkat Deteksi Dini Pasien Berisiko (*Screening Capture Rate*) | Menjaring minimal 85% pasien berisiko tinggi sebelum terjadi komplikasi akut | Memastikan sistem aplikasi benar-benar membantu triase dan pencegahan keterlambatan medis. |
| **Metrik Teknis Utama** | **Recall (Sensitivity)** & **F2-Score** | `Recall >= 0.85` dan `F2-Score >= 0.80` | Dalam domain medis, melewatkan pasien yang sebenarnya sakit (*False Negative*) jauh lebih berbahaya daripada peringatan berlebih. |
| **Metrik Teknis Sekunder** | **PR-AUC** & **Precision** | `PR-AUC >= 0.82` dan `Precision >= 0.70` | Menjaga keseimbangan agar aplikasi tidak terlalu sering memberikan alarm palsu (*false alarm*) yang memicu kepanikan pengguna. |

* **Analisis Biaya Kesalahan (*Error Trade-off*):**
  * **False Positive (FP):** Pasien yang sebenarnya sehat diprediksi berisiko tinggi (`target = 1`). Dampaknya adalah kecemasan sementara pada pengguna dan biaya pemeriksaan skrining lanjutan (EKG/konsultasi dokter).
  * **False Negative (FN):** Pasien yang sebenarnya memiliki risiko penyakit jantung diprediksi sehat/aman (`target = 0`). Dampaknya sangat fatal karena pasien menunda pengobatan dan berisiko mengalami serangan atau gagal jantung mendadak.
  * **Prioritas:** Meminimalkan **False Negative (FN)** dengan mengoptimalkan *Recall* sambil menjaga *Precision* pada batas yang dapat diterima secara klinis.

---

## 5. Baseline Non-ML & Pembanding Awal
* **Solusi Saat Ini / Heuristik Sederhana:** Aturan skrining klinis statis berbasis ambang batas faktor risiko tunggal (misalnya: `IF age > 50 AND (restingBP > 140 OR serumcholestrol > 240) THEN berisiko_tinggi`).
* **Skor Baseline:** *To Be Measured* di Tahap 9 (seluruh model ML wajib mengalahkan skor *Recall* dan *F2-Score* dari aturan heuristik ini).

---

## 6. Batasan Teknis & Kebutuhan Deployment (*Constraints*)
* **Mode Inferensi:** `Real-time REST API` (menggunakan FastAPI agar dapat dikonsumsi langsung oleh aplikasi mobile/web kesehatan saat pengguna memasukkan data pemeriksaan).
* **Target Latensi:** `< 200 ms` per permintaan prediksi agar pengalaman pengguna di dalam aplikasi tetap responsif.
* **Kebutuhan Interpretabilitas (*Explainability*):** **Wajib.** Aplikasi harus menampilkan faktor utama yang memengaruhi skor risiko pasien (menggunakan *SHAP values* atau *Feature Contribution*, misalnya: *"Risiko meningkat terutama karena nilai `restingBP` tinggi dan tipe `chestpain`"*), sehingga dokter dan pengguna tidak menerima prediksi *black-box* begitu saja.
* **Frekuensi Retraining:** Setiap 6 bulan sekali menggunakan data klinis baru yang telah tervalidasi dokter, atau lebih cepat jika terdeteksi *Data Drift* pada distribusi usia dan profil kesehatan pengguna aplikasi.

---