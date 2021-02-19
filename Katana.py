import random
import sys, getopt
import traceback

rmIndex = 0
removeAmount = 0
querySeq = []
tempListOne = []
tempListTwo = []


def findTE(indexListIndxOne, indexListIndxTwo, deletionPercent):
    global tempListOne
    global tempListTwo
    global removeAmount
    
    removeAmount = 0
    
    if deletionPercent != 0:
    
        tempListOne = indexListIndxOne
        tempListTwo = indexListIndxTwo
        
        temp = list(zip(tempListOne, tempListTwo))
        random.shuffle(temp)
        tempListOne, tempListTwo = zip(*temp)
        
        tempListOne = list(tempListOne)
        tempListTwo = list(tempListTwo)
        
        removeAmount = int(len(tempListOne)*deletionPercent)
        
        print("Removing " + str(removeAmount) + " Random Transposable Elements.")
        
        del tempListOne[removeAmount:]
        del tempListTwo[removeAmount:]
            
        temp = list(zip(tempListOne, tempListTwo))
        temp.sort(key=lambda x: x[0])
        tempListOne, tempListTwo = zip(*temp)
        
        tempListOne = list(tempListOne)
        tempListTwo = list(tempListTwo)
    else:
        removeAmount = 0 
    

def stripChromosome(queryNum, chromosome, indexListIndxOne, indexListIndxTwo, deletionPercent,chromosomeFile):
    global removeAmount
    
    listIndex = 0
    indexCounter = 0
    sideCounter = 0
    started = False
    
    file = open(chromosome[:-1] + "TE" + str(int(deletionPercent*100)) + "%.fasta", "w+")
    
    file.write(">" + chromosome[:-1] + " adjusted for " + str(int(deletionPercent*100)) + "% of Transposable Elements Removed.\n")
    
    print("Stripping Transposable Elements from Chromosome...")
    with open(chromosomeFile) as chromosometext:
        for line in chromosometext:
            
            if queryNum != 0:
                if line[0] == '>' and indexCounter != 0:
                    queryNum -= 1
                    indexCounter = 0
                    sideCounter = 0
                    
                indexCounter += 1
                continue
            
            if line[0] == '>':
                if started == True:
                    break                    
                else:
                    started = True
                    continue
            
            for char in line:
                
                if deletionPercent != 0:
                    if char == '\n':
                        continue
                    
                    indexCounter += 1
                    sideCounter += 1
                    
                    if indexCounter > 0:
                        if indexCounter == indexListIndxTwo[listIndex]:
                            if listIndex == (len(indexListIndxTwo) - 1):
                                continue
                            
                            listIndex += 1

                            if indexListIndxTwo[listIndex] <= indexListIndxTwo[listIndex - 1]:
                                listIndex += 1
                            
                        if indexCounter >= indexListIndxOne[listIndex] and indexCounter <= indexListIndxTwo[listIndex]:
                            file.write("")
                            sideCounter -= 1
                            
                        else:
                            file.write(char)
                            
                else:
                    
                    if char == '\n':
                        continue
        
                    indexCounter += 1
                    sideCounter += 1
                    
                    if indexCounter >= 1:
                        file.write(char)
                        
    file.close()
    
    print("Originally " + str(indexCounter) + " Base Pairs.")
    print("Now " + str(sideCounter) + " Base Pairs after " + str(removeAmount) + " Random Transposable Elements Removed.")
    print("Adjusted Chromosome written to: " + chromosome[:-1] + "TE" + str(int(deletionPercent*100)) + "%.fasta")
    
# Execution
def main(argv):
    repeatMaskerFile = ''
    chromosomeFile = ''
    querySeq = ''
    rmIndex = 0
    
    try:
        opts, args = getopt.getopt(argv, "hf:c:n:q:", ["rfile=","cfile=", "qSeq="])
    except getopt.GetoptError:
        print('katana.py -f <repeatMaskerFile> -c <ChromosomeFile> -n <Chromosome Count to be Spliced> -q <Chromosome queries>')
        sys.exit(2)
       
        # parse RepeatMasker
    for opt, arg in opts:
        
        if opt == '-h':
            print('katana.py -f <repeatMaskerFile> -c <ChromosomeFile> -n <Chromosome Count to be Spliced> -q <Chromosome queries>')
            sys.exit()
            
        elif opt in ("-f", "--rfile"):
            repeatMaskerFile = arg
            
        elif opt in ("-c", "--cfile"):
            chromosomeFile = arg
            
        elif opt in ("-q", "--qSeq"):
            querySeq = arg
            querySeq = querySeq.split("-")
            
    try:
        queryNum = 0
        for chromosome in querySeq:
            
            chromosome += " "
            rmIndex = 0
            indexListIndxOne = []
            indexListIndxTwo = []
            
            with open(repeatMaskerFile) as fastatext:
                print("Parsing " + chromosome[:-1] + " for Transposable Elements from " + repeatMaskerFile)
                for line in fastatext:
                        
                    if line.find(chromosome) != -1:
                        rmIndex += 1
                        values = line.split()
                        indexListIndxOne.append(int(values[5]))
                        indexListIndxTwo.append(int(values[6]))
                
            # strip Chromosomes of TEs
            findTE(indexListIndxOne, indexListIndxTwo, 0.1)
            stripChromosome(queryNum, chromosome, tempListOne, tempListTwo, 0.1, chromosomeFile)
            
            queryNum += 1
            
    except:
        print("Error Detected. Exiting...")
        traceback.print_exc()
        exit()
        
if __name__ == "__main__":
    main(sys.argv[1:])