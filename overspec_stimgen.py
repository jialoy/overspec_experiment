#!/usr/bin/env python

import random, itertools, csv, os

def random_with_remove(theList):
    # removes random element from list
    # returns removed element
    # list is modified
    choice = random.choice(theList)
    theList.remove(choice)
    return choice

def copy_and_shuffle(theList):
    # copy a list and random shuffle
    # returns new list
    theNewList = theList[:]
    random.shuffle(theNewList)
    return theNewList

def unique_shuffle_list(theList):
    # shuffles elements in a list with condition that no element can be
    # in the same position as its original position after the shuffle
    # returns new list of shuffled elements
    newList = list(theList)
    while True:
        random.shuffle(newList)
        for a, b in zip(theList, newList):
            if a == b:
                break
        else:
            return newList

def ordered_shuffle_list(theList, seedVal):
    # shuffles elements in a list to always return elements in a particular order based on seed value
    random.seed(seedVal)
    random.shuffle(theList)
    return theList

def merge_with_alternate(listA, listB):
    # returns new list where each element of list A
    # is separated by at least one element of list B
    # len(listA) must be < len(listB)
    # elements drawn randomly from each list when adding to new list
    listC = []
    for i in range(len(listA)):
        listC.append(random_with_remove(listB))
        listC.append(random_with_remove(listA))
    for i in range(len(listB)):
        listC.insert(random.randint(0, len(listC)), random_with_remove(listB))
    return(listC)

def get_distractor(currentImg, trialType):
    # generates distractor for prime image according to trial type (critical/filler animal/filler fruitveg/filler expressions)
    if trialType == 'critical':
        currentImgCol, currentImgNoun = currentImg.split('_')[1], currentImg.split('_')[0]
        distCol = random.choice([col for col in cols if col != currentImgCol])
        distNoun = random.choice([noun for noun in nouns if noun != currentImgNoun])
        dist = '_'.join([distNoun, distCol])
    elif trialType == 'fillerAni':
        dist = random.choice([x for x in anis if x != currentImg])
    elif trialType ==   'fillerFrv':
        dist = random.choice([x for x in frvs if x != currentImg])
    elif trialType == 'fillerExp':
        currentImgGdr = currentImg.split('_')[0]
        currentImgExp = currentImg.split('_')[1][0:2]
        distExp = random.choice([exp for exp in exps if exp != currentImgExp])
        dist = '{}_{}{}'.format(currentImgGdr, distExp, random.randint(1,4))
    elif trialType == 'fillerObjSC' or trialType == 'fillerObjSN':
        currentImgCol, currentImgNoun = currentImg.split('_')[1], currentImg.split('_')[0]
        if trialType == 'fillerObjSC':
            distCol = currentImgCol
            distNoun = random.choice([noun for noun in nouns if noun != currentImgNoun])
        elif trialType == 'fillerObjSN':
            distCol = random.choice([col for col in cols if col != currentImgCol])
            distNoun = currentImgNoun
        dist = '_'.join([distNoun, distCol])
    return dist

def shuffle_prime_target_refLists(primeRefList, targetRefList):
    # shuffles prime and target ref lists in the same order
    # (to ensure prime-target trial pairings stay the same in critical items)
    seedVal = random.randint(1,100)
    ordered_shuffle_list(primeRefList, seedVal)
    ordered_shuffle_list(targetRefList, seedVal)
    return [primeRefList, targetRefList]

def build_stimList(targImgList, trialType):
    # takes list of target images, generates distractor for each image
    # returns list of tuples of corresponding to targ/dist images for each trial
    stimList = []
    for targImg in targImgList:
        distImg = get_distractor(targImg, trialType)
        stimList.append((targImg, distImg))
    return stimList
    
def build_itemType_order():
    # generate list of item types in order to run
    # total no. of items = 112
    # critical items occur in sets of four trials (prime, cfillerDir, cfillerMatch, target)
    # filler items occur in sets of two trials (fillerMatch, fillerDir)
    # experiment has to begin with at least two filler items (i.e. four filler trials)
    # at least one filler item (i.e. two trials) has to seperate critical items
    criticalItems = ['critical']*32     # 32 critical items
    fillerItems = ['filler']*80     # 80 filler items
    
    itemTypeOrderList = []
    prevItem = None
    currentItem = None
    
    i1, i2 = [fillerItems.pop(fillerItems.index('filler')) for i in range(2)]     # make sure items 1 and 2 are fillers
    theRest = merge_with_alternate(criticalItems, fillerItems)
    itemTypeOrderList = [i1] + [i2] + theRest
    
    return itemTypeOrderList

