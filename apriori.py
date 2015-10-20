"""
Description : Python implementation of Apriori Algorithm
Usage $python main.py -f [filename] -s [minSupport] -c [minConfidence]

Note to readers : my data structure is a list contains sets contains lists inside the sets 
The reason I choose to implement in this way is because I can use the union method of the sets
The way I count the frequency is by going back to the original list and count them all again
"""

from collections import Counter
from optparse import OptionParser 

globNumberOfTransactions = 0.0
globOriginalList = None
globMinSup = 0
globMinConf = 0

def readFile(filename):
    """ 
    Function read the file 
    return a list of sets which contains the information of the transaction
    """
    originalList = list()
    file = open(filename, 'rU')
    c = 0
    for line in file:
        c = c+1
        line = line.strip().rstrip(',')
        record = set(line.split(', '))
        originalList.append(record)
    global globNumberOfTransactions 
    globNumberOfTransactions = c
    global globOriginalList
    globOriginalList = originalList
    #print(globNumberOfTransactions)

def getSizeOneItemSet(originalList):
    """this Function generate all the size 1-itemset candidate"""
    Cone = list()
    for s in originalList:
        for e in s:
            Cone.append(e)       
    return sorted(Cone)

def pruneForSizeOne(objectList):
    """this function take in a candidate itemset and filter by support """
    """ K is the result frequent itemset for its size"""
    kDict = dict()
    kList = list()
    a = Counter(objectList)
    for e in a:
        if((a[e]/ float(globNumberOfTransactions)) >= globMinSup):
            kDict.update({e:a[e]})
            c = set([e])
            kList.append(c)
    return kList

def getSizePlueOneItemSet(Klist): 
    """ my way of this doing is super lazy, I just union it and check for size
        and I put the result itemset into the list 
        at the end of the function, I check for its minsup"""
    candidate = list()
    for e in Klist:
        for f in Klist:
            a = e.union(f)
            if len(a) == len(e)+1:
                candidate.append(a)
    #print(candidate)
    #print(len(candidate))
    newlist = []
    for i in candidate:
        if i not in newlist:
            newlist.append(i)
    candidate = newlist
    #print(candidate)
    """ here is the normal pruning process """
    newlist = []
    for e in candidate:
        counter = 0
        for f in globOriginalList:
            if(f.issuperset(e)):
                counter = counter+ 1
        if((counter/float(globNumberOfTransactions)) >= globMinSup):
            newlist.append(e)
    #print(len(candidate))
    return newlist

def apriori(fName):
    candidateList = list()   
    allfrequentitemSet = list()
    readFile(fName)
    Cone = getSizeOneItemSet(globOriginalList)
    candidateList = pruneForSizeOne(Cone)
    for e in candidateList:
        allfrequentitemSet.append(e)
    #print(candidateList)
    while(candidateList !=[]):
        candidateList = getSizePlueOneItemSet(candidateList)
        #print(candidateList)
        for e in candidateList:
             allfrequentitemSet.append(e)
    print("frequent itemsets")          
    print(allfrequentitemSet)
    print("________________________________")
    
    """ generate all the association rule"""
    for e in allfrequentitemSet:
        for f in allfrequentitemSet:
            if(f.issuperset(e) & (f!=e)):
                associate(e,f)
    
                        
def associate(e,f):
    """ this function check the association rule between two sets"""
    counter1 = 0
    counter2 = 0
    for g in globOriginalList:
        if(g.issuperset(e)):
            counter1+=1
        if(g.issuperset(f)):
            counter2+=1
    conf = float(counter2)/counter1 
    if(conf >= globMinConf):
        print(e),
        print(':'),
        print(counter1/float(globNumberOfTransactions)), 
        print("==>"),
        print(f),
        print(':'),
        print(counter2/float(globNumberOfTransactions)),
        print("conf:"),
        print(conf)
        
if __name__ == "__main__":
    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile',
                          dest = 'inputFile',
                          help = 'data file',
                          default = "data/adult.data")
    optparser.add_option('-s','--minSupport',
                          dest = 'minSup',
                          help = 'Minimum Support',
                          default = 0.3,
                          type ='float')
    optparser.add_option('-c','--minConfidence',
                          dest = 'minConf',
                          help = 'Minimum Confidence',
                          default = 0.6,
                          type ='float')   
    (options, args) = optparser.parse_args()
    
    fName = None
    if options.inputFile is None:
            fName = "240P1/adult.data"
    elif options.inputFile is not None:
            fName = options.inputFile
    
    globMinSup = options.minSup
    globMinConf = options.minConf
    #print(fName,globMinSup,globMinConf)
    apriori(fName)
