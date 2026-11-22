#!/usr/bin/env python3
"""Kiểm tra một Knowledge Bundle theo OKF v0.2 (conformance §11) và vài quy ước thêm.

Cách chạy:  python3 -I check_bundle.py [--review-list] <thư-mục-bundle>
  --review-list: chỉ in danh sách concept cần rà lại (không có `verified`, `verified` cũ hơn
  commit cuối của file, hoặc quá `stale_after`). Chỉ báo cáo, luôn thoát mã 0.
Nên cài PyYAML (pip install pyyaml) để parse YAML đầy đủ. Nếu không có, script chạy
ở chế độ dự phòng: chỉ đọc các khóa cấp cao nhất bằng regex, không bắt được lỗi cú pháp YAML.

Lỗi (ERROR) = vi phạm conformance của spec. Cảnh báo (WARN) = quy ước nên theo.
Mã thoát 1 nếu có ERROR.
"""
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

try:
    import yaml
except ImportError:  # chế độ dự phòng
    yaml = None

RESERVED = {"index.md", "log.md"}
FM_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)
LINK_RE = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)\)")
FN_REF_RE = re.compile(r"\[\^([^\]]+)\](?!:)")
FN_DEF_RE = re.compile(r"^\[\^([^\]]+)\]:", re.M)
DATE_H_RE = re.compile(r"^## (\d{4}-\d{2}-\d{2})$", re.M)


def shallow_yaml(raw):
    """Parse tối thiểu khi không có PyYAML: khóa cấp cao nhất + sources[].id/resource."""
    d = {}
    for m in re.finditer(r"^([A-Za-z_][\w-]*):[ \t]*(.*)$", raw, re.M):
        v = m.group(2).strip().strip('"').strip("'")
        d[m.group(1)] = v
    if re.search(r"^generated:.*\bby:", raw, re.M):
        d["generated"] = {"by": "?"}
    srcs = []
    for block in re.split(r"^\s*-\s+(?=id:)", raw.split("\nsources:", 1)[1], flags=re.M)[1:] if "\nsources:" in raw else []:
        i = re.match(r"id:\s*(\S+)", block)
        r = re.search(r"resource:\s*(\S+)", block)
        srcs.append({"id": i.group(1) if i else None, "resource": r.group(1) if r else None})
    if srcs:
        d["sources"] = srcs
    return d


def split(text):
    m = FM_RE.match(text)
    if not m:
        return None, text
    raw = m.group(1)
    data = yaml.safe_load(raw) if yaml else shallow_yaml(raw)
    return data, text[m.end():]


def resolve(bundle, cur, target):
    target = target.split("#")[0]
    if not target or re.match(r"^[a-z]+:", target):
        return True  # URL ngoài hoặc neo trong trang
    base = bundle if target.startswith("/") else cur.parent
    p = (base / target.lstrip("/")).resolve()
    if p.is_dir():
        return (p / "index.md").exists()
    return p.exists()


def to_date(s):
    try:
        return datetime.fromisoformat(str(s).strip().replace("Z", "+00:00")).date()
    except ValueError:
        return None


def review_list(root):
    """Liệt kê concept cần rà lại. So theo NGÀY: commit ghi lại việc xác nhận thường đến sau
    `verified.at` vài giờ, so theo giờ sẽ báo nhầm mọi file."""
    bundle = Path(root).resolve()
    today = date.today()
    groups = {"chưa có `verified`": [], "đã đổi sau lần `verified` cuối": [], "quá `stale_after`": [], "không đọc được ngày commit (chưa commit?)": []}
    for f in sorted(bundle.rglob("*.md")):
        if f.name in RESERVED:
            continue
        rel = f.relative_to(bundle)
        m = FM_RE.match(f.read_text(encoding="utf-8"))
        raw = m.group(1) if m else ""
        vm = re.search(r"^verified:(.*?)(?=^\S|\Z)", raw, re.S | re.M)
        vdates = [d for d in (to_date(x) for x in re.findall(r"\bat:\s*([0-9][^\s,}]*)", vm.group(1))) if d] if vm else []
        sm = re.search(r"^stale_after:\s*\"?([^\s\"]+)", raw, re.M)
        stale = to_date(sm.group(1)) if sm else None
        if stale and stale < today:
            groups["quá `stale_after`"].append(f"{rel} (hạn {stale})")
        if not vdates:
            groups["chưa có `verified`"].append(str(rel))
            continue
        out = subprocess.run(["git", "log", "-1", "--format=%cI", "--", f.name], cwd=f.parent, capture_output=True, text=True)
        c = to_date(out.stdout) if out.returncode == 0 and out.stdout.strip() else None
        if c is None:
            groups["không đọc được ngày commit (chưa commit?)"].append(str(rel))
        elif c > max(vdates):
            groups["đã đổi sau lần `verified` cuối"].append(f"{rel} (verified {max(vdates)}, commit {c})")
    for title, items in groups.items():
        if items:
            print(f"## {title}: {len(items)}")
            for i in items:
                print(f"- {i}")
            print()
    return 0