def build_trialType_order(itemTypeOrderList):
    # generate list of trial types based on itemTypeOrderList where
    # each critical item comprises four trials: prime, cfillerDir, cfillerMatch, target
    # and each filler item comprises two trials: fillerMatch, fillerDir
    # cfiller trial types: animal/fruitveg/female exp/male exp
    # filler trial types: animal/fruitveg/female exp/male exp/object Same Colour/object Same Noun
    trialTypeList = ['prime']*32 + ['target']*32 + ['cfillerDir']*32 + ['cfillerMatch']*32 + ['fillerDir']*80 + ['fillerMatch']*80
    cfillerDirTrialTypeList = ['ani']*8 + ['frv']*8 + ['fexp']*8 + ['mexp']*8
    cfillerMatchTrialTypeList = ['ani']*8 + ['frv']*8 + ['fexp']*8 + ['mexp']*8
    fillerDirTrialTypeList = ['ani']*16 + ['frv']*16 + ['fexp']*16 + ['mexp']*16 + ['objSC']*8 + ['objSN']*8
    fillerMatchTrialTypeList = ['ani']*16 + ['frv']*16 + ['fexp']*16 + ['mexp']*16 + ['objSC']*8 + ['objSN']*8
    
    trialTypeOrderList = []     # prime/target/cfillerDir/cfillerMatch/fillerDir/fillerMatch
    fillerTrialTypeList = []
    
    for currentItem in itemTypeOrderList:
        if currentItem == 'critical':
            trialTypeOrderList.extend(['prime', 'cfillerDir', 'cfillerMatch', 'target'])
            fillerTrialTypeList.extend(['NA', cfillerDirTrialTypeList.pop(random.randrange(len(cfillerDirTrialTypeList))), cfillerMatchTrialTypeList.pop(random.randrange(len(cfillerMatchTrialTypeList))), 'NA'])
        elif currentItem == 'filler':
            trialTypeOrderList.extend(['fillerMatch', 'fillerDir'])
            fillerTrialTypeList.extend([fillerMatchTrialTypeList.pop(random.randrange(len(fillerMatchTrialTypeList))), fillerDirTrialTypeList.pop(random.randrange(len(fillerDirTrialTypeList)))])    

    return [trialTypeOrderList, fillerTrialTypeList]

