from datetime import datetime

with open("date 1-99.md", "r") as f:
    lines = f.readlines()

base_date = "2025-01-23"

# Convert to desired format
formatted_dates = [f"{base_date} {line.strip()}" for line in lines]  # Format  # Loop

# Print the result
for formatted_date in formatted_dates:
    print(f'"{formatted_date}",')
