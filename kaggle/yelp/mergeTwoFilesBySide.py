import sys

def mergeFile(file1Name, file2Name, fileOpName, sep=','):
    with open(file1Name, 'r') as file1, open(file2Name, 'r') as file2,\
            open(fileOpName, 'w') as opFile:
        for line1 in file1:
            cols1 = line1.strip().split(',')
            end = cols1[-1]
            line2 = file2.readline().strip()
            opFile.write(','.join(cols1[0:-1]) + sep + line2 + sep \
                             + cols1[-1] + '\n')


def main():
    if len(sys.argv) > 3:
        file1Name = sys.argv[1]
        file2Name = sys.argv[2]
        opFileName = sys.argv[3]
        sep = ','
        if len(sys.argv) > 4:
            sep =  sys.argv[4]
        mergeFile(file1Name, file2Name, opFileName, sep)
    else:
        print 'invalid args'

        
if __name__ == '__main__':
    main()
            