def build_trialStimList(trialTypeOrderList, fillerTrialTypeList):
    # generate list of trial stims (target + distractor images) in order to run
    # trial types: prime, cfillerDir, cfillerMatch, target, fillerMatch, fillerDir
    # for cfillerDir and cfillerMatch, filler trial types: ani, frv, fexp, mexp
    # for fillerMatch and fillerDir, filler trial types: ani, frv, fexp, mexp, objSC, objSN
    criticalConditions = ['c1']*8 + ['c2']*8 + ['c3']*8 + ['c4']*8
    targLeft = ('L','R')
    targRight = ('R','L')
    c1PrimePosList, c2PrimePosList, c3PrimePosList, c4PrimePosList, c1TargetPosList, c2TargetPosList, c3TargetPosList, c4TargetPosList = [[targLeft]*4 + [targRight]*4 for i in range(8)]
    primePosLists = {'c1': c1PrimePosList, 'c2': c2PrimePosList, 'c3': c3PrimePosList, 'c4': c4PrimePosList}
    targetPosLists = {'c1': c1TargetPosList, 'c2': c2TargetPosList, 'c3': c3TargetPosList, 'c4': c4TargetPosList}
    fillerDirPosList, fillerMatchPosList = [[targLeft]*112 + [targRight]*112 for i in range(2)]

    currentItemType = None
    condition = None
    
    trialStimList = []
    for i in range(numTrials):
        trialType = trialTypeOrderList[i]
        if trialType == 'prime':
            #print trialType
            currentItemType = 'critical'    # set currentItemType to critical
            condition = criticalConditions.pop(random.randrange(len(criticalConditions)))
            images = primeTrialsDict[condition].pop(0)
            positions = primePosLists[condition].pop(random.randrange(len(primePosLists[condition])))
        elif trialType == 'target':
            #print trialType
            images = targetTrialsDict[condition].pop(0)
            positions = targetPosLists[condition].pop(random.randrange(len(targetPosLists[condition])))
        elif trialType == 'cfillerDir':
            cfillerTrialType = fillerTrialTypeList[i]
            #print cfillerTrialType
            images = cfillerDirTrialsDict[cfillerTrialType].pop(random.randrange(len(cfillerDirTrialsDict[cfillerTrialType])))
            positions = fillerDirPosList.pop(random.randrange(len(fillerDirPosList)))
        elif trialType == 'cfillerMatch':
            cfillerTrialType = fillerTrialTypeList[i]
            #print cfillerTrialType
            images = cfillerMatchTrialsDict[cfillerTrialType].pop(random.randrange(len(cfillerMatchTrialsDict[cfillerTrialType])))
            positions = fillerMatchPosList.pop(random.randrange(len(fillerMatchPosList)))
        elif trialType == 'fillerMatch':
            condition = 'NA'
            fillerTrialType = fillerTrialTypeList[i]
            #print fillerTrialType
            images = fillerMatchTrialsDict[fillerTrialType].pop(random.randrange(len(fillerMatchTrialsDict[fillerTrialType])))
            positions = fillerMatchPosList.pop(random.randrange(len(fillerMatchPosList)))
        elif trialType ==  'fillerDir':
            condition = 'NA'
            fillerTrialType = fillerTrialTypeList[i]
            #print fillerTrialType
            images = fillerDirTrialsDict[fillerTrialType].pop(random.randrange(len(fillerDirTrialsDict[fillerTrialType])))
            positions = fillerDirPosList.pop(random.randrange(len(fillerDirPosList)))
        targImg, distImg = images[0], images[1]
        targPos, distPos = positions[0], positions[1]
        
        trialStimList.append((condition, targImg, distImg, targPos, distPos))
    #print trialStimList
        
    return trialStimList

def generate_primeTarget_refLists(categoryCondition, colourCondition):
    # generate prime and target referent lists by condition
    # conditions: category (within/across) x colour (same/different)
    prime_gCols, prime_kCols = copy_and_shuffle(cols), copy_and_shuffle(cols)   # colours: x4 for clothes category, x4 for toys category
    prime_gNouns, prime_kNouns = copy_and_shuffle(gs), copy_and_shuffle(ks)     # nouns: clothes x4, toys x4
    
    primeRefList = ['_'.join(i) for i in zip(prime_gNouns, prime_gCols)] + ['_'.join(i) for i in zip(prime_kNouns, prime_kCols)]
    if categoryCondition == 'within':
        target_gNouns, target_kNouns = unique_shuffle_list(prime_gNouns), unique_shuffle_list(prime_kNouns)
        if colourCondition == 'same':
            target_gCols, target_kCols = prime_gCols[:], prime_kCols[:]
        elif colourCondition == 'diff':
            target_gCols, target_kCols = unique_shuffle_list(prime_gCols), unique_shuffle_list(prime_kCols)
    elif categoryCondition == 'across':
        target_gNouns, target_kNouns = prime_kNouns[:], prime_gNouns[:]     # just swap the categories
        if colourCondition == 'same':
            target_gCols, target_kCols = prime_gCols[:], prime_kCols[:]
        elif colourCondition == 'diff':
            target_gCols, target_kCols = unique_shuffle_list(prime_gCols), unique_shuffle_list(prime_kCols)
    targetRefList = ['_'.join(i) for i in zip(target_gNouns, target_gCols)] + ['_'.join(i) for i in zip(target_kNouns, target_kCols)]
    
    primeTargetRefLists = shuffle_prime_target_refLists(primeRefList, targetRefList)
    
    return primeTargetRefLists

