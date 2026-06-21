#!/usr/bin/env python3
"""
test_app_boot.py — live Streamlit script-run smoke test.
========================================================
Closes the coverage gap that let a real regression ship: the import-based eval
harnesses load `app` as a module named `app`, so a submodule's lazy `import app`
resolves to the already-loaded instance. But `streamlit run app.py` executes the
file as `__main__`; without app.py registering itself in sys.modules under `app`,
that lazy import pulls in a SECOND copy and RE-EXECUTES the UI at module bottom —
crashing with StreamlitDuplicateElementId.

This test runs app.py through streamlit's AppTest (which executes it as the main
script, exactly like `streamlit run`), so the re-execution bug — and any future
one in the live render path — fails here instead of only in the browser.

The clarification query is used deliberately: it exercises the submodule lazy-import
path (build_clarification_queue → chassis_family → unit_armies → indices) and
short-circuits BEFORE the LLM call, so the test is deterministic and offline.

Run:  python tests/verify/test_app_boot.py
"""
import logging
import sys
import warnings
from pathlib import Path

logging.getLogger("streamlit").setLevel(logging.CRITICAL)
warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))


def main() -> int:
    from streamlit.testing.v1 import AppTest
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=240)

    at.run()
    if at.exception:
        print(f"[FAIL] initial app run raised: {at.exception}")
        return 1

    # A chassis query ('Land Raider') → faction clarification. This is the exact path
    # that crashed (indices.unit_army_map's lazy `import app` re-executed the UI).
    at.chat_input[0].set_value(
        "my unit is in a land raider, can they charge after the land raider moves?"
    ).run()
    if at.exception:
        print(f"[FAIL] clarification query raised: {at.exception}")
        return 1

    labels = {b.label for b in at.button}
    # The faction picker must offer the armies that field a Land Raider.
    expected = {"Adeptus Custodes", "Space Marines"}
    if not expected <= labels:
        print(f"[FAIL] expected faction-picker buttons {expected} missing; got {sorted(labels)}")
        return 1

    print(f"[PASS] app boots and the clarification path renders "
          f"({len(labels)} buttons incl. faction picker) with no exception.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
