import json
from pathlib import Path

from ai_analyzer import analyze_failure
from log_parser import read_log_file, parse_log_lines
from data_analyzer import (
    create_dataframe,
    analyze_tests,
    associate_errors
)



def generate_report(log_file, output_file):
    """Generate a structured JSON test analysis report."""

    # Read and parse the log file
    lines = read_log_file(log_file)
    parsed_logs = parse_log_lines(lines)

    # Analyze using Pandas
    df = create_dataframe(parsed_logs)
    summary = analyze_tests(df)
    failures = associate_errors(df)

    # Add AI analysis to each failure
    for failure in failures:
        print(f"Analyzing {failure['test_name']} with AI...")

        try:
            failure["ai_analysis"] = analyze_failure(failure)

        except Exception as error:
            print(
                f"AI analysis failed for "
                f"{failure['test_name']}: {error}"
            )
            failure["ai_analysis"] = None


    # Prepare structured report
    report = {
        "source_file": str(log_file),
        "summary": {
            "total_tests": summary["total_tests"],
            "passed": summary["passed"],
            "failed": summary["failed"],
            "pass_rate": summary["pass_rate"]
        },
        "failures": failures
    }

    # Create output directory if needed
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save the report as JSON
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=4) #makes the JSON easier for humans to read

    return report


def main():
    report = generate_report(
        "logs/sample.log",
        "reports/analysis.json"
    )

    print("=== JSON REPORT GENERATED ===")
    print(f"Total Tests: {report['summary']['total_tests']}")
    print(f"Failed Tests: {report['summary']['failed']}")
    print("Report saved to: reports/analysis.json")


if __name__ == "__main__":
    main()
