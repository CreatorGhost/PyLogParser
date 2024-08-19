import random
from datetime import datetime, timedelta

# List of sample IP addresses, methods, paths, user agents, and statuses
ips = ["54.36.149.41", "31.56.96.51", "40.77.167.129", "91.99.72.15", "66.249.66.194", "207.46.13.136", "178.253.33.51"]
methods = ["GET", "POST", "PUT", "DELETE"]
paths = ["/filter/27|13%20%D9%85%DA%AF%D8%A7%D9%BE%DB%8C%DA%A9%D8%B3%D9%84", "/image/60844/productModel/200x200", "/product/31893/62100/%D8%B3%D8%B4%D9%88%D8%A7%D8%B1", "/settings/logo"]
user_agents = [
    "Mozilla/5.0 (compatible; AhrefsBot/6.1; +http://ahrefs.com/robot/)",
    "Mozilla/5.0 (Linux; Android 6.0; ALE-L21 Build/HuaweiALE-L21) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.158 Mobile Safari/537.36",
    "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0)Gecko/16.0 Firefox/16.0",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
]
statuses = [200, 404, 500, 301]

# Function to generate a random log entry
def generate_log_entry():
    ip = random.choice(ips)
    timestamp = (datetime.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23), minutes=random.randint(0, 59))).strftime("%d/%b/%Y:%H:%M:%S +0330")
    method = random.choice(methods)
    path = random.choice(paths)
    status = random.choice(statuses)
    bytes_sent = random.randint(1000, 50000)
    user_agent = random.choice(user_agents)
    request_successful = random.randint(0, 300)
    request_failed = random.randint(0, 300)
    
    log_entry = f'{ip} - - [{timestamp}] "{method} {path} HTTP/1.1" {status} {bytes_sent} "-" "{user_agent}" "-" requestsuccessful: {request_successful}  requestfailed: {request_failed}'
    return log_entry

# Generate a log file with random entries
def generate_log_file(filename, num_entries):
    with open(filename, 'w') as file:
        for _ in range(num_entries):
            file.write(generate_log_entry() + "\n")

# Generate 100 random log entries and save to 'generated_logs.txt'
generate_log_file('generated_logs.txt', 100)