
import subprocess
import sys
from pathlib import Path
from tqdm import tqdm

# Directory containing run_all.py
RENDERER_DIR = Path(__file__).resolve().parent

PROJECT_ROOT = RENDERER_DIR.parents[2]

scripts = [
        "account_renderer.py",
        "calculators_renderer.py",
        "downloads_renderer.py",
        "drug_reference_renderer.py",
        "education_renderer.py",
        "home_renderer.py",
        "learning_renderer.py",
        "saved_renderer.py",
        "search_renderer.py",
        "topic_renderer.py",
]

# Ensure Python can locate the social_media package
env = None
import os
env = os.environ.copy()
existing_pythonpath = env.get("PYTHONPATH", "")
env["PYTHONPATH"] = (
    str(PROJECT_ROOT)
    + (os.pathsep + existing_pythonpath if existing_pythonpath else "")
)

failed = []
successful = 0

print(f"Project root: {PROJECT_ROOT}")
print(f"Renderer directory: {RENDERER_DIR}")

for script in tqdm(scripts, desc="Running renderers", unit="file"):
    script_path = RENDERER_DIR / script

    if not script_path.is_file():
        tqdm.write(f"NOT FOUND: {script_path}")
        failed.append(script)
        continue

    tqdm.write(f"Running: {script}")

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(PROJECT_ROOT),
        env=env,
        check=False,
    )

    if result.returncode == 0:
        successful += 1
        tqdm.write(f"SUCCESS: {script}")
    else:
        failed.append(script)
        tqdm.write(f"FAILED: {script} (exit code {result.returncode})")

print(f"\nCompleted: {successful}/{len(scripts)}")

if failed:
    print("Failed scripts:", ", ".join(failed))
