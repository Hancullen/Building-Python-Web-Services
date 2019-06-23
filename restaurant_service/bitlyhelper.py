from urllib.request import urlopen, quote
import json

TOKEN = '493ce31c599b5530f412a29dd544f793fb0d1048'
ROOT_URL = "https://api-ssl.bitly.com/"
SHORTEN = "/v3/shorten?access_token={}&longUrl={}"

class BitlyHelper:
    def shorten_url(self, longurl):
        try:
            url = ROOT_URL + SHORTEN.format(TOKEN, quote(longurl))
            response = urlopen(url).read()
            jr = json.loads(response)
            return jr['data']['url']
        except Exception as e:
            print (e)
