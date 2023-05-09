import datetime
import requests
from lxml import etree
from bs4 import BeautifulSoup

# Define the XML namespaces
xmlns = "http://www.sitemaps.org/schemas/sitemap/0.9"
xmlns_xsi = "http://www.w3.org/2001/XMLSchema-instance"
xsi_schemaLocation = "http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd"

# Define the base URL
base_url = "https://site.com/"

# Get the website HTML
response = requests.get(base_url)
soup = BeautifulSoup(response.text, "html.parser")

# Find all the links in the HTML
urls = []
for link in soup.find_all("a"):
    href = link.get("href")
    if href and href.endswith(".html"):
        url = {"url": href, "priority": "0.80"}
        if href == "index.html":
            url["priority"] = "1.00"
        urls.append(url)

# Create the root element
root = etree.Element("urlset", xmlns=xmlns, xmlns_xsi=xmlns_xsi, xsi_schemaLocation=xsi_schemaLocation)

# Add the URLs to the XML document
for url in urls:
    url_element = etree.SubElement(root, "url")
    loc_element = etree.SubElement(url_element, "loc")
    loc_element.text = base_url + url["url"]
    lastmod_element = etree.SubElement(url_element, "lastmod")
    lastmod_element.text = datetime.datetime.utcnow().isoformat() + "+00:00"
    priority_element = etree.SubElement(url_element, "priority")
    priority_element.text = url["priority"]

# Create the XML document and write it to a file
tree = etree.ElementTree(root)
tree.write("sitemap.xml", encoding="UTF-8", xml_declaration=True, pretty_print=True)