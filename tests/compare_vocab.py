import json
import sys
from pathlib import Path


def _load_json(path: str) -> dict:
    file = Path(path)
    with file.open(encoding="utf-8") as f:
        return json.load(f)


def compare_pt_section(expected_path: str, result_path: str) -> int:
    """Deep-compare the 'pt' section of two vocab JSON files.

    Template for the 'pt' structure:
      'pt': {
        'scraped': {'timestamp': str, 'vocabulary': []},
        'staged':  {'timestamp': str, 'approved': [{}], 'disapproved': []}
      }

    - Compares timestamps as plain strings.
    - Compares scraped.vocabulary as sets (order-insensitive) and reports
      missing/extra words.
    - Compares staged.disapproved as sets (order-insensitive).
    - Compares staged.approved entry-by-entry, keyed by 'Word'.

        Returns an integer status code only, with no output:

            - 0 => sections are equal
            - 1 => sections differ in any way
    """

    expected = _load_json(expected_path)
    result = _load_json(result_path)

    issues: list[str] = []

    exp_pt = expected.get("pt")
    res_pt = result.get("pt")

    if exp_pt is None and res_pt is None:
        return 0
    if exp_pt is None or res_pt is None:
        # One file has 'pt', the other does not
        return 1

    # --- scraped ---
    exp_scraped = exp_pt.get("scraped", {})
    res_scraped = res_pt.get("scraped", {})

    if exp_scraped.get("timestamp") != res_scraped.get("timestamp"):
        issues.append("scraped.timestamp differs")

    exp_vocab = exp_scraped.get("vocabulary", [])
    res_vocab = res_scraped.get("vocabulary", [])

    missing_vocab = sorted(set(exp_vocab) - set(res_vocab))
    extra_vocab = sorted(set(res_vocab) - set(exp_vocab))
    if missing_vocab or extra_vocab:
        issues.append("scraped.vocabulary differs")

    # --- staged ---
    exp_staged = exp_pt.get("staged", {})
    res_staged = res_pt.get("staged", {})

    if exp_staged.get("timestamp") != res_staged.get("timestamp"):
        issues.append("staged.timestamp differs")

    # disapproved: compare as sets
    exp_dis = exp_staged.get("disapproved", [])
    res_dis = res_staged.get("disapproved", [])
    missing_dis = sorted(set(exp_dis) - set(res_dis))
    extra_dis = sorted(set(res_dis) - set(exp_dis))
    if missing_dis or extra_dis:
        issues.append("staged.disapproved differs")

    # approved: compare entry-by-entry, keyed by 'Word'
    exp_approved_list = exp_staged.get("approved", []) or []
    res_approved_list = res_staged.get("approved", []) or []

    def index_approved(entries: list[dict]) -> dict[str, dict]:
        mapping: dict[str, dict] = {}
        for entry in entries:
            key = entry.get("Word")
            if key is None:
                # Fallback: use the whole dict as a key string
                key = json.dumps(entry, sort_keys=True)
            mapping[key] = entry
        return mapping

    exp_approved = index_approved(exp_approved_list)
    res_approved = index_approved(res_approved_list)

    exp_words = set(exp_approved.keys())
    res_words = set(res_approved.keys())

    missing_words = sorted(exp_words - res_words)
    extra_words = sorted(res_words - exp_words)
    if missing_words or extra_words:
        issues.append("staged.approved entries differ (missing/extra words)")

    common_words = sorted(exp_words & res_words)
    for word in common_words:
        if exp_approved[word] != res_approved[word]:
            issues.append("staged.approved entry differs")

    return 0 if not issues else 1


if __name__ == "__main__":
    if len(sys.argv) != 3:
        # Incorrect usage: signal error via exit code only
        raise SystemExit(2)

    _, expected_path, result_path = sys.argv
    raise SystemExit(compare_pt_section(expected_path, result_path))
