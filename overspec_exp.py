#!/usr/bin/env python

import pygame, random, sys, math, subprocess, threading, os, csv
import numpy as np
from pygame.locals import *
from overspec_stimgen import cols, gs, ks, nouns, anis, frvs, exps, numTrials

filePath = '/Users/jia/Desktop/overspec/'   # to change
imgW, imgH = 400, 400
boxW, boxH = 436, 436

def begin():
    
    global canvas, xc, yc, imagePositions, boxPositions
    
    pygame.init()
    pygame.mixer.init(44100, -16, 2, 2048)
    
    scrRes = pygame.display.Info()
    scrWidth = scrRes.current_w
    scrHeight = scrRes.current_h
    xc = scrWidth/2
    yc = scrHeight/2
    mousePos = [xc, yc]
    imagePositions = {'L': (0.5*xc-imgW/2, yc-imgH/2), 'R': (1.5*xc-imgW/2, yc-imgH/2)}
    boxPositions = {'L': (0.5*xc-boxW/2, yc-boxH/2), 'R': (1.5*xc-boxW/2, yc-boxH/2)}
    
    canvas = pygame.display.set_mode((scrWidth, scrHeight), 0, 32)
    canvas.fill((255, 255, 255))
    
def changeScreen(col):
    # for debugging
    cols = {'o': (255,237,192), 'w':(255,255,255), 'g':(233,255,226)}
    canvas.fill(cols[col])
    pygame.display.update()
    
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
    miscImages = ['boxB', 'boxTarg', 'mic', 'micRed', 'micBlank', 'bike', 'chimney']
    #stimDict[miscImages[i]] = [pygame.image.load('{}overspec/stims/{}.png'.format(filePath, miscImages[i])) for i in range(len(miscImages))]
    stimDict['boxB'] = pygame.image.load('{}stims/box_b.png'.format(filePath))
    stimDict['boxTarg'] = pygame.image.load('{}stims/box_targ.png'.format(filePath))
    # stimDict['mic'] = pygame.image.load('{}overspec/stims/mic_black.png'.format(filePath))
    # stimDict['micRed'] = pygame.image.load('{}overspec/stims/mic_red.png'.format(filePath))
    # stimDict['micGrey'] = pygame.image.load('{}overspec/stims/mic_grey.png'.format(filePath))
    # stimDict['micBlank'] = pygame.image.load('{}overspec/stims/mic_blank.png'.format(filePath))
    stimDict['stream'] = pygame.image.load('{}stims/stream.png'.format(filePath))
    stimDict['streamGrey'] = pygame.image.load('{}stims/stream_grey.png'.format(filePath))
    stimDict['streamBlank'] = pygame.image.load('{}stims/stream_blank.png'.format(filePath))
    stimDict['bike'] = pygame.image.load('{}stims/bike.png'.format(filePath))
    stimDict['chimney'] = pygame.image.load('{}stims/chimney.png'.format(filePath))
    return stimDict

def loadAudio(audioDir):
    # pre-load sound files
    # returns X
    global audioDict
    audioDict = {}
    for n in range(len(nouns)):
        for c in range(len(cols)):
            fileName = '_'.join([nouns[n],cols[c]])
            audioDict[fileName] = pygame.mixer.Sound('{}{}/{}.wav'.format(filePath, audioDir, fileName))
    for a in anis:
        audioDict[a] = pygame.mixer.Sound('{}{}/filler_audio/animals/{}.wav'.format(filePath, audioDir, a))
    for f in frvs:
        audioDict[f] = pygame.mixer.Sound('{}{}/filler_audio/fruitveg/{}.wav'.format(filePath, audioDir, f))
    for gdr in ['f', 'm']:
        for exp in exps:
            for i in range(1,5):
                audioDict['{}_{}{}'.format(gdr, exp, i)] = pygame.mixer.Sound('{0}{1}/filler_audio/{2}/{3}/{2}_{3}{4}.wav'.format(filePath, audioDir, gdr, exp, i))
    audioDict['disfluency'] = [pygame.mixer.Sound('{}{}/disfluency.wav'.format(filePath, audioDir)), pygame.mixer.Sound('{}overspec/{}/disfluency2.wav'.format(filePath, audioDir))]
    audioDict['ok'] = pygame.mixer.Sound('{}{}/ok.wav'.format(filePath, audioDir))
    audioDict['clickon'] = [pygame.mixer.Sound('{}{}/clickon.wav'.format(filePath, audioDir)), pygame.mixer.Sound('{}{}/clickon2.wav'.format(filePath, audioDir))]
    audioDict['clickonDisf'] = pygame.mixer.Sound('{}{}/clickondisf.wav'.format(filePath, audioDir))
    audioDict['soundCheck'] = pygame.mixer.Sound('{}{}/soundcheck.wav'.format(filePath, audioDir))
    return audioDict

