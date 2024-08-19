import re
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime


def parse_log_line(line):
    """Parse a single log line and return a dictionary with extracted information."""
    # Define the regex pattern to match the log line format
    pattern = r'(\d+\.\d+\.\d+\.\d+) .+ \[(.+)\] "(\w+) (.+) HTTP/\d\.\d" (\d+) (\d+) .+ requestsuccessful: (\d+)\s+requestfailed: (\d+)'
    # Attempt to match the pattern against the log line
    match = re.match(pattern, line)
    
    # If a match is found, extract and return the information
    if match:
        return {
            'ip': match.group(1),  # Extract the IP address
            'timestamp': datetime.strptime(match.group(2), "%d/%b/%Y:%H:%M:%S %z"),  # Parse the timestamp
            'method': match.group(3),  # Extract the HTTP method
            'path': match.group(4),  # Extract the requested path
            'status': int(match.group(5)),  # Extract and convert the status code to an integer
            'bytes': int(match.group(6)),  # Extract and convert the bytes transferred to an integer
            'successful': int(match.group(7)),  # Extract and convert the successful requests count to an integer
            'failed': int(match.group(8))  # Extract and convert the failed requests count to an integer
        }
    
    # If no match is found, return None
    return None

def analyze_logs(logs):
    """Perform various analyses on the parsed logs."""
    # Initialize a dictionary to store different types of analyses
    analyses = {
        'ip_counts': defaultdict(int),  # Count of requests per IP address
        'method_counts': defaultdict(int),  # Count of requests per HTTP method
        'status_counts': defaultdict(int),  # Count of requests per status code
        'hourly_requests': defaultdict(int),  # Count of requests per hour
        'total_bytes': 0,  # Total bytes transferred
        'total_successful': 0,  # Total number of successful requests
        'total_failed': 0  # Total number of failed requests
    }

    # Iterate through each log entry
    for log in logs:
        # Increment the count for this IP address
        analyses['ip_counts'][log['ip']] += 1
        
        # Increment the count for this HTTP method
        analyses['method_counts'][log['method']] += 1
        
        # Increment the count for this status code
        analyses['status_counts'][log['status']] += 1
        
        # Increment the count for the hour of this request
        analyses['hourly_requests'][log['timestamp'].hour] += 1
        
        # Add the bytes transferred in this request to the total
        analyses['total_bytes'] += log['bytes']
        
        # Add the successful requests count from this log to the total
        analyses['total_successful'] += log['successful']
        
        # Add the failed requests count from this log to the total
        analyses['total_failed'] += log['failed']

    # Return the completed analyses
    return analyses

def create_visualizations(analyses):
    """Create visualizations based on the log analyses."""
    # IP address bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(analyses['ip_counts'].keys(), analyses['ip_counts'].values())
    plt.title('Requests by IP Address')
    plt.xlabel('IP Address')
    plt.ylabel('Number of Requests')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('ip_requests.png')
    plt.close()

    # Hourly requests line chart
    plt.figure(figsize=(12, 6))
    hours = sorted(analyses['hourly_requests'].keys())
    requests = [analyses['hourly_requests'][hour] for hour in hours]
    plt.plot(hours, requests, marker='o')
    plt.title('Hourly Request Distribution')
    plt.xlabel('Hour of Day')
    plt.ylabel('Number of Requests')
    plt.xticks(range(0, 24))
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('hourly_requests.png')
    plt.close()

def save_to_csv_and_excel(logs, analyses, csv_file, excel_file):
    """Save parsed logs and analyses to CSV and Excel files."""
    # Create DataFrames
    logs_df = pd.DataFrame(logs)
    
    # Remove timezone information from datetime objects
    logs_df['timestamp'] = logs_df['timestamp'].dt.tz_localize(None)
    
    analyses_df = pd.DataFrame({
        'Metric': ['Total Bytes', 'Total Successful Requests', 'Total Failed Requests'],
        'Value': [analyses['total_bytes'], analyses['total_successful'], analyses['total_failed']]
    })

    # Save to CSV
    logs_df.to_csv(csv_file, index=False)
    
    # Save to Excel
    logs_df.to_excel(excel_file, sheet_name='Parsed Logs', index=False)
    analyses_df.to_excel(excel_file, sheet_name='Summary', index=False)
    pd.DataFrame(analyses['ip_counts'].items(), columns=['IP', 'Count']).to_excel(excel_file, sheet_name='IP Counts', index=False)
    pd.DataFrame(analyses['method_counts'].items(), columns=['Method', 'Count']).to_excel(excel_file, sheet_name='Method Counts', index=False)
    pd.DataFrame(analyses['status_counts'].items(), columns=['Status', 'Count']).to_excel(excel_file, sheet_name='Status Counts', index=False)

def main():
    log_file = 'apache_logs.txt'
    csv_file = 'parsed_logs.csv'
    excel_file = 'log_analysis.xlsx'

    # Read and parse log file
    with open(log_file, 'r') as file:
        logs = [parse_log_line(line) for line in file if parse_log_line(line)]

    # Analyze logs
    analyses = analyze_logs(logs)

    # Create visualizations
    create_visualizations(analyses)

    # Save to CSV and Excel
    save_to_csv_and_excel(logs, analyses, csv_file, excel_file)

    print(f"Log analysis complete. Results saved to {csv_file} and {excel_file}")

if __name__ == "__main__":
    main()