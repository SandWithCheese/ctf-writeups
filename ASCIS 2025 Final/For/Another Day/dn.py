import dnfile

pe = dnfile.dnPE("svchost.exe")

if not pe.net or not pe.net.resources:
    print("No .NET resources found")
    raise SystemExit

for i, r in enumerate(pe.net.resources):
    # Convert to python string
    name = str(r.name) if r.name else f"res_{i}"

    data = r.data

    print(f"[+] Resource {i}: {name}, size={len(data)} bytes")

    # Sanitize filename
    safe_name = name.replace("/", "_").replace("\\", "_")

    with open(safe_name, "wb") as f:
        f.write(data)
        print(f"    -> dumped to {safe_name}")
