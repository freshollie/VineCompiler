import SeevineDownloader
import VineCompiler
import time
import os

###
# Vine Comp creating bot
# By freshollie
# v-0
# Downloads and compiles popular vines
# Will upload to youtube once completed
###

class VineBot:
    def __init__(self,location='',numVines=100):
        if not location:
            location=time.strftime("%d-%m-%Y")
            part=2
            while os.path.exists(location):
                location=time.strftime("%d-%m-%Y")+'part '+str(part)
                part+=1
        self.numVines=numVines
        self.location=location
        self.run()

    def run(self):
        self.mainloop()

    def mainloop(self):
        SeevineDownloader.Downloader(location=self.location,numberOfVines=self.numVines) #Downloads until 100 videos are collected
        VineCompiler.CreateVideo(location=self.location) #Compiles videos when 100 are collected
        # Will upload video after upload api has been programmed

if __name__ == '__main__':
    VineBot()
    input('Completed')
