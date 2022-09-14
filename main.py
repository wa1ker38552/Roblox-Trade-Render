from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image
import requests
import random
import os


def render_trade(requesting, offering):
  itemtable = requests.get('https://www.rolimons.com/itemapi/itemdetails').json()['items']
  request = requests.get(f'https://thumbnails.roblox.com/v1/assets?assetIds={",".join([str(i) for i in requesting+offering])}&size=150x150&format=Png&isCircular=false')
  for item in request.json()['data']:
    im = requests.get(item['imageUrl'])
    with open(f'assets/items/{item["targetId"]}.png', 'wb') as file:
      file.write(im.content)

  template = Image.open('assets/template.png')
  for i, item in enumerate(requesting):
    itm = Image.open(f'assets/items/{item}.png')
    template.paste(itm, (i*200+30, 30), itm)

  for i, item in enumerate(offering):
    itm = Image.open(f'assets/items/{item}.png')
    template.paste(itm, (i*200+30, 250), itm)

  x = ImageDraw.Draw(template)
  f = ImageFont.truetype('assets/P22.ttf', 15)
  for i, item in enumerate(requesting): 
    x.text((i*200+30, 180), itemtable[str(item)][0], font=f, fill=(0, 0, 0))
    x.text((i*200+30, 200), str(itemtable[str(item)][2]), font=f, fill=(0, 0, 0))
    x.text((i*200+30, 220), str(itemtable[str(item)][3]), font=f, fill=(0, 0, 0))
  for i, item in enumerate(offering): 
    x.text((i*200+30, 400), itemtable[str(item)][0], font=f, fill=(0, 0, 0))
    x.text((i*200+30, 420), str(itemtable[str(item)][2]), font=f, fill=(0, 0, 0))
    x.text((i*200+30, 440), str(itemtable[str(item)][3]), font=f, fill=(0, 0, 0))

  f = ImageFont.truetype('assets/P22.ttf', 30)
  x.text((30, 30), 'Items you will give:', font=f, fill=(0, 0, 0))
  x.text((30, 250), 'Items you will recieve:', font=f, fill=(0, 0, 0))
  
  offering_value = sum([itemtable[str(i)][3] if itemtable[str(i)][3] != -1 else itemtable[str(i)][2]  for i in offering])
  requesting_value = sum([itemtable[str(i)][3] if itemtable[str(i)][3] != -1 else itemtable[str(i)][2] for i in requesting])
  value = f'+{str(offering_value-requesting_value)}' if not '-' in str(offering_value-requesting_value) else str(offering_value-requesting_value)
  
  f = ImageFont.truetype('assets/P22.ttf', 20)
  color = (255, 0, 0) if requesting_value > offering_value else (0, 255, 0)
  x.text((350, 270), str(offering_value), font=f, fill=color)
  x.text((350, 250), str(requesting_value), font=f, fill=color)
  x.text((450, 260), value, font=f, fill=color)
  template.save('assets/fn.png')

  for item in os.listdir('assets/items'):
    os.remove(f'assets/items/{item}')
  

while True:
  trade = requests.get('https://www.rolimons.com/tradeadsapi/getrecentads').json()['trade_ads'][random.randint(1, 80)]
  try:
    render_trade(trade[4]['items'], trade[5]['items'])
    break
  except KeyError: pass