def generate_fillerBare_refLists(fillerNounsList, fillerType):
    # generate dir and match referent lists for bare noun fillers (animals / fruitveg)
    # filler noun category: animal / fruitveg
    # filler type: critical (occurring within critical items) / filler
    # returns list of sublists corresponding to dir and match lists for noun category
    if fillerType == 'cfiller':
        dirRefList = random.sample(fillerNounsList, 8)
        matchRefList = [x for x in fillerNounsList if x not in dirRefList]
    elif fillerType == 'filler':
        dirRefList = fillerNounsList[:]
        matchRefList = fillerNounsList[:]
    
    return [dirRefList, matchRefList]

def generate_fillerExp_refLists(expsList):
    # generate dir and match referent lists for expression fillers
    # expsList: male or female expressions
    # returns list of sublists corresponding to
    # cfiller, filler, cfiller, filler lists
    refList = []
    for i in range(2):  # repeat for dir and match lists
        fillerExpsRefs = expsList[:]     # all 24 expressions of the gender
        random.shuffle(fillerExpsRefs)   # first shuffle to randomise order
        it = iter(fillerExpsRefs)
        sliced = [list(itertools.islice(it, 0, i)) for i in [8,16]]     # slice into chunks of 8 and 16 elements
        refList.extend(sliced)

    return refList

def generate_fillerObj_refLists():
    # generate dir and match referent lists for object fillers
    # returns list of sublists each containing 8 objects (4 gs, 4 ks)
    # for Same Colour Dir, Same Colour Match, Same Noun Dir, Same Noun Match lists
    objGs = ['_'.join((g,c)) for g in gs for c in cols]     # all 16 colour+noun combinations of clothing
    objKs = ['_'.join((k,c)) for k in ks for c in cols]     # all 16 colour+noun combinations of toys
    
    li1, li2, li3, li4 = [], [], [], []     # initialise empty lists to populate for SCDir, SCMatch, SNDir, SNMatch trials
    
    for li in [li1, li2, li3, li4]:
        # random pop 4 objects from each G/K list to fill lists 1-4
        li.extend([objGs.pop(random.randrange(len(objGs))) for x in range(4)] + [objKs.pop(random.randrange(len(objKs))) for x in range(4)])
    
    return [li1, li2, li3, li4]

def generate_stim_spreadsheet(subjNo):
    
    stimgensDir = 'stimgens/'
    if not os.path.exists(stimgensDir):
        os.makedirs(stimgensDir)
    
    fileName = '{}sub{}.csv'.format(stimgensDir, subjNo)
    
    with open(fileName, 'wb+') as f:
        writer = csv.writer(f)
        
        rowCount = 0
        numTrials = 288
        
        for row in range(numTrials):
            condition, targImg, distImg, targPos, distPos = trialStimList[rowCount][0], trialStimList[rowCount][1], trialStimList[rowCount][2], trialStimList[rowCount][3], trialStimList[rowCount][4]
            writer.writerow((subjNo, trialTypeOrderList[rowCount], fillerTrialTypeList[rowCount], condition, targImg, distImg, targPos, distPos))
            rowCount +=1
            
        f.close()

################################################
################################################
###### start generating some dicts #############
################################################
################################################


################################################
### critical prime + target trial stims ########
################################################

cols = ['c1', 'c2', 'c3', 'c4']

gs = ['g1', 'g2', 'g3', 'g4']
#ts = ['t1', 't2', 't3', 't4']
ks = ['k1', 'k2', 'k3', 'k4']
nouns = gs + ks

c1PrimeTargetRefs = generate_primeTarget_refLists('within', 'same')
c2PrimeTargetRefs = generate_primeTarget_refLists('within', 'diff')
c3PrimeTargetRefs = generate_primeTarget_refLists('across', 'same')
c4PrimeTargetRefs = generate_primeTarget_refLists('across', 'diff')

 
## build prime and target trial stim dicts
primeTrialsDict = {'c1': build_stimList(c1PrimeTargetRefs[0], 'critical'),
                   'c2': build_stimList(c2PrimeTargetRefs[0], 'critical'),
                   'c3': build_stimList(c3PrimeTargetRefs[0], 'critical'),
                   'c4': build_stimList(c4PrimeTargetRefs[0], 'critical')}

