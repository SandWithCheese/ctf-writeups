# # main/tests/test_reports.py
# from django.test import SimpleTestCase, RequestFactory
# from unittest.mock import patch

# import io
# import stat
# import tarfile
# import zipfile
# import shutil
# from pathlib import Path

# from main.reports import (
#     extract_zip,
#     extract_tar,
#     validate_url,
# )

# TMP_DIR = Path("/tmp")
# REPORTS_DIR = TMP_DIR / "reports"


# def _write_text(path: Path, content: str = "hello\n") -> None:
#     path.parent.mkdir(parents=True, exist_ok=True)
#     path.write_text(content, encoding="utf-8")


# def _zip_with(members: dict[str, bytes], symlink: tuple[str, str] | None = None) -> bytes:
#     bio = io.BytesIO()
#     with zipfile.ZipFile(bio, "w", compression=zipfile.ZIP_DEFLATED) as zf:
#         for name, data in members.items():
#             zf.writestr(name, data)
#         if symlink:
#             link_name, target = symlink
#             info = zipfile.ZipInfo(link_name)
#             info.create_system = 3  # Unix
#             info.external_attr = ((stat.S_IFLNK | 0o777) & 0xFFFF) << 16
#             zf.writestr(info, target)
#     return bio.getvalue()


# def _tar_with(
#     files: dict[str, bytes] | None = None,
#     symlink: tuple[str, str] | None = None,
#     fifo: str | None = None,
#     chardev: tuple[str, int, int] | None = None,
# ) -> bytes:
#     bio = io.BytesIO()
#     with tarfile.open(fileobj=bio, mode="w") as tf:
#         if files:
#             for name, data in files.items():
#                 file_bio = io.BytesIO(data)
#                 ti = tarfile.TarInfo(name=name)
#                 ti.size = len(data)
#                 tf.addfile(ti, fileobj=file_bio)

#         if symlink:
#             link_name, target = symlink
#             ti = tarfile.TarInfo(name=link_name)
#             ti.type = tarfile.SYMTYPE
#             ti.linkname = target
#             tf.addfile(ti)

#         if fifo:
#             ti = tarfile.TarInfo(name=fifo)
#             ti.type = tarfile.FIFOTYPE
#             ti.mode = 0o644
#             tf.addfile(ti)

#         if chardev:
#             name, major, minor = chardev
#             ti = tarfile.TarInfo(name=name)
#             ti.type = tarfile.CHRTYPE
#             ti.devmajor = major
#             ti.devminor = minor
#             ti.mode = 0o644
#             tf.addfile(ti)
#     return bio.getvalue()


# class ReportsTests(SimpleTestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self._temp_dirs: list[Path] = []  # track extraction directories
#         REPORTS_DIR.mkdir(parents=True, exist_ok=True)
#         # Real file for download/validate tests
#         self.sample_path = REPORTS_DIR / "report1.txt"
#         _write_text(self.sample_path, "sample report\n")

#     def _mktempdir(self, name: str) -> Path:
#         """Create and register a temp extraction directory under /tmp."""
#         p = TMP_DIR / name
#         p.mkdir(parents=True, exist_ok=True)
#         self._temp_dirs.append(p)
#         return p

#     def tearDown(self):
#         # Remove only extraction dirs created during tests
#         for d in self._temp_dirs:
#             shutil.rmtree(d, ignore_errors=True)

#         # Keep REPORTS_DIR, but clean any leftover files inside
#         if REPORTS_DIR.exists():
#             for p in REPORTS_DIR.iterdir():
#                 if p.is_file() or p.is_symlink():
#                     p.unlink()

#     # ---------- extract_zip ----------

#     def test_extract_zip_ok(self):
#         data = _zip_with({"a.txt": b"hi", "sub/b.bin": b"\x00\x01"})
#         target_dir = self._mktempdir("extract_zip_ok")

#         with zipfile.ZipFile(io.BytesIO(data), "r") as zf:
#             ok, msg = extract_zip(zf, target_dir)

