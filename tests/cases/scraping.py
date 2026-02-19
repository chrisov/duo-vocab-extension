from pathlib import Path
import shutil
from app.server import _handle_save_vocab

def run_case(fixture_path: str) -> None:
    """Run a scraping test using a fixture file.

    fixture_path: path to the JSON fixture, relative to project root.
    The result is written to ``result.json`` in the same directory as the
    fixture file.
    """

    project_root = Path(__file__).resolve().parents[2]
    src = project_root / fixture_path
    if not src.is_file():
        print(f"Fixture not found: {src}")
        return

    ## Write results next to the fixture
    case_dir = src.parent
    result_path = case_dir / "result.json"
    shutil.copy2(src, result_path)

    rel_result = str(result_path.relative_to(project_root))

    language = "pt"
    entry = {
        "timestamp": "2025-01-01T00:00:00Z",
        "vocabulary": ["gato", "cidade"],
    }

    _handle_save_vocab(language, entry, vocab_key=rel_result)



if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python -m tests.cases.scraping tests/vocab/scraping/empty/empty.json")
        raise SystemExit(1)
    run_case(sys.argv[1])