targetTrialsDict = {'c1': build_stimList(c1PrimeTargetRefs[1], 'critical'),
                    'c2': build_stimList(c2PrimeTargetRefs[1], 'critical'),
                    'c3': build_stimList(c3PrimeTargetRefs[1], 'critical'),
                    'c4': build_stimList(c4PrimeTargetRefs[1], 'critical')}

########################################################
### filler ani, frv, exp and obj trial stims ###########
########################################################

anis = ['ani{}'.format(i) for i in range(1,17)]
frvs = ['frv{}'.format(i) for i in range(1,17)]

fillerAniRefs = generate_fillerBare_refLists(anis, 'filler')
fillerFrvRefs = generate_fillerBare_refLists(frvs, 'filler')
cfillerAniRefs = generate_fillerBare_refLists(anis, 'cfiller')
cfillerFrvRefs = generate_fillerBare_refLists(frvs, 'cfiller')
    

exps = ['an', 'di', 'fr', 'ha', 'sa', 'su']

expsF, expsM = [], []     # empty lists for female/male facial expression image names
for exp in exps:
    # list of sublists where each sublist represents one expression
    expsF.extend(['f_{}{}'.format(exp, i) for i in range(1,5)])
    expsM.extend(['m_{}{}'.format(exp, i) for i in range(1,5)])

fillerExpFRefs = generate_fillerExp_refLists(expsF)
fillerExpMRefs = generate_fillerExp_refLists(expsM)

fillerObjRefs = generate_fillerObj_refLists()


cfillerDirTrialsDict = {'ani': build_stimList(cfillerAniRefs[0], 'fillerAni'),
                        'frv': build_stimList(cfillerFrvRefs[0], 'fillerFrv'),
                        'fexp': build_stimList(fillerExpFRefs[0], 'fillerExp'),
                        'mexp': build_stimList(fillerExpMRefs[0], 'fillerExp')}
cfillerMatchTrialsDict = {'ani': build_stimList(cfillerAniRefs[1], 'fillerAni'),
                          'frv': build_stimList(cfillerFrvRefs[1], 'fillerFrv'),
                          'fexp': build_stimList(fillerExpFRefs[2], 'fillerExp'),
                          'mexp': build_stimList(fillerExpMRefs[2], 'fillerExp')}
fillerDirTrialsDict = {'ani': build_stimList(fillerAniRefs[0], 'fillerAni'),
                       'frv': build_stimList(fillerFrvRefs[0], 'fillerFrv'),
                       'fexp': build_stimList(fillerExpFRefs[1], 'fillerExp'),
                       'mexp': build_stimList(fillerExpMRefs[1], 'fillerExp'),
                       'objSC': build_stimList(fillerObjRefs[0], 'fillerObjSC'),
                       'objSN': build_stimList(fillerObjRefs[1], 'fillerObjSN')}
fillerMatchTrialsDict = {'ani': build_stimList(fillerAniRefs[1], 'fillerAni'),
                         'frv': build_stimList(fillerFrvRefs[1], 'fillerFrv'),
                         'fexp': build_stimList(fillerExpFRefs[3], 'fillerExp'),
                         'mexp': build_stimList(fillerExpMRefs[3], 'fillerExp'),
                         'objSC': build_stimList(fillerObjRefs[2], 'fillerObjSC'),
                         'objSN': build_stimList(fillerObjRefs[3], 'fillerObjSN')}

# print primeTrialsDict
# print'\n'
# print targetTrialsDict
# print'\n'
# print '*********************'
# 
# print cfillerDirTrialsDict
# print '\n'
# print cfillerMatchTrialsDict
# print '\n'
# print fillerDirTrialsDict
# print '\n'
# print fillerMatchTrialsDict
# print '\n'
# print '*********************'

################################################
################################################
    
numTrials = 288
    
itemTypeOrderList = build_itemType_order()

trialTypeLists = build_trialType_order(itemTypeOrderList)
trialTypeOrderList, fillerTrialTypeList = trialTypeLists[0], trialTypeLists[1]

trialStimList = build_trialStimList(trialTypeOrderList, fillerTrialTypeList)
    
#for testing/debugging    
# subjNo = 1
#generate_stim_spreadsheet(subjNo)

