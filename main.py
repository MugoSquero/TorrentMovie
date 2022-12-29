import requests
from lxml.html import fromstring
from json import loads
import re

requests.packages.urllib3.disable_warnings()

results = ""

#Change the location where you want to downlod torrent files
locationToDownload = "D:\\Movies\\"

def scrapeText(text, start, end):
    if end == '':
        end = text[-1]
    start_index = text.find(start)
    if start_index == -1:
        # start text not found
        scrape = ""
    else:
        end_index = text.find(end, start_index)
        if end_index == -1:
            # end text not found
            scrape = ""
        else:
            # start and end texts found, extract the text between them
            scrape = text[start_index + len(start):end_index]
    
    return scrape


def downloadTorrent(purl):
    global locationToDownload
    response = requests.get(purl)
    torrentUrl = response.headers['content-disposition']
    torrentUrl = scrapeText(torrentUrl, "attachment; filename=\"", " [YTS.MX].torrent\"") + ".torrent"
    print("Downloading: " + torrentUrl)
    with open(locationToDownload + torrentUrl, "wb") as file:
        file.write(response.content)


def alternativeSearch(pimdb):
    headers = {"User-Agent": "My-User-Agent/1.0", "Accept-Language": "en-US", "Accept-Encoding": "gzip, deflate",}
    if pimdb.startswith('tt'):
        response = requests.get("https://www.imdb.com/title/" + pimdb, verify=False, headers=headers)
        tree = fromstring(response.content)
        pimdb = tree.findtext('.//title').replace(" - IMDb", "")
    response = requests.get("https://snowfl.com/FygTUUoAMkCRguGHWrYmREEYTwGHEuljZNpeXwCnw/{}/sIlCauM6/0/SEED/NONE/1".format(pimdb), verify=False, headers=headers)
    print("Torrents are displaying, please select one index number to download!!\n")
    for i in range(5):
        torrents = loads(response.text)[i]
        print("Index: {}\n\tName: {}\n\tSize: {}\n\tSeeder: {}\n\tLeecher: {}\n\tType: {}".format(i, torrents['name'], torrents['size'], torrents['seeder'], torrents['leecher'], torrents['type']))
    
    indexTorrent = int(input("Please enter the index number of the torrent you want to download: "))
    torrents = loads(response.text)[indexTorrent]
    try:
        magnetUrl = torrents['magnet']
    except KeyError:
        magnetUrl = torrents['url']
    if 'magnet:' in magnetUrl:
        print("Download URL:\n\n" + magnetUrl)
    else:
        print("Couldn't fetch the magnet URL, please download it manually from this URL:\n\n" + magnetUrl)
    GoodBye()


def GoodBye():
    print("\nGoodbye.")
    exit()

imdbTitle = input("Please enter the imdb title (tt*) or the name of a movie : ")
if not imdbTitle.startswith('tt'):
    response = requests.get("https://yts.mx/ajax/search?query=" + imdbTitle, verify=False)
    iresponse = loads(response.text)
    if not iresponse['status'] == "ok":
        checkAlternative = input("YTS is missing that movie, do you want an alternative? (Y/n): ").lower()
        if checkAlternative == '' or checkAlternative == 'y':
            alternativeSearch(imdbTitle)
        else:
            GoodBye()
    for i in range(5):
            results = loads(response.text)['data'][i]
            print("Index: {}\n\tTitle: {}\n\tYear: {}".format(i, results['title'], results['year']))
    indexResult = int(input("Please enter the index number of the movie you want to download: "))
    results = loads(response.text)['data'][indexResult]['url']

if results == "":
    response = requests.get("https://yts.mx/ajax/search?query=" + imdbTitle, verify=False)
    
    ytsUrl = loads(response.text)
    
    if not ytsUrl['status'] == "ok":
        checkAlternative = input("YTS is missing that movie, do you want an alternative? (Y/n): ").lower()
        if checkAlternative == '' or checkAlternative == 'y':
            alternativeSearch(imdbTitle)
        else:
            GoodBye()
    
    ytsUrl = loads(response.text)['data'][0]['url']

else:
    ytsUrl = results

response = requests.get(ytsUrl, verify=False)

baseUrls = scrapeText(response.text, "<em class=\"pull-left\">Available in: &nbsp;</em>", "<br><br>")

baseUrls = baseUrls.split('\n')

p720 = scrapeText(baseUrls[1], "<a href=\"", "720p.BluRay</a>")
p1080 = scrapeText(baseUrls[2], "<a href=\"", "1080p.BluRay</a>")

if p720 == '':
    askWeb = input("There is no option for BlueRay. Do you want WEB version instead? (y/N): ").lower()
    if askWeb == '' or askWeb == "n":
        GoodBye()
    else:
        p720 = scrapeText(baseUrls[1], "<a href=\"", "720p.WEB</a>")
        p1080 = scrapeText(baseUrls[2], "<a href=\"", "1080p.WEB</a>")


p720 = re.findall("https://yts.mx/torrent/download/[0-9a-zA-Z]*", p720)[0]
p1080 = re.findall("https://yts.mx/torrent/download/[0-9a-zA-Z]*", p1080)[0]

downloadTorrent(p720)
downloadTorrent(p1080)