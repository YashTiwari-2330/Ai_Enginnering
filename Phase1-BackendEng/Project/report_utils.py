import os
import json
import csv
from datetime import datetime
from typing import Dict, Any, Tuple


def _age_bucket(age: int) -> str:
    if age is None:
        return "unknown"
    if age <= 10:
        return "0-10"
    if age <= 20:
        return "11-20"
    if age <= 30:
        return "21-30"
    if age <= 40:
        return "31-40"
    if age <= 50:
        return "41-50"
    if age <= 60:
        return "51-60"
    return ">60"


def generate_report(data: Dict[str, Any], out_dir: str = "reports") -> Tuple[str, str]:
    """Generate a report from the students data and write JSON and CSV files.

    Returns (json_path, csv_path).
    """
    os.makedirs(out_dir, exist_ok=True)

    students = data.get("students", []) if isinstance(data, dict) else []

    total_students = len(students)
    ages = [s.get("age") for s in students if isinstance(s.get("age"), (int, float))]
    avg_age = round(sum(ages) / len(ages), 2) if ages else None

    # Age distribution
    age_distribution = {}
    for s in students:
        bucket = _age_bucket(s.get("age"))
        age_distribution[bucket] = age_distribution.get(bucket, 0) + 1

    # Email domains
    domains = {}
    for s in students:
        email = s.get("email") or ""
        parts = email.split("@")
        domain = parts[1].lower() if len(parts) == 2 else "unknown"
        domains[domain] = domains.get(domain, 0) + 1

    # Build report
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    json_filename = f"report_{timestamp}.json"
    csv_filename = f"report_{timestamp}.csv"

    json_path = os.path.join(out_dir, json_filename)
    csv_path = os.path.join(out_dir, csv_filename)

    report = {
        "generated_at_utc": timestamp,
        "total_students": total_students,
        "average_age": avg_age,
        "age_distribution": age_distribution,
        "email_domains": domains,
        "students_sample_count": min(20, total_students)
    }

    # Save JSON report
    with open(json_path, "w") as jf:
        json.dump(report, jf, indent=4)

    # Save CSV with full student rows (id, name, age, email)
    with open(csv_path, "w", newline="") as cf:
        writer = csv.writer(cf)
        writer.writerow(["id", "name", "age", "email"])
        for s in students:
            writer.writerow([
                s.get("id"),
                s.get("name"),
                s.get("age"),
                s.get("email")
            ])

    return json_path, csv_path
