#!/usr/bin/env python

import pygame, random, sys, math, subprocess, threading, os, csv
import numpy as np
from pygame.locals import *
from overspec_stimgen_v2 import cols, gs, ks, nouns, anis, frvs, exps, numTrials

filePath = '/Users/jia/Desktop/overspec/'   # to change
imgW, imgH = 400, 400
boxW, boxH = 436, 436

def begin():
    
    global canvas, xc, yc, imagePositions, arrowPositions, boxPositions
    
    pygame.init()
    pygame.mixer.init(44100, -16, 2, 2048)
    
    scrRes = pygame.display.Info()
    scrWidth = scrRes.current_w
    scrHeight = scrRes.current_h
    xc = scrWidth/2
    yc = scrHeight/2
    mousePos = [xc, yc]
    imagePositions = {'L': (0.5*xc-imgW/2, 0.95*yc-imgH/2), 'R': (1.5*xc-imgW/2, 0.95*yc-imgH/2), 'C': (xc-55,1.8*yc-20)}
    boxPositions = {'L': (0.5*xc-boxW/2, 0.95*yc-boxH/2), 'R': (1.5*xc-boxW/2, 0.95*yc-boxH/2)}
    arrowPositions = {'L': (0.5*xc-30, 0.95*yc-boxH/2-90), 'R': (1.5*xc-30, 0.95*yc-boxH/2-90)}
    
    canvas = pygame.display.set_mode((scrWidth, scrHeight), 0, 32)
    canvas.fill((255, 255, 255))
    pygame.display.set_caption(' ')
    
#####################################
###### functions to load dicts ######

def loadImages():
    # pre-load images for critical and filler stims
    # returns dict of images with key, val pairs corresponding to image name, image (pygame object)
    global stimDict
    stimDict = {}
    for n in range(len(nouns)):
        for c in range(len(cols)):
            imgName = '_'.join([nouns[n],cols[c]])
            stimDict[imgName] = pygame.image.load('{}stims/{}.png'.format(filePath, imgName))
    #images = ['_'.join([nouns[n], cols[c]]) for n in range(len(nouns)) for c in range(len(cols))]
    for a in anis:
        stimDict[a] = pygame.image.load('{}stims/filler_images/animals/{}.png'.format(filePath, a))
    for f in frvs:
        stimDict[f] = pygame.image.load('{}stims/filler_images/fruitveg/{}.png'.format(filePath, f))
    for gdr in ['f', 'm']:
        for exp in exps:
            for i in range(1,5):
                stimDict['{}_{}{}'.format(gdr, exp, i)] = pygame.image.load('{0}stims/filler_images/{1}/{2}/{1}_{2}{3}.png'.format(filePath, gdr, exp, i))
    stimDict['boxB'] = pygame.image.load('{}stims/box_b.png'.format(filePath))
    stimDict['stream'] = pygame.image.load('{}stims/stream.png'.format(filePath))
    stimDict['streamGrey'] = pygame.image.load('{}stims/stream_grey.png'.format(filePath))
    stimDict['streamBlank'] = pygame.image.load('{}stims/stream_blank.png'.format(filePath))
    stimDict['nochimney'] = pygame.image.load('{}stims/nochimney.png'.format(filePath))
    stimDict['chimney'] = pygame.image.load('{}stims/chimney.png'.format(filePath))
    stimDict['arrow'] = pygame.image.load('{}stims/arrow.png'.format(filePath))
    stimDict['begin'] = pygame.image.load('{}stims/begin.png'.format(filePath))
    stimDict['connect'] = pygame.image.load('{}stims/connect.png'.format(filePath))
    return stimDict

