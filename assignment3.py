import requests
import csv
import re
from collections import defaultdict

# Part I: Pull Down Web Log File
def download_log_file(url):
    response = requests.get(url)

    if response.status_code == 200:
        with open("log_file.csv", "wb") as file:
            file.write(response.content)
        print("File downloaded successfully.")
    else:
        print("Failed to download the file.")

# Part II: Process File Using CSV
def process_log_file():
    with open('log_file.csv', 'r') as file:
        reader = csv.reader(file)

        # Initialize counters and dictionary
        image_hits = 0
        browsers = defaultdict(int)
        hour_hits = defaultdict(int)

        # Iterate over each row in the CSV file
        for row in reader:
            # Check if the row has enough columns
            if len(row) < 5:
                continue  # Skip rows that don't have enough columns

            # Part III: Search for Image Hits
            if re.search(r'\.(jpg|gif|png)$', row[0], re.IGNORECASE):
                image_hits += 1

            # Part IV: Find the most popular browser
            user_agent = row[2] if len(row) > 2 else ""
            if "Firefox" in user_agent:
                browsers["Firefox"] += 1
            elif "Chrome" in user_agent:
                browsers["Chrome"] += 1
            elif "Internet Explorer" in user_agent:
                browsers["Internet Explorer"] += 1
            elif "Safari" in user_agent:
                browsers["Safari"] += 1

            # Part V: Extra Credit - Count hits per hour
            if len(row) > 1:  # Ensure the row has at least 2 columns
                access_time = row[1].split()[1].split(':')[0]
                hour_hits[access_time] += 1

    # Calculate the total hits
    total_hits = sum(hour_hits.values())

    # Calculate the image percentage only if total_hits is not zero
    if total_hits > 0:
        image_percentage = (image_hits / total_hits) * 100
    else:
        image_percentage = 0.0

    print(f"Total hits: {total_hits}")
    print(f"Image requests account for {image_percentage:.1f}% of all requests")

    most_popular_browser = max(browsers, key=browsers.get)
    print(f"The most popular browser is: {most_popular_browser}")

    # Part V: Extra Credit - Print hits per hour
    print("Hits per hour:")
    for hour, hits in sorted(hour_hits.items(), key=lambda x: int(x[0])):
        print(f"Hour {hour} has {hits} hits")

if __name__ == "__main__":
    url = "http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv"
    download_log_file(url)
    process_log_file()

