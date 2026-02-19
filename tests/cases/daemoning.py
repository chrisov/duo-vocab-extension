from pathlib import Path
import shutil
import json

from daemon.JSONVocab import JSONVocab
from daemon.main import _process_model_response
from daemon.model import response_example


def run_case(fixture_path: str) -> None:
    """Run a daemon vocab test using a fixture file.

    fixture_path: path to the JSON fixture, relative to the project root.
    The result is written to ``result.json`` in the same directory as the
    fixture file.
    """

    project_root = Path(__file__).resolve().parents[2]
    src = project_root / fixture_path
    if not src.is_file():
        print(f"Fixture not found: {src}")
        return

    # Write results next to the fixture
    case_dir = src.parent
    result_path = case_dir / "result.json"
    shutil.copy2(src, result_path)

    # Use a path relative to the project root so that JSONVocab/load_data_from_json
    # resolve it correctly without needing an entry in paths.json
    rel_result = str(result_path.relative_to(project_root))

    # Load the vocab JSON and process it with the static example model response
    obj = JSONVocab(rel_result, "pt")

    try:
        response = json.loads(response_example)
    except json.JSONDecodeError:
        print("response_example is not valid JSON, skipping...")
        return

    new_staged = response.get("staged", {})
    _process_model_response(obj, new_staged)
    obj.write_data_to_json()



if __name__ == "__main__":
	import sys
	if len(sys.argv) != 2:
		print("Usage: python -m tests.cases.daemoning tests/vocab/daemon/empty/empty.json")
		raise SystemExit(1)
	run_case(sys.argv[1])
