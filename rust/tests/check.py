"""Validate Book-centered Rust skill packages and compile complete examples."""

from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
NAMES = (
    "rust-foundations", "rust-ownership", "rust-types", "rust-errors",
    "rust-collections", "rust-projects", "rust-testing",
    "rust-concurrency", "rust-async", "rust-unsafe",
    "rust-quality", "rust-docs",
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
            if "#[test]" in code:
                subprocess.run(
                    ["rustc", "--edition=2021", "-Dwarnings", "--test",
                     str(src), "-o", str(exe)], check=True,
                )
                subprocess.run([str(exe)], check=True, timeout=10)
    print(f"PASS {name}: packaging, links, {len(examples)} Rust examples")


if __name__ == "__main__":
    actual = {p.name for p in ROOT.glob("rust-*") if (p / "SKILL.md").is_file()}
    assert actual == set(NAMES), f"skill directories differ: {actual ^ set(NAMES)}"
    for document in (ROOT / "README.md", ROOT / "skill-loading.md"):
        text = document.read_text()
        assert all(name in text for name in NAMES), f"{document.name}: missing skill"
        for link in re.findall(r"\]\(([^)]+)\)", text):
            if not link.startswith(("https://", "http://", "#")):
                assert (document.parent / link.split("#", 1)[0]).exists(), link
    subprocess.run(["rustc", "--version"], check=True)
    for skill in sys.argv[1:] or NAMES:
        check(skill)
