#!/usr/bin/env python3
"""Contoh pemakaian konektor Codeberg (custom.codeberg) untuk PERKARA AJI II.

STATUS VERIFIKASI — JUJUR, per 2026-11-07 (dicek ulang hari ini):
  GAGAL / BELUM TERBUKTI. `whoami` (GET /api/v1/user) masih mengembalikan
  HTTP 401 Unauthorized. Penyebab yang sudah terbukti: helper
  `bin/codeberg.py` mengirim `Authorization: token hsurr:...` sehingga
  pertukaran surrogate tidak terjadi — token asli TIDAK PERNAH sampai ke
  server Codeberg (Forgejo menjawab "access token does not exist [sha:
  hsurr:...]"). Jadi tokennya sendiri belum teruji sama sekali.
  Perbaikan yang sudah diminta: konektor di-re-register dengan placement
  `query_param:access_token` + helper diubah ke
  `url_with_surrogate_query_param`, dan link reconnect sudah dikirim ke
  Mas Aji sekitar 2026-11-07 03:01. JANGAN klaim konektor ini bekerja
  sebelum `whoami` berhasil mengembalikan login Codeberg yang benar.

File ini TIDAK berisi API key/token/rahasia apa pun. Semua panggilan
dilewatkan ke helper resmi `bin/codeberg.py` yang memakai surrogate
dari secure storage. Hanya operasi READ-ONLY yang aman (whoami, repos,
repo, search_repos). Jangan ubah helper/CONNECTOR.md/connector.yaml.

Cara pakai:
    python3 examples/konektor/codeberg_example.py whoami
    python3 examples/konektor/codeberg_example.py repos
    python3 examples/konektor/codeberg_example.py repo forgejo-contrib forgejo-cli
    python3 examples/konektor/codeberg_example.py search forgejo-sdk

Kenapa Codeberg relevan untuk PERKARA AJI II:
  Codeberg adalah hosting git gratis (Forgejo, non-profit Jerman, hanya
  untuk proyek FOSS). Repo perkara-aji-ii-agent bisa di-mirror ke sini
  sebagai cadangan GitHub, dan API-nya (kompatibel Gitea) bisa dipakai
  agen untuk membaca/membuat issue, release, dan mengelola repo dari VPS.
  Client Python yang direkomendasikan: harabat/pyforgejo (MIT) — sudah
  di-clone ke data/konektor-repo-screening/codeberg/pyforgejo.
"""
import json
import subprocess
import sys

import os

HELPER = os.environ.get("CODEBERG_HELPER", "/home/hatch/workspace/custom-connectors/custom.codeberg/bin/codeberg.py")


def run(*args):
    """Panggil helper resmi; kembalikan dict hasil atau None bila gagal."""
    proc = subprocess.run(
        [sys.executable, HELPER, *args],
        capture_output=True, text=True, timeout=60,
    )
    if proc.returncode != 0:
        print(f"[codeberg] helper gagal (exit {proc.returncode}):", file=sys.stderr)
        print((proc.stderr or proc.stdout).strip()[-500:], file=sys.stderr)
        print("[codeberg] Ingat: verifikasi konektor ini masih GAGAL (401). "
              "Periksa status reconnect sebelum mengandalkan hasil ini.",
              file=sys.stderr)
        return None
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        print("[codeberg] output helper bukan JSON:", proc.stdout[:300], file=sys.stderr)
        return None


def main(argv):
    cmd = argv[1] if len(argv) > 1 else "whoami"
    if cmd == "whoami":
        data = run("whoami")
        if data:
            print("login:", data.get("login"), "| id:", data.get("id"),
                  "| nama:", data.get("full_name"))
    elif cmd == "repos":
        data = run("repos")
        if isinstance(data, list):
            for r in data[:20]:
                print(r.get("full_name"), "| private:", r.get("private"),
                      "| updated:", r.get("updated_at"))
    elif cmd == "repo":
        owner, repo = argv[2], argv[3]
        data = run("repo", owner, repo)
        if data:
            print(data.get("full_name"), "| branch:", data.get("default_branch"),
                  "| private:", data.get("private"))
    elif cmd == "search":
        data = run("search_repos", argv[2])
        if data and isinstance(data.get("data"), list):
            for r in data["data"][:20]:
                print(r.get("full_name"), "| private:", r.get("private"))
    else:
        print("perintah: whoami | repos | repo <owner> <repo> | search <kata>",
              file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
