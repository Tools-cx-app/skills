"""Validate skill packaging and compile/run every complete Rust example."""

from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
NAMES = (
    "rust-ownership", "rust-errors", "rust-collections",
    "rust-cargo", "rust-quality", "rust-docs", "rust-crates-first",
)


def check(name):
    assert name in NAMES, f"unknown skill: {name}"
    path = ROOT / name / "SKILL.md"
    text = path.read_text()
    front = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    assert front, f"{name}: missing frontmatter"
    fields = dict(line.split(": ", 1) for line in front[1].splitlines())
    assert fields["name"] == name
    assert fields["description"].startswith("Use when")
    assert len(fields["description"]) <= 500
    assert len(front[1]) <= 1024
    for section in ("适用", "步骤", "示例", "误区", "来源"):
        assert section in text, f"{name}: missing {section}"
    assert "/home/" not in text, f"{name}: machine-specific path"
    sources = ROOT / name / "references/sources.md"
    assert sources.is_file()
    for document in (path, sources):
        for link in re.findall(r"\]\(([^)]+)\)", document.read_text()):
            if not link.startswith(("https://", "http://", "#")):
                assert (document.parent / link.split("#", 1)[0]).exists(), link
    examples = re.findall(r"^```rust\n(.*?)^```", text, re.M | re.S)
    with tempfile.TemporaryDirectory(prefix="rust-skill-check-") as directory:
        for index, code in enumerate(examples):
            src = Path(directory) / f"example_{index}.rs"
            exe = Path(directory) / f"example_{index}"
            src.write_text(code)
            subprocess.run(
                ["rustc", "--edition=2021", "-Dwarnings", str(src), "-o", str(exe)],
                check=True,
            )
            subprocess.run([str(exe)], check=True, timeout=10)
    print(f"PASS {name}: packaging, links, {len(examples)} Rust examples")


if __name__ == "__main__":
    subprocess.run(["rustc", "--version"], check=True)
    for skill in sys.argv[1:] or NAMES:
        check(skill)
