from moviepy.editor import *
import threading
import os
import time
import sys
import re

def tryint(s):
    try:
        return int(s)
    except:
        return s

def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

def sort_nicely(l):
    """ Sort the given list in the way that humans expect.
    """
    
    l.sort(key=alphanum_key)

vines = []

class ClipCompiler:

    def __init__(self,location):
        self.location=location
        self.vines=[]
        self.run()

    def makeVine(self,num,title,file):
        vine = VideoFileClip(self.location+'videos/%s' %(file))# Video clip object of current clip
                
        txt = TextClip(title, font='Amiri-regular',
                       color='white',fontsize=12).set_duration(vine.duration)
                                                  # Generate an overlay based off
                                                  # the video title
        txt_col = txt.on_color(size=(txt.w+10,txt.h),
                  color=(0,0,0), pos=(6,'center'), col_opacity=0.6)
        # ^ Add coloured background to the clip
        
        finalClip = CompositeVideoClip([vine,txt_col.set_pos((0,'bottom'))])
        # ^ Adds the title to the video clip
        self.vines.append(finalClip) # Adds the clip to a list of clips
        

    def run(self):
        i=0
        with open(self.location+'titles.txt') as titles:
            videoList=os.listdir(self.location+'videos')
            sort_nicely(videoList)
            for file in videoList:
                title = titles.readline() #titles in the compiled titles file
                self.makeVine(i,title,file)
                if 'idlelib.run' not in sys.modules:
                    os.system('cls')
                print('===Compiling vines into video===')
                print('Clips completed: %s/%s' %(len(self.vines),len(videoList)))
                print(title)
                i+=1
    
                
                
        

class CreateVideo:
    def __init__(self,location=''):
        if location:
            self.location=location+'/'
        else:
            self.location=location
        
        vines=ClipCompiler(self.location).vines
        print('Compiling clips')

        compiled = concatenate_videoclips(vines)
        # ^Compile clips together

        print('Adding background')

        background=ImageClip('background.png').set_duration(compiled.duration) # Load background image

        moviesize=background.size

        print('Resizing')
        compiled=compiled.resize(height=moviesize[1],width=compiled.size[0]*(moviesize[1]/compiled.size[1])).set_pos('center')
        #Changes to size of background but keeps same resolution

        final = CompositeVideoClip([background,compiled])
        # Add background image to forground of clips
        final.write_videofile(self.location+'%s.mp4' %(time.strftime("%d-%m-%Y")), fps=29.97, codec='libx264')
        # ^ save file with todays date ready for upload

if __name__=='__main__':
    CreateVideo()
