import os
import threading
import time
import datetime
import sys
from urllib.request import Request,urlopen

# See vine auto compiler
# by freshollie
# V 2.0 After changes to the site
# Lots of 1 line algorithms soz.

class Downloader:
    def __init__(self,location='',numberOfVines=100):
        if location:
            self.location=location+'/'
        else:
            self.location=location
            
        self.numberOfVines=numberOfVines
        self.descDict={}
        self.titlesDict={}
        self.videoNum=0
        self.lastTitle=''
        self.checkNum=0
        self.videosDownloaded=0
        self.downloading={}
        
        if not os.path.exists(self.location+'videos'):        
            os.makedirs(self.location+'videos')
            
        self.urlList=[]
            
        self.desc = open(self.location+'Desc.txt','w')
            
        self.titles = open(self.location+'Titles.txt','w')
        try:
            urls=open('VideoList.txt','a')
            for url in urls.read():
                self.urlList.append(url.strip())
            print(urls)
        except:
            urls=open('VideoList.txt','w')
        
        while True:
            self.downloadVideos()
            if self.videoNum>=self.numberOfVines:
                break
            print('Waiting for next batch...')
            time.sleep(300)

        print('Writing titles')
        orderedKeys=list(self.titlesDict.keys())
        orderedKeys.sort()
        for key in orderedKeys:
            self.titles.write(self.titlesDict[key])
            
        print('Writing description')
        orderedKeys=list(self.descDict.keys())
        orderedKeys.sort()
        for key in orderedKeys:
            self.desc.write(self.descDict[key])

        print('Writing urls')
        for url in self.urlList:
            urls.write(url+'\n')
        
        
        self.titles.close()
        self.desc.close()
                

    def removeOddChars(self,string):
        # Removes the weird &#123213; from the title
        while len(string.split('&#'))>1:
            string=''.join(string.split('&#'+string.split('&#')[-1].split(';')[0]+';')).replace('  ',' ')
        return string
            

    def downloadVideo(self,url,file_name,title):
        '''
        Written by stack overflow
        '''
        
        req = Request(url, headers={'User-Agent' : "Happy Land"})
        #Request error
        u = None
        while not u:
            try:
                u = urlopen(req)
            except:
                time.sleep(1)
                pass
        
        f = open(self.location+'videos/'+str(file_name)+'.mp4', 'wb')
        meta = dict(u.info())
        file_size = int(meta["Content-Length"][0])

        block_sz = 8192
        self.downloading[file_name]=True
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
            f.write(buffer)
        f.close()
        del self.downloading[file_name]
        self.videosDownloaded+=1 # Real time display of number downloaded
        self.lastTitle=title # Show real time display of last title name

    def getVideoUrl(self,htmlsource):
        '''Gets the video url from the video page'''
        return str(htmlsource).split('video id')[1].split('source src="')[1].split('"')[0]

    def getNextVideo(self,htmlsource):
        '''Redundant, used on 1 site'''
        return str(htmlsource).split('class="prevpost"')[0].split('a href="')[-1].split('"')[0]

    def getVideoTitle(self,htmlsource):
        '''Gets title of video from video page'''
        return self.removeOddChars(str(htmlsource).split('"post-title">')[-1].split('</')[0])

    def getVideoAuthor(self,htmlsource):
        '''Gets video author from video page'''
        return self.removeOddChars(str(htmlsource).split('class="name"')[1].split('</a>')[0].split('>')[-1])

    def getVideoTime(self,i):
        '''Gets the current time in the video based on clip number'''
        return str(datetime.timedelta(seconds=round(i*6.47)))
    
        

    def getAllVideos(self,htmlsource):
        '''Collects the video URL's from the front page'''
        urls=[]
        for url in str(htmlsource).split('popular-vines')[-1].split('a href="'):
            url=url.split('">')[0]
            if '/u/' not in url:
                if url!='':
                    urls.append(url)
            else:
                break
        return urls

    def doVideo(self,newUrl,videoNum):
        self.checkNum=0
        self.downloading[videoNum]=False
        time = self.getVideoTime(videoNum)
        req = Request(newUrl, headers={'User-Agent' : "Happy Land"})
        con = None
        
        while not con:
            try:
                con = urlopen(req)
            except:
                time.sleep(1)
                pass
            
        response = con.read()
        
        title=self.getVideoTitle(response)
        author=self.getVideoAuthor(response)
        line = (('%s : %s by %s\n') %(time,title,author))
        justTitle = '%s by %s\n' %(title,author)

        self.titlesDict[videoNum]=justTitle
        self.descDict[videoNum]=line
        
        videoUrl = 'http://www.seenive.com'+self.getVideoUrl(response)
        threading.Thread(target = self.downloadVideo,args =([videoUrl,videoNum,title])).start()
                    
        
    def printStats(self):
        if 'idlelib.run' not in sys.modules:
            os.system('cls')
        print('=====Downloading vines, will run until 100 are collected====')
        print('Videos downloaded: %s' %(self.videosDownloaded))
        print('Last title: %s' %(self.lastTitle))
        print('Currently Downloading: %s' %(len(self.downloading)))

    def downloadVideos(self):
        checkNum=0
        
        while True:
            origUrl='http://www.seevine.com'
            req = Request(origUrl, headers={'User-Agent' : "Happy Land"})
            con=None
            con = urlopen(req)
            while not con:
                try:
                    con = urlopen(req)
                except:
                    time.sleep(1)
                    pass
            
            for url in self.getAllVideos(con.read()):
                newUrl=origUrl+url
                
                if newUrl not in self.urlList:
                    self.urlList.append(newUrl)
                    
                    threading.Thread(target=self.doVideo,args=([newUrl,self.videoNum])).start()
                    self.videoNum+=1
                    
                self.printStats()
               

            self.checkNum+=1
            if self.checkNum>10:
                while self.downloading:
                    self.printStats()
                return
            
if __name__=='__main__':
    Downloader()