def record(recsDirPath, trialNo):
    rec = subprocess.Popen(['sox -d -c 1 -b 16 -r 44100 {}/trial{}.wav'.format(recsDirPath, trialNo)], shell=True)
    
def displayText(text, fontSize, xyCoords, colour=(0,0,0)):
    # displays text string centred on xyCoords
    font = pygame.font.SysFont('Arial', fontSize)
    text = font.render(text, 1, colour)
    text_rect = text.get_rect(center=(xyCoords))
    canvas.blit(text, text_rect)
    return text_rect

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
    # optional: clears canvas
    # waits for a specified duration (ms)
    if clear==True:
        clearCanvas()
    t0 = pygame.time.get_ticks()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(), pygame.quit()
        tE = pygame.time.get_ticks() - t0
        pygame.display.update()
        if tE > timeInMs:
            break
        
def get_stim_spreadsheet(subjNo):
    # reads in stim spreadsheet generated by overspec_stimgen module
    # returns list of strings with each string corresponding to trial stim
    stimFileName = 'sub{}.csv'.format(subjNo)
    
    with open('{0}stimgens/{1}'.format(filePath, stimFileName), 'rb') as f:
        stimDF = f.readlines()
        
        return stimDF

def show_instructions(trialTask):
    instDict = {'loading': ['Please wait while your partner connects to the network', 0.3*yc],
                'loadingSuccess': ['Ok! Now let\'s check the audio streaming.', yc],
                'soundCheck': ['Follow your partner\'s instructions', 0.3*yc],
                'soundCheck2': ['Great! Now send following instruction to your partner.', 0.3*yc],
                'soundCheck3': ['Click on the mic when you finish speaking', 1.7*yc],
                'soundCheck4': ['"Please click on the XXX."', 0.8*yc],
                'soundCheckFinish': ['Ok that\'s fine! The experiment will now begin.', yc],
                'match': ['Listen to your partner\'s description', 0.15*yc],
                'match2': ['Now click on the picture your partner described', 0.3*yc],
                'dir': ['Describe the picture highlighted in green to your partner', 0.3*yc],
                'dir2': ['Click on the mic when you finish speaking', 1.7*yc],
                'dir3': ['Wait while your partner clicks on a picture', 1.7*yc]}
    displayText(instDict[trialTask][0], 24, (xc, instDict[trialTask][1]))
    pygame.display.update()

def show_image(objName, pos):
    canvas.blit(objName, imagePositions[pos])
    pygame.display.update()

def show_box(box, boxPos):
    canvas.blit(box, boxPositions[boxPos])
    pygame.display.update()
    
def show_mic(micImage):
    canvas.blit(stimDict[micImage], (xc-60, 1.5*yc-60))
    pygame.display.update()

def play_audio(objName):
    pygame.mixer.Sound.play(objName)
    while pygame.mixer.get_busy():
        pass
    
def get_obj_click():
    # check for click on either object on prime/filler match trials
    clickPos = waitForClick((0.5*xc, yc, boxW, boxH), (1.5*xc, yc, boxW, boxH))
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
    pygame.mouse.set_visible(0)
    # (long and fugly but) gets rectangle of instructions text
    textRect = pygame.font.SysFont('Arial', 24).render('Click on the mic when you finish speaking', 1, (0,0,0)).get_rect(center=(xc, 1.7*yc))
    pygame.draw.rect(canvas, (255,255,255), (textRect))
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
            if (xc-60<x<xc+60 and yc-60<y<1.7*yc+60):
                clicked = 'mic'
                break
    
    return clicked

def create_rec_folder(subjNo):
    # create recording directory if it doesn't exist, returns path
    recsDirPath = '{}recs/sub{}/'.format(filePath, subjNo)
    if not os.path.exists(recsDirPath):
        os.makedirs(recsDirPath)
    
    return recsDirPath

