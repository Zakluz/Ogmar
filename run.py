import subprocess
import datetime
import os


today = datetime.date.today().isoformat()
output_filename = f"{today}.txt"
branch_name = today

with open(output_filename, "w", encoding="utf-8") as outfile:
    subprocess.run(["python3", "weather.py"], stdout=outfile, stderr=subprocess.STDOUT, text=True)

subprocess.run(["git", "checkout", "-b", branch_name])

subprocess.run(["git", "add", output_filename])

subprocess.run(["git", "commit", "-m", f"Add output for {today}"])

subprocess.run(["git", "push", "--set-upstream", "origin", branch_name])

subprocess.run(["git", "pull"])


