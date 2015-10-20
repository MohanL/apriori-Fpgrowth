"""
Description : Python implementation of FpGrowth Algorithm
Usage $python main.py -f [filename] -s [minSupport] -c [minConfidence]
"""
from treelib import Node, Tree
from collections import Counter
import operator
from optparse import OptionParser 

globNumberOfTransactions = 0.0
globOriginalList = None
globMinSup = 0
globMinConf = 0

def readFile(filename):
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
    #print(globOriginalList)

def getSizeOneItemSet(originalList):
    Cone = list()
    for s in originalList:
        for e in s:
            Cone.append(e)       
    return sorted(Cone)

def priorityDic(objectList):
    kDict = Counter(objectList)
    return kDict

def FpGrowth(fName):
    
    readFile(fName)
    Cone = getSizeOneItemSet(globOriginalList)
    priorityDict = priorityDic(Cone)
    #print(priorityDict)
    tree = Tree()   
    tree.create_node("{}", "root")
    #reconstruct the whole transction database based on the priority
    counter = 0
    for set in globOriginalList:
        temp = dict()
        for element in set:
            priority = priorityDict.get(element)
            temp.update({element:priority})
            sorted_temp = sorted(temp.items(), key=operator.itemgetter(1))
            sorted_temp.reverse()
        #print(sorted_temp)
        # construct Fp tree
        root = "root"
        for tuple in sorted_temp:
            if(not tree.contains(tuple[0])):
                tree.create_node(tuple[0], tuple[0], root, 0)
                root = tuple[0]
            else: 
                if tuple[0] in tree.is_branch(root):
                    #print("node already in this branch, don't know what to do")
                    #print("going down")
                    root = tuple[0]
                    #print(root)
                else:
                    #print("should create a duplicate node")
                    tree.create_node(tuple[0], counter, root, 0)
                    root = counter
                    counter += 1
                # I need to decide whether to create a new node or not
                # the condition is under this branch if this node exist
                # so I should check the root
    tree.show()
        
if __name__ == "__main__":
    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile',
                          dest = 'inputFile',
                          help = 'data file',
                          default = "data/test.txt")
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
    FpGrowth(fName)