def loadAudio(audioDir):
    # pre-load sound files, stores in dict obj
    # commenting stuff out depending on whether the final expt plays via pygame mixer or piping sox through command line (sox play currently doesn't seem to work on AT lab computers)
    # pygame version loads files as pygame mixer Sound objects
    # sox version loads files as string objects
    global audioDict
    audioDict = {}
    audioDict['instructions'] = '{}{}/inst_audio.wav'.format(filePath, audioDir)
    for n in range(len(nouns)):
        for c in range(len(cols)):
            fileName = '_'.join([nouns[n],cols[c]])
            # audioDict[fileName] = pygame.mixer.Sound('{}{}/{}.wav'.format(filePath, audioDir, fileName))
            audioDict[fileName] = '{}{}/{}.wav'.format(filePath, audioDir, fileName)
    for a in anis:
        # audioDict[a] = pygame.mixer.Sound('{}{}/filler_audio/animals/{}.wav'.format(filePath, audioDir, a))
        audioDict[a] = '{}{}/filler_audio/animals/{}.wav'.format(filePath, audioDir, a)
    for f in frvs:
        # audioDict[f] = pygame.mixer.Sound('{}{}/filler_audio/fruitveg/{}.wav'.format(filePath, audioDir, f))
        audioDict[f] = '{}{}/filler_audio/fruitveg/{}.wav'.format(filePath, audioDir, f)
    for gdr in ['f', 'm']:
        for exp in exps:
            for i in range(1,4):
                # audioDict['{}_{}{}'.format(gdr, exp, i)] = pygame.mixer.Sound('{0}{1}/filler_audio/{2}/{3}/{2}_{3}{4}.wav'.format(filePath, audioDir, gdr, exp, i))
                audioDict['{}_{}{}'.format(gdr, exp, i)] = '{0}{1}/filler_audio/{2}/{3}/{2}_{3}{4}.wav'.format(filePath, audioDir, gdr, exp, i)
    # audioDict['disfluency'] = [pygame.mixer.Sound('{}{}/disfluency.wav'.format(filePath, audioDir)), pygame.mixer.Sound('{}{}/disfluency2.wav'.format(filePath, audioDir))]
    # audioDict['ok'] = pygame.mixer.Sound('{}{}/ok.wav'.format(filePath, audioDir))
    # audioDict['clickon'] = [pygame.mixer.Sound('{}{}/clickon.wav'.format(filePath, audioDir)), pygame.mixer.Sound('{}{}/clickon2.wav'.format(filePath, audioDir))]
    # audioDict['clickonDisf'] = pygame.mixer.Sound('{}{}/clickondisf.wav'.format(filePath, audioDir))
    # audioDict['soundCheck'] = pygame.mixer.Sound('{}{}/soundcheck.wav'.format(filePath, audioDir))    
    audioDict['disfluency'] = ['{}{}/disfluency.wav'.format(filePath, audioDir), '{}{}/disfluency2.wav'.format(filePath, audioDir)]
    audioDict['ok'] = '{}{}/ok.wav'.format(filePath, audioDir)
    audioDict['clickon'] = ['{}{}/clickon.wav'.format(filePath, audioDir), '{}{}/clickon2.wav'.format(filePath, audioDir)]
    audioDict['clickonDisf'] = '{}{}/clickondisf.wav'.format(filePath, audioDir)
    audioDict['soundCheck'] = '{}{}/soundcheck.wav'.format(filePath, audioDir)
    return audioDict

#####################################
###### functions i'm reusing ########

def record(recsDirPath, trialNo):
    rec = subprocess.Popen(['sox -d -c 1 -b 16 -r 44100 {}/trial{}.wav'.format(recsDirPath, trialNo)], shell=True)
    
def displayText(text, fontSize, xyCoords, colour=(0,0,0)):
    # displays text string centred on xyCoords
    font = pygame.font.SysFont('Arial', fontSize)
    text = font.render(text, 1, colour)
    text_rect = text.get_rect(center=(xyCoords))
    canvas.blit(text, text_rect)
    return text_rect

