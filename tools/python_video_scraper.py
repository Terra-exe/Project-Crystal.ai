from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

# Initialize a Chrome session
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run Chrome in headless mode. Comment this out if you want to see the browser.
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Navigate to the webpage
driver.get('https://marinajacobi.com/player-embed/id/8530')

# Wait for JavaScript to load (adjust time as necessary)
time.sleep(5)

# Attempt to find video URLs
# Note: You may need to adjust the search criteria based on how videos are embedded in your website
video_elements = driver.find_elements(By.TAG_NAME, 'video')
source_elements = driver.find_elements(By.TAG_NAME, 'source')

video_urls = set()

# Extract src from <video> tags
for video in video_elements:
    if video.get_attribute('src'):
        video_urls.add(video.get_attribute('src'))

# Extract src from <source> tags within <video> tags
for source in source_elements:
    if source.get_attribute('src'):
        video_urls.add(source.get_attribute('src'))

# Print found video URLs
print("Found the following video links:")
for video_url in video_urls:
    print(video_url)

# Make sure to close the driver session
driver.quit()