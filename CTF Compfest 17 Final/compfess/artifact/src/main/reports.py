import zipfile
import tarfile
import stat
from pathlib import Path
from urllib.parse import urlparse
from django.http import HttpResponseBadRequest, FileResponse


def _is_symlink_zip(info: zipfile.ZipInfo) -> bool:

    if getattr(info, "create_system", None) == 3:
        mode = (info.external_attr >> 16) & 0xFFFF
        return stat.S_ISLNK(mode)
   
    return False

def extract_zip(zf: zipfile.ZipFile, target_dir: Path) -> tuple[bool, str]:
    members = []
    has_txt = False

    for info in zf.infolist():

        if _is_symlink_zip(info):
            return False, "ZIP cant contain symlink entries"
        
        if info.filename.lower().endswith(".txt"):
            has_txt = True

        members.append(info)

    if not has_txt:
        return False, "Archive must contain at least one .txt file"

    zf.extractall(path=str(target_dir), members=members)
    return True, "OK"

def extract_tar(tf: tarfile.TarFile, target_dir: Path) -> tuple[bool, str]:
    members = []
    has_txt = False

    for member in tf.getmembers():
        if member.ischr() or member.isblk() or member.isfifo() or member.issym() or member.islnk():
            return False, f"TAR contains disallowed entry: {member.name}"
        
        if member.isfile() and member.name.lower().endswith(".txt"):
            has_txt = True

        members.append(member)

    if not has_txt:
        return False, "Archive must contain at least one .txt file"

    tf.extractall(path=str(target_dir), members=members)
    return True, "OK"

def validate_url(raw_url: str):
    parsed = urlparse(raw_url)
    if parsed.scheme != "file":
        return HttpResponseBadRequest("Only file:// URLs are allowed")

    path = (parsed.path or "").replace("..",".")

    if not path.startswith("/upload/reports"):
        return HttpResponseBadRequest("Invalid path")
    
    target = Path(path)  

    if not target.exists():
        return HttpResponseBadRequest("Report not found")

    return FileResponse(
        open(target, "rb"),
        as_attachment=True,
        filename=target.name,
        content_type="text/plain; charset=utf-8",
    )