def displayTextMultiline(text, fontSize, textPos, textSize, colour=(0,0,0)):
    # function to blit multiline text to surface because there is no easy way to do this in pygame
    # textPos specifies position of top left corner of textarea within the surface
    # textSize specifies size of the textarea
    font = pygame.font.SysFont('Arial', fontSize)
    words = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]  # specify space width
    maxWidth, maxHeight = textSize    # specify textarea size
    x, y = textPos
    for line in words:
        for word in line:
            wordSurface = font.render(word, 1, colour)
            wordWidth, wordHeight = wordSurface.get_size()
            if x + wordWidth >= maxWidth:
                x = textPos[0]      # reset x pos
                y += wordHeight     # start on new row
            canvas.blit(wordSurface, (x, y))
            x += wordWidth + space
        x = textPos[0]
        y += wordHeight

def centreMouse():
    pygame.mouse.set_pos([xc,yc])
    pygame.mouse.set_visible(1)

def clearCanvas():
    pygame.mouse.set_visible(0)
    canvas.fill((255,255,255))
    pygame.display.update()
    
def waitForClick(leftObjDims, rightObjDims):
    # wait for mouse click on match trials
    # object dimensions must be in the form of a tuple corresponding to
    # object x centre, object y centre, object width, object height
    
    leftObjXC, leftObjYC, leftObjW, leftObjH = leftObjDims[0], leftObjDims[1], leftObjDims[2], leftObjDims[3]
    rightObjXC, rightObjYC, rightObjW, rightObjH = rightObjDims[0], rightObjDims[1], rightObjDims[2], rightObjDims[3]
    
    centreMouse()
    clicked = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        x,y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]==1:
            if leftObjXC-0.5*leftObjW<x<leftObjXC+0.5*leftObjW and leftObjYC-0.5*leftObjH<y<leftObjYC+0.5*leftObjH:
                clicked = 'L'
                break
            elif rightObjXC-0.5*rightObjW<x<rightObjXC+0.5*rightObjW and rightObjYC-0.5*rightObjH<y<rightObjYC+0.5*rightObjH:
                clicked = 'R'
                break
    
    return clicked

def wait(timeInMs, clear=False):
    # waits for a specified duration (ms)
    # optional: clears canvas after
    t0 = pygame.time.get_ticks()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(), pygame.quit()
        tE = pygame.time.get_ticks() - t0
        pygame.display.update()
        if tE > timeInMs:
            break
    if clear==True:
        clearCanvas()
        
########################################
###### functions for current expt ######
        
def get_stim_spreadsheet(subjNo):
    # reads in stim spreadsheet generated by overspec_stimgen module
    # returns list of strings with each string corresponding to trial stim
    stimFileName = 'sub{}.csv'.format(subjNo)
    
    with open('{0}stimgens/{1}'.format(filePath, stimFileName), 'rb') as f:
        stimDF = f.readlines()
        
        return stimDF

def show_instructions(trialTask):
    instDict = {'loading': ['Please wait while your partner connects to the network', 0.3*yc],
                'loadingSuccess': ['Ok! Now let\'s check the audio streaming.', 0.95*yc],
                'soundCheck1': ['When you see this mic symbol, it means your partner can hear you speak.', 0.3*yc],
                'soundCheck2': ['Now try to say the following instruction to your partner:', 0.7*yc],
                'soundCheck3': ['"Please click on the basket of bread."', 0.9*yc],
                'soundCheck4': ['Click on the mic when you finish speaking', 1.65*yc],
                'soundCheck5': ['Great! Now your partner will send an instruction to you.', 0.95*yc],
                'soundCheckFinish': ['Ok that\'s fine! The experiment will now begin.', yc],
                'match': ['Listen to your partner\'s description', 0.15*yc],
                'match2': ['Now click on the picture your partner described', 0.3*yc],
                'dir': ['Describe the picture that the arrow is pointing at to your partner', 0.15*yc],
                'dir2': ['Click on the mic when you finish speaking', 1.65*yc],
                'dir3': ['Wait while your partner clicks on a picture...', 1.78*yc]}
    displayText(instDict[trialTask][0], 24, (xc, instDict[trialTask][1]))
    pygame.display.update()

