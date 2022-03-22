import requests 
import lxml.html


# Open web page that should be passed to lxml
html = requests.get('https://store.steampowered.com/explore/new/')

# doc is an HtmlElement object that contains the XPaths method for extracting 
# information from the html document
doc = lxml.html.fromstring(html.content)

# get all div with that id. Since it can only be one, get the first in the list
new_releases = doc.xpath('//div[@id="tab_newreleases_content"]')[0]

# Get titles
titles = new_releases.xpath('.//div[@class="tab_item_name"]/text()')

# Get prices
prices = new_releases.xpath('.//div[@class="discount_final_price"]/text()')

# Get tags
tags = [tag.text_content() for tag in new_releases.xpath('.//div[@class="tab_item_top_tags"]')]
tags = [tag.split(',') for tag in tags]

# Get platforms
all_platforms = []
platforms = new_releases.xpath('.//div[@class="tab_item_details"]')

for game in platforms:
    temp = game.xpath('.//span[contains(@class, "platform_img")]')
    platform = [t.get('class').split(' ')[-1] for t in temp]
    all_platforms.append(platform)

output = []

for info in zip(titles, prices, tags, all_platforms):
    res = {}
    res['title'] = info[0]
    res['price'] = info[1]
    res['tag'] = info[2]
    res['platform'] = info[3]

    output.append(res)

print(output)
