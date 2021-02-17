import random
import sys, getopt
import traceback

querySeq = "chr21 "
chromosomeFile = ""
rmIndex = 0
removeAmount = 0
indexListIndxOne = []
indexListIndxTwo = []
tempListOne = []
tempListTwo = []

def findTE(indexListIndxOne, indexListIndxTwo, deletionPercent):
    global tempListOne
    global tempListTwo
    global removeAmount
    
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
    

def stripChromosome(indexListIndxOne, indexListIndxTwo, deletionPercent):
    global removeAmount
    global querySeq
    global chromosomeFile
    
    listIndex = 0
    indexCounter = -5
    sideCounter = -5
    lineTrigger = 0
    
    file = open(querySeq[:-1] + "TE" + str(int(deletionPercent*100)) + "%.fasta", "w+")
    
    file.write(">" + querySeq[:-1] + " adjusted for " + str(int(deletionPercent*100)) + "% of Transposable Elements Removed.\n")

    print("Stripping Transposable Elements from Chromosome...")
    with open(chromosomeFile) as chromosometext:
        for line in chromosometext:
            
            if lineTrigger == 0:
                lineTrigger = 1
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

    print("Originally " + str(indexCounter) + " Base Pairs.")
    print("Now " + str(sideCounter) + " Base Pairs after " + str(removeAmount) + " Random Transposable Elements Removed.")
    print("Adjusted Chromosome written to: " + querySeq[:-1] + "TE" + str(int(deletionPercent*100)) + "%.fasta")
    
# Execution
def main(argv):
    global rmIndex
    global querySeq
    global chromosomeFile
    
    repeatMaskerFile = ''
    chromosomeFile = ''
    querySeq = ''
    
    try:
        opts, args = getopt.getopt(argv, "hf:c:q:", ["rfile=","cfile=","qSeq="])
    except getopt.GetoptError:
        print('katana.py -f <repeatMaskerFile> -c <ChromosomeFile> -q <Chromosome query>')
        sys.exit(2)
       
        # parse RepeatMasker
    for opt, arg in opts:
        
        if opt == '-h':
            print('katana.py -f <repeatMaskerFile> -c <ChromosomeFile> -q <Chromsome query>')
            sys.exit()
            
        elif opt in ("-f", "--rfile"):
            repeatMaskerFile = arg
            
        elif opt in ("-c", "--cfile"):
            chromosomeFile = arg
            
        elif opt in ("-q", "--qSeq"):
            querySeq = arg
            querySeq += " "
            print(querySeq)
    
    try:
        print("Parsing " + querySeq + "for Transposable Elements from " + repeatMaskerFile)

        with open(repeatMaskerFile) as fastatext:
            for line in fastatext:
                
                if line.find(querySeq) != -1:
                    rmIndex += 1
                    values = line.split()
                    indexListIndxOne.append(int(values[5]))
                    indexListIndxTwo.append(int(values[6]))
            
        # parse Chromosome
        #findTE(indexListIndxOne, indexListIndxTwo, 0.8)
        #stripChromosome(tempListOne, tempListTwo, 0.8)        
        #findTE(indexListIndxOne, indexListIndxTwo, 0.4)
        #stripChromosome(tempListOne, tempListTwo, 0.4)
        findTE(indexListIndxOne, indexListIndxTwo, 0.1)
        stripChromosome(tempListOne, tempListTwo, 0.1)
            
    except:
        print("Error Detected. Exiting...")
        traceback.print_exc()
        exit()
        
if __name__ == "__main__":
    main(sys.argv[1:])