def main(root):
    bundle = Path(root).resolve()
    errors, warns = [], []
    if yaml is None:
        warns.append("Không có PyYAML: đang chạy chế độ dự phòng, chưa kiểm tra cú pháp YAML đầy đủ")
    concepts = 0
    for f in sorted(bundle.rglob("*.md")):
        rel = f.relative_to(bundle)
        text = f.read_text(encoding="utf-8")
        fm, body = split(text)

        if f.name in RESERVED:
            if f.name == "index.md" and fm and rel.parent != Path("."):
                errors.append(f"{rel}: index.md ngoài thư mục gốc không được có frontmatter")
            if f.name == "log.md":
                if not DATE_H_RE.search(body):
                    warns.append(f"{rel}: log.md không có đề mục ngày ISO 8601")
        else:
            concepts += 1
            if fm is None:
                errors.append(f"{rel}: thiếu frontmatter")
                continue
            if not isinstance(fm, dict) or not str(fm.get("type", "")).strip():
                errors.append(f"{rel}: thiếu trường `type`")
            for k in ("title", "description"):
                if not fm.get(k):
                    warns.append(f"{rel}: nên có `{k}`")
            # sources, footnotes
            ids = {s.get("id") for s in fm.get("sources", []) if isinstance(s, dict) and s.get("id")}
            for s in fm.get("sources", []) or []:
                if not (isinstance(s, dict) and s.get("resource")):
                    errors.append(f"{rel}: một mục `sources` thiếu `resource`")
            refs = set(FN_REF_RE.findall(body))
            defs = set(FN_DEF_RE.findall(body))
            for l in sorted(refs - defs):
                errors.append(f"{rel}: footnote [^{l}] được dùng nhưng chưa định nghĩa")
            for l in sorted(defs - refs):
                warns.append(f"{rel}: footnote [^{l}] định nghĩa nhưng không được dùng")
            for l in sorted(defs):
                if ids and l not in ids:
                    warns.append(f"{rel}: footnote [^{l}] không khớp `sources[].id` nào")
            for k in ("generated",):
                if "generated" in fm and not (isinstance(fm["generated"], dict) and fm["generated"].get("by")):
                    errors.append(f"{rel}: `generated` cần có `by`")
            if fm.get("status") not in (None, "draft", "stable", "deprecated"):
                errors.append(f"{rel}: `status` phải là draft|stable|deprecated")

        for target in LINK_RE.findall(body):
            if not resolve(bundle, f, target):
                warns.append(f"{rel}: link hỏng -> {target}")

    root_idx = bundle / "index.md"
    if root_idx.exists():
        fm, _ = split(root_idx.read_text(encoding="utf-8"))
        if not fm or fm.get("okf_version") != "0.2":
            warns.append("index.md gốc: nên khai báo okf_version: \"0.2\"")

    for e in errors:
        print("ERROR", e)
    for w in warns:
        print("WARN ", w)
    print(f"\n{concepts} concept, {len(errors)} lỗi, {len(warns)} cảnh báo")
    return 1 if errors else 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 2 and args[0] == "--review-list":
        sys.exit(review_list(args[1]))
    if len(args) != 1:
        sys.exit(__doc__)
    sys.exit(main(args[0]))