def show_image(objName, pos):
    # draws targ/dist image on screen
    canvas.blit(objName, imagePositions[pos])
    pygame.display.update()

def show_box(box, boxPos):
    # draws box around targ/dist image on screen
    canvas.blit(box, boxPositions[boxPos])
    pygame.display.update()
    
def show_arrow(arrowPos):
    # displays arrow pointing to target image to be described on screen
    canvas.blit(stimDict['arrow'], arrowPositions[arrowPos])
    pygame.display.update()
    
def show_mic(micImage):
    # displays mic (streaming icon) on screen
    canvas.blit(stimDict[micImage], (xc-60, 1.45*yc-60))
    pygame.display.update()

def play_sound_files(tempo, *soundFiles):
    # invokes sox in the terminal via subprocess to play sound files
    # ###### ------UPDATE (29/04/19): play via sox does not work in the AT perception lab computers --------- ########
    toPlay = ' '.join(list(soundFiles))
    if tempo=='normal':
        listen = subprocess.Popen(['play {}'.format(toPlay)], shell=True)
        listen.wait()
    elif tempo=='slow':
        listen = subprocess.Popen(['play {} tempo 0.88'.format(toPlay)], shell=True)
        listen.wait()
    
# def play_sound_files(*soundObjs):
#     # plays sound file(s)
#     for s in soundObjs:
#         pygame.mixer.Sound.play(s)
#         while pygame.mixer.get_busy():
#             pass
    
def get_obj_click():
    # check for click on either object on prime/filler match trials
    clickPos = waitForClick((0.5*xc, 0.95*yc, boxW, boxH), (1.5*xc, 0.95*yc, boxW, boxH))
    return clickPos

# def get_speech_dur():
#     # get duration of participant's 'recording'
#     # returns time taken in ms
#     # use value to create a variable delay to simulate time taken
#     # for participant to click
#     clock = pygame.time.Clock()
#     t0 = pygame.time.get_ticks()
#     centreMouse()
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#         tt = pygame.time.get_ticks() - t0
# 
#         clickeMic = False
#         x,y = pygame.mouse.get_pos()
#         if pygame.mouse.get_pressed()[0]==1:
#             if (xc-60<x<xc+60 and yc-60<y<1.7*yc+60):
#                 clickedMic = True
#                 break
#     
#     return tt

def update_mic():
    # changes mic image from streaming to grey
    # displays instructions to wait for partner click
    pygame.mouse.set_visible(0)
    # (long and fugly but) gets rectangle of instructions text
    # textRect = pygame.font.SysFont('Arial', 24).render('Click on the mic when you finish speaking', 1, (0,0,0)).get_rect(center=(xc, 1.65*yc))
    # pygame.draw.rect(canvas, (255,255,255), (textRect))
    show_mic('streamBlank')
    show_mic('streamGrey')
    show_instructions('dir3')

def get_mic_click():
    # check for click on mic
    # update mic image (turns grey, show instruction text to wait)
    centreMouse()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        clicked = False
        x,y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]==1:
            if (xc-60<x<xc+60 and 1.45*yc-60<y<1.45*yc+60):
                clicked = 'mic'
                break
    
    return clicked

def create_rec_folder(subjNo):
    # create recording directory if it doesn't exist, returns path
    recsDirPath = '{}recs/sub{}/'.format(filePath, subjNo)
    if not os.path.exists(recsDirPath):
        os.makedirs(recsDirPath)
    else:
        print 'Oops, participant already exists. Try a different participant ID.'
        pygame.quit()
        sys.exit()
    
    return recsDirPath

def create_data_file(subjNo):
    # create data csv file for current ppt
    dataDirPath = '{}/data/'.format(filePath)
    if not os.path.exists(dataDirPath):
        os.makedirs(dataDirPath)
    dataFilePath = '{}/data/sub{}_data.csv'.format(filePath, subjNo)
    if not os.path.isfile(dataFilePath):
        with open(dataFilePath, 'wb') as f:
            writer = csv.writer(f)
            writer.writerow(['subjNo', 'trialNo', 'trialType', 'fillerType', 'condition', 'varDelay', 'targImg', 'distImg', 'targPos', 'distPos', 'clickPos'])
    else:
        print 'Oops, participant already exists! Try a different participant ID.'
        pygame.quit()
        sys.exit()
    return dataFilePath
        

