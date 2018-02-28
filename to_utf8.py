#encoding=utf-8
import sys
fin = open(sys.argv[1], 'rb')
fou = open(sys.argv[2], 'wb')

for line in fin:
    newline = line.decode('GB18030').encode('utf-8')
    fou.write(newline)

fin.close()
fou.close()