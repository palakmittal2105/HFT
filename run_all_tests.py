
import subprocess
import sys


test_files = [
    "test_simulator.py",
    "test_all_schedulers.py",
    "test_market_aware.py",
    "test_dynamic_urgency.py",
    "test_dynamic_selection.py"
]


failed = []

for test_file in test_files:
    print(f"\n{'=' * 55}")
    print(f"Running {test_file}")
    print("=" * 55)

    result = subprocess.run(
        [sys.executable, test_file],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.stderr:
        print(result.stderr)

    if result.returncode == 0:
        print(f"PASS: {test_file}")
    else:
        print(f"FAIL: {test_file}")
        failed.append(test_file)

print("\n" + "=" * 55)

if failed:
    print("Some tests failed:")
    for test_file in failed:
        print("-", test_file)
    sys.exit(1)
else:
    print("ALL TEST FILES PASSED!")
