from pathlib import Path


def read_log_file(file_path):
    """
    Read a log file and return its lines.
    """

    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        lines = file.readlines()

    return lines


if __name__ == "__main__":
    log_lines = read_log_file("logs/sample.log")

    print("=== TEST LOG CONTENT ===")

    for line in log_lines:
        print(line.strip())
