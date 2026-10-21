"""Build actual ELF objects and compare BSS size against file size.

Run: python3 verify.py
Requires clang and Python 3; no third-party packages.
"""

from pathlib import Path
import struct
import subprocess


ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"
BUILD.mkdir(exist_ok=True)


def read_sections(path):
    """Read section metadata from a little-endian ELF64 object."""
    data = path.read_bytes()
    assert data[:6] == b"\x7fELF\x02\x01", "Expected little-endian ELF64"
    section_offset = struct.unpack_from("<Q", data, 40)[0]
    entry_size, count, names_index = struct.unpack_from("<HHH", data, 58)
    headers = [
        struct.unpack_from("<IIQQQQIIQQ", data, section_offset + i * entry_size)
        for i in range(count)
    ]
    names_header = headers[names_index]
    names = data[names_header[4]:names_header[4] + names_header[5]]
    sections = {}
    for header in headers:
        name = names[header[0]:].split(b"\0", 1)[0].decode()
        sections[name] = {"type": header[1], "size": header[5]}
    return len(data), sections


cases = [
    ("array_small", "array.c", ["-DARRAY_COUNT=10"]),
    ("array_large", "array.c", ["-DARRAY_COUNT=10000"]),
    ("vars_one", "variables.c", []),
    ("vars_many", "variables.c", ["-DMANY_VARIABLES"]),
]

results = {}
lines = ["All sizes in bytes; no debug information.",
         "case          .bss   BSS payload   file   .symtab   .strtab"]

for name, source, defines in cases:
    output = BUILD / (name + ".o")
    subprocess.run(
        ["clang", "--target=x86_64-unknown-linux-gnu",
         "-O0", "-g0", "-fno-common", *defines,
         "-c", source, "-o", str(output)],
        cwd=ROOT,
        check=True,
    )
    file_size, sections = read_sections(output)
    # SHT_NOBITS = 8: its logical size is recorded, but no payload is stored.
    assert sections[".bss"]["type"] == 8
    bss_size = sections[".bss"]["size"]
    results[name] = (file_size, bss_size)
    lines.append(
        f"{name:<12} {bss_size:>6} {0:>13} {file_size:>6}"
        f" {sections['.symtab']['size']:>9} {sections['.strtab']['size']:>9}"
    )

assert results["array_small"][1] == 40
assert results["array_large"][1] == 40000
assert results["array_small"][0] == results["array_large"][0]
assert results["vars_one"][1] == 4
assert results["vars_many"][1] == 40
assert results["vars_many"][0] > results["vars_one"][0]

lines.extend([
    "",
    "PASS: Enlarging the array increased BSS without increasing file size.",
    "PASS: Adding variables increased file size through metadata.",
    "PASS: All four BSS sections are SHT_NOBITS and have no file payload.",
])
report = "\n".join(lines) + "\n"
(BUILD / "results.txt").write_text(report)
print(report, end="")
