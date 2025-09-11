# scripts/view_runs.py
from mem import get_all_runs, get_run_details

runs = get_all_runs()
for r in runs:
    print(f"{r[0]}. {r[1]}")

run_id = int(input("View run ID: "))
details = get_run_details(run_id)
print("Query:", details[1])
print("Plan:", details[2])
print("Markdown Output:\n", details[3])
