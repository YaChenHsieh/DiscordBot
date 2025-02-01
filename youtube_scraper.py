import re
import requests

class YouTubeScraper:
    def __init__(self, channel_url):
        """
        Initialize the YouTubeScraper instance
        :param channel_url: Base URL of the YouTube channel (e.g., "https://www.youtube.com/user/PewDiePie")
        """
        self.channel_url = channel_url
        self.html = None  # Stores the downloaded HTML content

    def fetch_html(self):
        """
        Fetch the HTML content from the channel's /videos page
        """
        try:
            response = requests.get(self.channel_url + "/videos")
            response.raise_for_status()  # Check if the HTTP response status is 200 OK
            self.html = response.text
            print(f"HTML content fetched successfully for {self.channel_url}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching HTML content: {e}")
            self.html = None
    
    def get_latest_video_info(self):
        """
        Extract the latest video information and URL from the HTML content
        :return: Dictionary containing video info and URL, or None if extraction fails
        """
        if not self.html:
            print("HTML content is not fetched. Please call fetch_html() first.")
            return None

        try:
            # Extract video information using regex
            info = re.search(r'(?<={"label":").*?(?="})', self.html).group()
            video_id = re.search(r'(?<="videoId":").*?(?=")', self.html).group()
            url = f"https://www.youtube.com/watch?v={video_id}"

            # Extract title from info using regex
            title = info.split(' by ')[0]
            
            # Extract author (e.g., "MrBeast")
            author_match = re.search(r'by ([\w\s]+?) \d', info)
            author = author_match.group(1) if author_match else None

            # Extract video create time from info using regex
            time_match = re.search(r'(\d+ \w+ ago)', info)
            time_ago = time_match.group(1) if time_match else None

            return {"info": info, "title":title, "author":author, "time_ago": time_ago, "url": url}
        except AttributeError:
            print("Failed to extract video information. Please check the regex patterns.")
            return None

if __name__ == "__main__":
    
    # Read channels from a separate file
    yt_list = "youtube_list.txt"

    try:
        with open(yt_list, "r") as file:
            channels = [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print("Error: channels.txt file not found.")
        channels = []

    # Iterate through each channel and fetch its latest video info
    for channel_url in channels:
        print(f"Processing channel: {channel_url}")
        scraper = YouTubeScraper(channel_url)
        scraper.fetch_html()
        latest_video = scraper.get_latest_video_info()

        if latest_video:
            print(f"Video title: {latest_video['title']}")
            print(f"Video author: {latest_video['author']}")
            print(f"Video time_ago: {latest_video['time_ago']}")
            print(f"Video URL: {latest_video['url']}")
        else:
            print("Failed to fetch video information.")
        print("-")
