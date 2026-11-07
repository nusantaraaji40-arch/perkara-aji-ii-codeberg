# Contoh Konektor Codeberg — PERKARA AJI II

Contoh pemakaian konektor Codeberg (custom.codeberg) dari workspace Muse, khusus operasi **read-only** yang aman. Repo ini bagian dari proyek PERKARA AJI II — agen AI yang membuat video YouTube 8 menit dari foto presenter.

Codeberg adalah hosting git gratis (Forgejo, non-profit Jerman, hanya untuk proyek FOSS). Repo `perkara-aji-ii-agent` bisa di-mirror ke sini sebagai cadangan GitHub, dan API-nya (kompatibel Gitea) bisa dipakai agen untuk membaca/membuat issue, release, dan mengelola repo dari VPS.

## Isi repo

| File | Konektor | Perintah |
|---|---|---|
| `codeberg_example.py` | custom.codeberg | `whoami`, `repos`, `repo`, `search` |

## Cara pakai

```bash
python3 codeberg_example.py whoami
python3 codeberg_example.py repos
python3 codeberg_example.py repo forgejo-contrib forgejo-cli
python3 codeberg_example.py search forgejo-sdk
```

Syarat: helper konektor harus ada di mesinmu, yaitu `~/workspace/custom-connectors/custom.codeberg/bin/codeberg.py`. Kalau helper-mu ada di tempat lain, atur lewat environment variable:

```bash
CODEBERG_HELPER=/path/ke/codeberg.py python3 codeberg_example.py
```

## Tanpa secret

File-file di repo ini **tidak berisi API key, token, atau rahasia apa pun**. Semua otentikasi dilakukan helper konektor, yang memakai surrogate dari secure storage Muse. Jangan pernah menaruh token di file, di `.env`, atau di commit.

## Status verifikasi — jujur (2026-11-07)

Konektor Codeberg **belum terbukti bekerja** pada 2026-11-07: `whoami` (GET /api/v1/user) dijawab HTTP 401 Unauthorized. Penyebab yang sudah terbukti: helper mengirim `Authorization: token hsurr:...` sehingga pertukaran surrogate tidak terjadi — token asli tidak pernah sampai ke server (Forgejo: "access token does not exist [sha: hsurr:...]"). Jadi tokennya sendiri belum teruji sama sekali.

Perbaikan: konektor di-re-register dengan penempatan `query_param:access_token` dan helper diubah ke `url_with_surrogate_query_param`; link reconnect sudah dikirim ~03:01 2026-11-07. Periksa ulang file contoh ini setelah reconnect masuk. Jangan klaim konektor ini bekerja sebelum `whoami` berhasil mengembalikan login Codeberg yang benar.

## Repo terkait (hasil screening)

Repo open source terbaik untuk memakai Codeberg/Forgejo API dari code sendiri (bukan bagian repo ini, lisensinya masing-masing):

- **pyforgejo** — https://codeberg.org/harabat/pyforgejo — client library Python untuk Forgejo API (generated dari OpenAPI spec, `pip install pyforgejo`), lisensi MIT. Paling cocok: agen ini berbahasa Python.
- **forgejo-cli** — https://codeberg.org/forgejo-contrib/forgejo-cli — CLI resmi komunitas Forgejo (repo, PR, issue, release, wiki, actions), lisensi Apache-2.0 + MIT (dual). Otomasi VPS tanpa tulis kode API.
- **forgejo-sdk** — https://codeberg.org/mvdkleijn/forgejo-sdk — SDK Go pembungkus Forgejo API, lisensi MIT. Kurang cocok langsung (agen Python, bukan Go); berguna sebagai referensi pola pemakaian API.

## Lisensi

Code contoh di repo ini berlisensi **MIT** (lihat `LICENSE`). Dependensi/repo terkait di atas punya lisensinya sendiri-sendiri — periksa sebelum memakai.