def write_data_to_file(dataFile, dataToLog):
    # updates log csv with current trial info
    with open(dataFile, 'ab') as f:
        writer = csv.writer(f)
        writer.writerow(dataToLog)
        
def generate_varDelay(min, max):
    # generates a random variable delay between min and max
    # from a normal log distribution range of 5000 values
    theRange = np.logspace(math.log(min, 10), math.log(max, 10), 5000)
    varDelay = random.choice(theRange)
    return varDelay

def draw_sprite_to_screen(imgGroup, dur):
    # displays sprite image
    # imgGroup is object of LoadSprite class
    # dur is duration sprite should be shown for
    clock = pygame.time.Clock()
    t0 = pygame.time.get_ticks()

    while True:
        tt = pygame.time.get_ticks() - t0
        
        event = pygame.event.poll()

        imgGroup.update()
        imgGroup.draw(canvas)
        pygame.display.update()
        clock.tick(1)
        
        if tt > dur:
            break
        
def begin_screen():
    show_image(stimDict['begin'], 'C')
    pygame.display.update()
    waitForClick((xc, 1.8*yc, 110, 40), (xc, 1.8*yc, 110, 40))
        
def instructions_phase():
    instText = '''Welcome!\n\nIn this experiment, you and your partner will play a simple picture naming and matching game.\n\nYou will take turns to name pictures, and to match their descriptions to the correct picture on your screen.\n\nWhen it is your turn to describe, speak clearly into the microphone on the headphones you are wearing. Your partner will hear you through the one-way audio stream between the computers.\n\nAvoid saying "left" and "right" to refer to the pictures as the positions might be different for your partner.\n\nWhen it is your partner's turn to describe, listen carefully to them, then click on the picture that matches what they say.\n\nWhen you are ready, please let the experimenter know.'''
    
    clearCanvas()
    displayTextMultiline(instText, 28, (0.3*xc, 0.3*yc), (1.7*xc, 100))
    pygame.display.update()
    wait(500)
    play_sound_files('normal', audioDict['instructions'])
    waitForClick((50, 2*yc-50, 100, 100), (50, 2*yc-50, 100, 100))
    
    show_image(stimDict['connect'], 'C')
    waitForClick((xc, 1.8*yc, 110, 40), (xc, 1.8*yc, 110, 40))

def loading_phase():
    clearCanvas()
    pygame.mouse.set_visible(0)
    show_instructions('loading')
    loadingImage = LoadSprite('loading', 4, (xc-150, yc-150, 300, 300))
    loadingImageGroup = pygame.sprite.Group(loadingImage)
    
    draw_sprite_to_screen(loadingImageGroup, 3000)
    
def sound_check_phase():
    clearCanvas()
            
    show_instructions('loadingSuccess') 
    wait(3000)
    
    clearCanvas()
    
    show_instructions('soundCheck1')
    show_mic('stream')
    micArrow = LoadSprite('arrowR', 2, (0.6*xc, 1.35*yc, 200, 96))
    micArrowGroup = pygame.sprite.Group(micArrow)
    draw_sprite_to_screen(micArrowGroup, 8000)
    
    wait(1000)
    for i in range(2,5):
        show_instructions('soundCheck{}'.format(i))
    get_mic_click()
    update_mic()
    wait(3000, True)

    show_instructions('soundCheck5')
    wait(5000, True)
    
    show_instructions('match')
    show_image(stimDict['nochimney'], 'R')
    show_image(stimDict['chimney'], 'L')
    wait(2500)
    play_sound_files('normal', audioDict['soundCheck'])
    show_instructions('match2')
    
    get_obj_click()
    
    clearCanvas()
    wait(500)
    show_instructions('soundCheckFinish')
    wait(5000)
    
