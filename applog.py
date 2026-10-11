"""
applog.py — the app's one logger.
================================
Streamlit configures only its own loggers, so a bare logging.getLogger() in app code
drops INFO and prints WARNING+ through the last-resort handler with no timestamp. This
attaches one stderr handler to the "thejudge" logger tree; thejudge.service sends
stderr to the journal, so `journalctl -u thejudge` is the app log.

Usage:  from applog import get_logger;  log = get_logger(__name__)
"""
import logging
import sys

_ROOT = "thejudge"


def get_logger(name: str) -> logging.Logger:
    root = logging.getLogger(_ROOT)
    if not root.handlers:                       # idempotent across Streamlit reruns
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s: %(message)s", "%Y-%m-%d %H:%M:%S"))
        root.addHandler(handler)
        root.setLevel(logging.INFO)
        root.propagate = False                  # don't double-print via Streamlit's root
    # Streamlit runs app.py as __main__; give it a stable name in the log.
    leaf = "app" if name == "__main__" else name
    return logging.getLogger(f"{_ROOT}.{leaf}")
