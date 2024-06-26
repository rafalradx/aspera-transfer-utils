import re
import argparse


def parse_log(file):
    transfer_start_pattern = re.compile(
        r'LOG FASP Transfer Start uuid=(?P<uuid>[a-f0-9-]+) op=send status=(?P<status>\w+) file="(?P<file>[^"]+)" size=(?P<size>\d+) start_byte=\d+ rate=(?P<rate>[\d.]+)(?P<unit>Kbps|Mbps) loss=[\d.]+ rexreqs=\d+ overhead=\d+'
    )
    transfer_stop_pattern = re.compile(
        r'LOG FASP Transfer Stop uuid=(?P<uuid>[a-f0-9-]+) op=send status=(?P<status>\w+) file="(?P<file>[^"]+)" size=(?P<size>\d+) start_byte=\d+ rate=(?P<rate>[\d.]+)(?P<unit>Kbps|Mbps) elapsed=(?P<elapsed>[\d.]+)s loss=[\d.]+ rexreqs=\d+ overhead=\d+'
    )

    transfer_events = []
    transfer_stats = {"total_files": 0, "started": 0, "success": 0, "total_time": 0.0}

    for line in file:

        if line.startswith("LOG Add sender src :"):
            transfer_stats["total_files"] += 1

        start_match = transfer_start_pattern.match(line)
        stop_match = transfer_stop_pattern.match(line)

        if start_match:
            transfer_events.append(
                {
                    "event": "start",
                    "status": start_match.group("status"),
                    "file": start_match.group("file"),
                    "size": int(start_match.group("size")),
                    "rate": float(start_match.group("rate")),
                }
            )
            transfer_stats["started"] += 1

        if stop_match:
            transfer_events.append(
                {
                    "event": "stop",
                    "status": stop_match.group("status"),
                    "file": stop_match.group("file"),
                    "size": int(stop_match.group("size")),
                    "rate": float(stop_match.group("rate")),
                    "elapsed": float(stop_match.group("elapsed")),
                }
            )
            if stop_match.group("status") == "success":
                transfer_stats["success"] += 1

    return transfer_events, transfer_stats


# format final statistics when transfer is finished
def get_last_n_lines(file_path, n):
    with open(file_path, 'r') as file:
        # Read the file lines in reverse order
        lines = file.readlines()
        # Get the last n lines
        last_n_lines = lines[-n:]
    return last_n_lines

def extract_statistics(log_lines):
    stats = {}
    for line in log_lines:
        if ':' in line:
            key, value = line.split(':', 1)
            stats[key.strip()] = int(value.strip())
    return stats

def print_statistics(stats):
    print("Source File Transfer Statistics:")
    for key, value in stats.items():
        print(f"{key:<50}: {value}")


def main():
    parser = argparse.ArgumentParser(
        description="Parse a log file for transfer events and statistics."
    )
    parser.add_argument("filename", type=str, help="The log file to parse")
    args = parser.parse_args()

    # Example usage
    with open(args.filename, "r") as file:
        transfer_events, transfer_stats = parse_log(file)

    # Print the parsed transfer events
    # for event in transfer_events:
    #    print(event)


    # Print the transfer statistics
    total_files = transfer_stats["total_files"]
    started = transfer_stats["started"]
    success = transfer_stats["success"]
    progress = (success / total_files) if total_files > 0 else 0

    if progress < 1.0:
        print(f"Total files to transfer: {total_files}")
        if started != 0:
            print(f"Transfers started: {started}")
        else:
            print("Tranfser resumed")
        print(f"Transfers completed successfully: {success}")
        print(f"Progress: {progress:.2%}")
    else:
        last_17_lines = get_last_n_lines(args.filename, 17)
        stats = extract_statistics(last_17_lines)
        print_statistics(stats)


if __name__ == "__main__":
    main()