def create_data_file(subjNo):
    # create data csv file for current ppt
    dataDirPath = '{}/data/'.format(filePath)
    if not os.path.exists(dataDirPath):
        os.makedirs(dataDirPath)
    dataFilePath = '{}/sub{}_data.csv'.format(dataDirPath, subjNo)
    with open(dataFilePath, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(['subjNo', 'trialNo', 'trialType', 'fillerType', 'condition', 'targImg', 'distImg', 'targPos', 'distPos', 'clickPos'])
    return dataFilePath
        

def write_data_to_file(dataFile, dataToLog):
    with open(dataFile, 'ab') as f:
        writer = csv.writer(f)
        writer.writerow(dataToLog)
        
def generate_varDelay(min, max):
    # generates a random variable delay between min and max
    # from a normal log distribution range of 5000 values
    theRange = np.logspace(math.log(min, 10), math.log(max, 10), 5000)
    varDelay = random.choice(theRange)
    return varDelay

def loading_screen():
    pygame.mouse.set_visible(0)
    show_instructions('loading')
    loadingImage = LoadSprite()
    loadingImageGroup = pygame.sprite.Group(loadingImage)
    
    clock = pygame.time.Clock()
    t0 = pygame.time.get_ticks()
    
    while True:
        tt = pygame.time.get_ticks() - t0
        
        event = pygame.event.poll()

        loadingImageGroup.update()
        loadingImageGroup.draw(canvas)
        pygame.display.update()
        clock.tick(1)
        
        if tt > 2000:
            break
    
def sound_check_phase():
    clearCanvas()
            
    show_instructions('loadingSuccess') 
    wait(3000)
    
    clearCanvas()
    
    show_instructions('soundCheck')
    show_image(stimDict['bike'], 'R')
    show_image(stimDict['chimney'], 'L')
    wait(2500)
    play_audio(audioDict['soundCheck'])
    
    get_obj_click()
    
    clearCanvas()
    
    for i in range(2,5):
        show_instructions('soundCheck{}'.format(i))
    show_mic('stream')
    get_mic_click()
    update_mic()
    wait(2000, False)
    
    clearCanvas()
    show_instructions('soundCheckFinish')
    wait(2000)
    
class LoadSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(LoadSprite, self).__init__()
        self.images = []
        self.images.extend([pygame.image.load('{}stims/loading{}.png'.format(filePath, i)) for i in range(1,5)])

        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(xc-150, yc-150, 300, 300)

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
        
    def draw_stim_to_screen(self):
        
        clearCanvas()
        wait(200, True)
        show_image(stimDict[self.targImg], self.targPos)
        show_image(stimDict[self.distImg], self.distPos)
        show_box(stimDict['boxB'], self.targPos)
        show_box(stimDict['boxB'], self.distPos)
        if self.trialType == 'target' or 'Dir' in self.trialType:
            show_instructions('dir')
            show_box(stimDict['boxTarg'], self.targPos)
            show_mic('stream')
            show_instructions('dir2')
        elif self.trialType == 'prime' or 'Match' in self.trialType:
            show_instructions('match')
    
    def play_utterance(self, trialNo):
        ## play audio recording for match trials
        if self.trialType == 'prime' or 'Match' in self.trialType:
            # simulate speech onset latency
            if self.trialType == 'prime':
                varDelay = 2000
            else:
                varDelay = generate_varDelay(1500, 3000)
            wait(varDelay, False)
            
            if trialNo == 1:
                # 'um, ok, click on the X'
                play_audio(audioDict['disfluency'][0])
                play_audio(audioDict['ok'])
                play_audio(audioDict['clickon'][random.randint(0,1)])
            elif trialNo == 3:
                # 'click on thee... uh, the X'
                play_audio(audioDict['clickonDisf'])
            elif trialNo == 5:
                # 'click on the X'
                play_audio(audioDict['clickon'][random.randint(0,1)])
            elif trialNo == 7:
                # 'um, the X'
                play_audio(audioDict['disfluency'][0])
            else:
                if 'filler' in self.trialType:
                    disfluent = random.randint(1,5)
                    if disfluent == 1:  # disfluency on 20% of filler trials (random nasal/nonnasal utterance-initial FP)
                        play_audio(audioDict['disfluency'][random.randint(0,1)])
            play_audio(audioDict[self.targImg])
            ## update canvas with click instructions
            wait(500, False)
            show_instructions('match2')
    
    def get_trial_click(self, recsDirPath, trialNo):
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
            if self.trialType == 'target':
                varDelay = 1500
            else:
                varDelay = generate_varDelay(1500,3000)
            update_mic()
            wait(varDelay, False)
        elif self.trialType == 'prime' or 'Match' in self.trialType:
            ## for match trials, get object clicked on (L or R)
            resp = get_obj_click()
        return resp
    
    def log_trial_data(self, dataFile, resp):
        dataToLog = [self.subjNo, self.trialNo, self.trialType, self.fillerType, self.criticalCondition, self.targImg, self.distImg, self.targPos, self.distPos, resp]
        write_data_to_file(dataFile, dataToLog)
        
def build_experiment(subjNo):
    
    begin()
    
    recsDir = create_rec_folder(subjNo)
    dataFile = create_data_file(subjNo)
    stims = get_stim_spreadsheet(subjNo)
    
    stimDict = loadImages()
    audioDict = loadAudio('stimaudio_f_scaled')
    
    loading_screen()
    
    sound_check_phase()

    for i in range(numTrials):
        trialNo = i+1
        trial = Trial(subjNo, trialNo, stims[i])
        trial.draw_stim_to_screen()
        trial.play_utterance(trialNo)
        response = trial.get_trial_click(recsDir, trialNo)
        trial.log_trial_data(dataFile, response)
        
        print stims[i], response