#         self.assertTrue(ok)
#         self.assertEqual(msg, "OK")
#         self.assertTrue((target_dir / "a.txt").exists())
#         self.assertTrue((target_dir / "sub" / "b.bin").exists())

#     def test_extract_zip_rejects_symlink(self):
#         data = _zip_with({"foo.txt": b"x"}, symlink=("link", "/etc/passwd"))
#         target_dir = self._mktempdir("extract_zip_symlink")

#         with zipfile.ZipFile(io.BytesIO(data), "r") as zf:
#             ok, _ = extract_zip(zf, target_dir)

#         self.assertFalse(ok)

#     def test_extract_zip_requires_txt(self):
#         data = _zip_with({"bin.dat": b"\x00"})
#         target_dir = self._mktempdir("extract_zip_no_txt")

#         with zipfile.ZipFile(io.BytesIO(data), "r") as zf:
#             ok, msg = extract_zip(zf, target_dir)

#         self.assertFalse(ok)
#         self.assertIn(".txt", msg)

#     # ---------- extract_tar ----------

#     def test_extract_tar_ok(self):
#         data = _tar_with(files={"a.txt": b"1", "b.dat": b"2"})
#         target_dir = self._mktempdir("extract_tar_ok")

#         with tarfile.open(fileobj=io.BytesIO(data), mode="r") as tf:
#             ok, msg = extract_tar(tf, target_dir)

#         self.assertTrue(ok)
#         self.assertEqual(msg, "OK")
#         self.assertTrue((target_dir / "a.txt").exists())
#         self.assertTrue((target_dir / "b.dat").exists())

#     def test_extract_tar_rejects_disallowed(self):
#         for suffix, kwargs in [
#             ("symlink", {"files": {"a.txt": b"x"}, "symlink": ("l", "/etc/passwd")}),
#             ("fifo", {"files": {"a.txt": b"x"}, "fifo": "pipefile"}),
#             ("chardev", {"files": {"a.txt": b"x"}, "chardev": ("devchar", 1, 3)}),
#         ]:
#             data = _tar_with(**kwargs)
#             target_dir = self._mktempdir(f"extract_tar_bad_{suffix}")

#             with tarfile.open(fileobj=io.BytesIO(data), mode="r") as tf:
#                 ok, msg = extract_tar(tf, target_dir)

#             self.assertFalse(ok)
#             self.assertIn("disallowed", msg)

#     def test_extract_tar_requires_txt(self):
#         data = _tar_with(files={"bin.dat": b"\x00"})
#         target_dir = self._mktempdir("extract_tar_no_txt")

#         with tarfile.open(fileobj=io.BytesIO(data), mode="r") as tf:
#             ok, msg = extract_tar(tf, target_dir)

#         self.assertFalse(ok)
#         self.assertIn(".txt", msg)

#     # ---------- validate_url ----------

#     def test_validate_url_non_file_scheme(self):
#         resp = validate_url("http://example.com/x")
#         self.assertEqual(resp.status_code, 400)
#         self.assertIn(b"Only file:// URLs are allowed", b"".join(resp))

#     def test_validate_url_outside_base(self):
#         resp = validate_url("file:///etc/shadow")
#         self.assertEqual(resp.status_code, 400)
#         self.assertIn(b"Invalid path", b"".join(resp))

#     def test_validate_url_missing(self):
#         resp = validate_url(f"file://{REPORTS_DIR / 'nope.txt'}")
#         self.assertEqual(resp.status_code, 400)
#         self.assertIn(b"Report not found", b"".join(resp))

#     def test_validate_url_ok(self):
#         resp = validate_url(f"file://{self.sample_path}")
#         self.assertEqual(resp.status_code, 200)
#         body = b"".join(resp.streaming_content)
#         self.assertIn(b"sample report", body)

#!/usr/bin/env python3
import os

file_path = "/upload/reports/test.txt"

# Ensure the parent directory exists
os.makedirs(os.path.dirname(file_path), exist_ok=True)

with open(file_path, "w") as f:
    f.write("this is bad\n")

print(f'Wrote "this is bad" to {file_path}')
