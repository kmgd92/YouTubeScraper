import bs4
import requests
import datetime
import time
import db


#Parses rssUrl for all video ids and time publish adds each new video when posted
#params (Name of Youtuber, rssUrl of Youtubers videos page)
def getUserVideos(Youtuber, rssUrl):
    url = rssUrl
    html = requests.get(url)
    soup = bs4.BeautifulSoup(html.text, "html.parser")

    #get videoId from db and hold in dictionary
    videoStore = {}
    dbData = db.getVidIDs()
    for vid in dbData:
        videoStore[vid] = ""

    #current time in UTC
    currentTime = []
    currentTime.append(int(datetime.datetime.utcnow().strftime("%Y")))
    currentTime.append(int(datetime.datetime.utcnow().strftime("%m")))
    currentTime.append(int(datetime.datetime.utcnow().strftime("%d")))
    currentTime.append(int(datetime.datetime.utcnow().strftime("%H")))
    currentTime.append(int(datetime.datetime.utcnow().strftime("%M")))

    #Check youtube every 60 seconds for a new video, add to db and notify video was added
    while(True):
        for entry in soup.find_all("entry"):
            for pub in entry.find_all("id"):
                pub = str.split(pub.text, ':')
                if pub[2] not in videoStore:
                    print(str(pub[2]))
                    videoStore.update({pub[2]: currentTime})
                    db.insertVid(Youtuber,str(pub[2]),str(currentTime))
                    print("New Video added")
                    print(currentTime)
        time.sleep(60)


if __name__ == '__main__':
    getUserVideos("BitBoy Crypto", "https://www.youtube.com/feeds/videos.xml?channel_id=UCjemQfjaXAzA-95RKoy9n_g")



