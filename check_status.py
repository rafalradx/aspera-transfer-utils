import re
import argparse


def parse_log(file):
    transfer_start_pattern = re.compile(
        r'LOG FASP Transfer Start uuid=(?P<uuid>[a-f0-9-]+) op=send status=(?P<status>\w+) file="(?P<file>[^"]+)" size=(?P<size>\d+) start_byte=\d+ rate=(?P<rate>[\d.]+)Mbps loss=[\d.]+ rexreqs=\d+ overhead=\d+'
    )
    transfer_stop_pattern = re.compile(
        r'LOG FASP Transfer Stop uuid=(?P<uuid>[a-f0-9-]+) op=send status=(?P<status>\w+) file="(?P<file>[^"]+)" size=(?P<size>\d+) start_byte=\d+ rate=(?P<rate>[\d.]+)Mbps elapsed=(?P<elapsed>[\d.]+)s loss=[\d.]+ rexreqs=\d+ overhead=\d+'
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
                    "uuid": start_match.group("uuid"),
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
                    "uuid": stop_match.group("uuid"),
                    "status": stop_match.group("status"),
                    "file": stop_match.group("file"),
                    "size": int(stop_match.group("size")),
                    "rate": float(stop_match.group("rate")),
                    "elapsed": float(stop_match.group("elapsed")),
                }
            )
            if stop_match.group("status") == "success":
                transfer_stats["success"] += 1
                transfer_stats["total_time"] += float(stop_match.group("elapsed"))

    return transfer_events, transfer_stats


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
    print(f"Total files to transfer: {transfer_stats['total_files']}")
    print(f"Transfers started: {transfer_stats['started']}")
    print(f"Transfers completed successfully: {transfer_stats['success']}")
    completed = transfer_stats["success"] / transfer_stats["total_files"]
    print(f"Progress: {completed:.2%}")
    elapsed_hours = transfer_stats["total_time"] / 3600
    print(f"Total transfer time: {elapsed_hours:.2} h")


if __name__ == "__main__":
    main()
