import requests
import xml.etree.ElementTree as ET

url = "https://hnrss.org/newest?q=Signal&points=99"
response = requests.get(url)

if response.status_code == 200:
    root = ET.fromstring(response.text)
    # Find the first <item> and extract the <link>
    link = root.find(".//item/link").text
    print(link)  # This is the final URL we need
else:
    print("Error fetching data")