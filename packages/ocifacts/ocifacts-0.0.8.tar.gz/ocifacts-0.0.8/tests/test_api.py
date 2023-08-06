"""Test Ocifacts API"""

from datetime import datetime
import sys

sys.path.append("../")
import ocifacts  # noqa

curr_dt = datetime.now()
timestamp = int(round(curr_dt.timestamp()))

# test file
ocifacts.push(
    f"aunum/mdl-test:file-{timestamp}",
    filepath="./tests/data/test.yaml",
    labels={"this": "that", "jlist": "a list with spaces"},
)
ocifacts.pull(f"aunum/mdl-test:file-{timestamp}", "./tests/out/")
