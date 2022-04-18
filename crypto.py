from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from requests import TooManyRedirects
from twilio.rest import Client
from keys import accountSID, authToken

TwilioNumber = '+17624755435'
mycellphone = '+12816155559'
client = Client(accountSID, authToken)

url = 'https://finance.yahoo.com/cryptocurrencies/?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&guce_referrer_sig=AQAAAG-133v3mUV48r6QY0iSyxLbQe8617Jhz7IFnl44acwvba-5iK0EgtuKebriO4SV8PaZqxeqVTSd1-CIrqQbteoOcA-0S26iDARRfxLLkua7jBeD5xHQCMCUueh5dMDYN5Wiu5KoXc1yyrgDRK4PAAFk13gSwI47IAwWnVR18frw'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
req = Request(url, headers=headers)
webpage = urlopen(req).read()
soup = BeautifulSoup(webpage, 'html.parser')

table_rows = soup.findAll("tr")

for row in table_rows[1:6]:
    title = row.findAll("td", attrs={"aria-label":"Name"})[0].text
    symbol = row.findAll("a")[0].text
    cur_price = float(row.findAll("fin-streamer")[0].text.replace(',',''))
    change_percentage = float(row.findAll("fin-streamer")[2].text.replace('+','').replace('%',''))
    prev_price = round(cur_price/(1+(.001 * change_percentage)),2)
    print("Name: " + title)
    print("Symbol: " + symbol)
    print("Current Price: " + "${:,.2f}". format(cur_price))
    print("Previous Price: " + "${:,.2f}". format(prev_price))
    print("Percent Change: " + str(change_percentage) + '%\n')
    if symbol == 'BTC-USD' and cur_price < 40000:
        btc_message = client.messages.create(to=mycellphone, from_=TwilioNumber,body="BTC is below $40,000")
    if symbol == 'ETH-USD' and cur_price < 3000:
        eth_message = client.messages.create(to=mycellphone, from_=TwilioNumber,body="ETH is below $3,000")