def end_screen():
    instText = '''You have reached the end of the experiment. You may now exit the booth.\n\n\nThank you very much for your participation.'''
    clearCanvas()
    displayTextMultiline(instText, 36, (0.3*xc, 0.6*yc), (1.7*xc, 100))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
    
class LoadSprite(pygame.sprite.Sprite):
    def __init__(self, imgName, numImgs, imagePos):
        super(LoadSprite, self).__init__()
        self.numImgs = numImgs      # number of images in sprite
        self.imgName = imgName
        self.imageFiles = [pygame.image.load('{}stims/{}{}.png'.format(filePath, self.imgName, i)) for i in range(1, numImgs+1)]
        self.images = []
        self.images.extend(self.imageFiles)

        self.index = 0
        self.image = self.images[self.index]
        self.rectL, self.rectT, self.rectW, self.rectH = imagePos[0], imagePos[1], imagePos[2], imagePos[3]
        self.rect = pygame.Rect(self.rectL, self.rectT, self.rectW, self.rectH)

    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0      # reset index to 0 if we're at the last image of our sprite
        self.image = self.images[self.index]

    
class Trial:
    
    def __init__(self, subjNo, trialNo, currentTrialInfo):
        currentTrialInfo = currentTrialInfo.strip().split(',')
        self.trialType = currentTrialInfo[1]
        self.fillerType = currentTrialInfo[2]
        self.criticalCondition = currentTrialInfo[3]
        self.targImg = currentTrialInfo[4]
        self.distImg = currentTrialInfo[5]
        self.targPos = currentTrialInfo[6]
        self.distPos = currentTrialInfo[7]
        self.subjNo = subjNo
        self.trialNo = trialNo
        
    def get_varDelay(self):
        ## uses generate_varDelay() to get varDelay duration depending on trialType and trialNo
        if self.trialType == 'prime':   # prime ppt match trials
            varDelay = 2000     # 2000 ms speech initiation latency on prime ppt match trials
        elif 'Match' in self.trialType:     # non-prime ppt match trials
            if self.trialNo < 20:
                if self.trialNo <= 5:
                    varDelay = generate_varDelay(3000, 3500)    # 3000-3500 ms speech initiation latency on non-prime match trials during first 5 trials
                else:
                    varDelay = generate_varDelay(2500, 3500)    # 2500-3500 ms speech initiation latency on non-prime match trials during trials 6-20
            else:
                varDelay = generate_varDelay(1800, 3000)    # 1800-3000 ms speech initiation latency on non-prime match trials post first 20 trials
        elif self.trialType == 'target':    # target ppt dir trials
            varDelay = 2000     # 2000 ms partner click time on target ppt dir trials
        elif 'Dir' in self.trialType:
            if self.trialType < 20:
                varDelay = generate_varDelay(2500, 3500)    # 2500-3500 ms partner click time on non-target dir trials during first 20 trials
            else:
                varDelay = generate_varDelay(1800,3000)     # 1800-3000 ms partner click time on non-target dir trials post first 20 trials
        
        return varDelay
        
    def draw_stim_to_screen(self):
        ## draws target img, dist img and boxes to screen
        clearCanvas()
        wait(200, True)
        show_image(stimDict[self.targImg], self.targPos)
        show_image(stimDict[self.distImg], self.distPos)
        show_box(stimDict['boxB'], self.targPos)
        show_box(stimDict['boxB'], self.distPos)
        if self.trialType == 'target' or 'Dir' in self.trialType:
            show_instructions('dir')
            show_arrow(self.targPos)
            show_mic('stream')
            show_instructions('dir2')
        elif self.trialType == 'prime' or 'Match' in self.trialType:
            show_instructions('match')
    
    def play_utterance(self, trialNo, varDelay):
        ## play audio recording for match trials
        if self.trialType == 'prime' or 'Match' in self.trialType:
            
            # if it's an m/f exp filler, select which version of utterance to use
            if 'exp' in self.fillerType:
                if self.trialNo < 30:
                    referentSoundFile = audioDict[self.targImg[0:4] + str(random.randint(1,2))]
                else:
                    referentSoundFile = audioDict[self.targImg[0:4] + str(random.randint(1,4))]
            else:
                referentSoundFile = audioDict[self.targImg]
            
            #simulate speech onset latency
            wait(varDelay, False)
            
            if trialNo == 1:
                # 'um, ok, click on the X'
                ## play_audio(audioDict['disfluency'][0])
                ## play_audio(audioDict['ok'])
                ## play_audio(audioDict['clickon'][random.randint(0,1)])
                play_sound_files('slow', audioDict['disfluency'][0], audioDict['ok'], audioDict['clickon'][random.randint(0,1)], referentSoundFile)
            elif trialNo == 3:
                # 'click on thee... uh, the X'
                ## play_audio(audioDict['clickonDisf'])
                play_sound_files('slow', audioDict['clickonDisf'], referentSoundFile)
            elif trialNo == 5:
                # 'click on the X'
                ## play_audio(audioDict['clickon'][random.randint(0,1)])
                play_sound_files('slow', audioDict['clickon'][random.randint(0,1)], referentSoundFile)
            elif trialNo == 7:
                # 'um, the X'
                ## play_audio(audioDict['disfluency'][0])
                play_sound_files('slow', audioDict['disfluency'][0], referentSoundFile)
            else:
                if 'filler' in self.trialType:
                    disfluent = random.randint(1,5)
                    if disfluent == 1:  # disfluency on 20% of filler trials (random nasal/nonnasal utterance-initial FP)
                        ## play_audio(audioDict['disfluency'][random.randint(0,1)])
                        play_sound_files('slow', audioDict['disfluency'][random.randint(0,1)], referentSoundFile)
                    else:
                        play_sound_files('slow', referentSoundFile)
                else:
                    play_sound_files('slow', referentSoundFile)
            # play_audio(audioDict[self.targImg])
            ## update canvas with click instructions
            wait(500, False)
            show_instructions('match2')
    
    def get_trial_click(self, recsDirPath, trialNo, varDelay):
        ## wait for click on each trial
        if self.trialType == 'target' or 'Dir' in self.trialType:
            ## for dir trials
            ## start recording, stop recording 250ms after mic click
            threading.Thread(target = record(recsDirPath, trialNo))
            resp = get_mic_click()
            if resp:
                wait(250)
                recording = False
                os.system('pkill sox')
            ## simulate partner click with a variable delay and instructions to wait
            update_mic()
            wait(varDelay, False)
        elif self.trialType == 'prime' or 'Match' in self.trialType:
            ## for match trials, get object clicked on (L or R)
            resp = get_obj_click()
        return resp
    
    def log_trial_data(self, dataFile, varDelay, resp):
        dataToLog = [self.subjNo, self.trialNo, self.trialType, self.fillerType, self.criticalCondition, round(varDelay,2), self.targImg, self.distImg, self.targPos, self.distPos, resp]
        write_data_to_file(dataFile, dataToLog)
        
def build_experiment(subjNo, gender):
    
    begin()
    
    recsDir = create_rec_folder(subjNo)
    dataFile = create_data_file(subjNo)
    stims = get_stim_spreadsheet(subjNo)
    
    stimDict = loadImages()
    audioDict = loadAudio('stimaudio_{}_scaled'.format(gender))
    
    begin_screen()
    # instructions_phase()
    # loading_phase()
    # sound_check_phase()
    
    for i in range(48):
        trialNo = i+1
        trial = Trial(subjNo, trialNo, stims[i])
        varDelay = trial.get_varDelay()
        trial.draw_stim_to_screen()
        trial.play_utterance(trialNo, varDelay)
        response = trial.get_trial_click(recsDir, trialNo, varDelay)
        trial.log_trial_data(dataFile, varDelay, response)
        
        print trialNo, stims[i], response
        print '\n'
        
    end_screen()
