#       PSC2DUNDEE Change the format of Potsdam Sentence Corpus (PSC) to a format similar to the Dundee corpus
# Usage: python psc2dundee.py <simulation_file> <cnt_file> <output_file> (e.g. python psc2dundee.py 'psc_data.csv' 'psc.cnt' 'dundee_output.txt') 
#   simulation_file is a csv of the PSC data
#   cnt_file        is a cnt file, containing word length information of words in each sentence
#   output_file     is a txt file where you save the dundee-like output
# Note: Before loading the psc data, I replaced NAs with -9999 to keep the column a numeral type of data
# by Yunyan Duan, 07/03/2016

import re, argparse, bisect, csv

parser = argparse.ArgumentParser(description='make dundee file from PSC.')
parser.add_argument('simulation_file', help = 'PSC data csv file')
parser.add_argument('cnt_file', help = 'cnt file')
parser.add_argument('output_file', help = 'give a name for the output file')
args = parser.parse_args()

class Fixation:
    def __init__(self):
        self.ppt = 'unknown'
        self.text = 'unknown'
        self.word = 'unknown'
        self.screennum = -1
        self.linenum = -1
        self.olen = -1
        self.wlen = -1
        self.xpos = -1
        self.wordnum = -1
        self.fdur = -1
        self.oblp = -1
        self.wdlp = -1
        self.laun = -99
    def pretty_print(self):
        return(' '.join([str(self.ppt), str(self.text),
                         str(self.word), str(self.screennum), str(self.linenum), 
                         str(self.olen), str(self.wlen), str(self.xpos), 
                         str(self.wordnum), str(self.fdur), str(self.oblp), 
                         str(self.wdlp), str(self.laun)]))

class SimFix:
    def __init__(self, line):
        self.id = int(line[0])
        self.sn = int(line[1])
        self.nw = int(line[2])
        self.wn = int(line[3])
        self.let = int(line[4])
        self.dur = int(line[5])
        self.ao = int(line[6])
        self.dir = int(line[7])
        self.l = int(line[8])
        self.f = float(line[9])
        self.p = float(line[10])
        self.x = int(line[11])
        self.wid = int(line[12])
        self.word = line[13]

# Step 1: Read data
## Data1: PSC simulation
filename = args.simulation_file
print filename

simfixes = []
with open(filename) as rf:
    psccsv = csv.reader(rf, delimiter=',')
    for i,line in enumerate(psccsv):
            if i > 0:
                fix = SimFix(line)
                simfixes.append(fix)

## Data2: corpus cnt file
cntname = args.cnt_file

sentcnts = []
with open(cntname) as rf:
    for line in rf:
        sentcnts.append([int(i) for i in line.split()])
 
# Step 2: Generate Dundee output
wf = open(args.output_file,'w')
wf.write("ppt text word screennum linenum olen wlen xpos wordnum fdur oblp wdlp laun\n")
count_error = 0

for i in range(len(simfixes)):
    sent = sentcnts[simfixes[i].sn]
    
    x = Fixation()
    x.ppt = simfixes[i].id
    x.text = simfixes[i].sn
    x.word = simfixes[i].word
    x.screennum = 1
    x.linenum = 1
    x.olen = simfixes[i].l
    x.wlen = simfixes[i].l
    x.xpos = sent[simfixes[i].wn + 2] + simfixes[i].let - 1*(simfixes[i].wn == 1) #simfixes[i].ao * simfixes[i].dir ######## in case you don't need the exact xpos... use the output amplitude instead 
    x.wordnum = simfixes[i].wn
    x.fdur = simfixes[i].dur
    x.oblp = simfixes[i].let
    x.wdlp = simfixes[i].let
    if i == 0 :
        x.laun = (-9999)*(-9999)
    else:
        x.laun = simfixes[i-1].ao * simfixes[i-1].dir *(-1)
    wf.write(x.pretty_print()+'\n')   
wf.close()
