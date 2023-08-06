#!/usr/bin/python

""" 
Copyright (c) 2016 King Mongkut's University technology Thonburi
Author: Nattawet Sriwichai
Contact: nattawet.sri@mail.kmutt.ac.th
Version: 1.3b 2017-03-01
License: MIT License

The MIT License

Copyright (c) 2016 King Mongkut's University technology Thonburi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE. 
"""
version = "GenomeManagement_v1.3b"

import re
import gzip
import codecs
from operator import itemgetter, attrgetter

utf8 = codecs.getreader('UTF-8')


class Fasta_manager(object):
	def __init__(self, fastaFile, show_genome_stat=False):
		self.chromosomeLength = {}
		self.chromosomeSeq = {}
		self.chromosomeStatistics = {}  # Length, GC, AT, N
		count_bases = {'A': 0, 'T':0, 'C':0, 'G':0, 
										'R':0, 'S':0, 'W':0, 'K':0, 
										'M':0, 'B':0, 'D':0, 'H':0, 
										'V':0, 'Y':0, 'N': 0
		}
		
		if(fastaFile.find('.gz') > 0):
			filegz = gzip.open(fastaFile, 'rb')
			self.file = utf8(filegz)
		else:
			self.file = open(fastaFile, 'r')
		fasta = self.file.read().split('>')
		fasta = fasta[1:]
		for chromosome in fasta:
			if (chromosome[:50].find(' ') < 0):
				header = chromosome[:chromosome[:50].find('\n')]
			else:
				header = chromosome[:chromosome[:50].find(' ')]
			sequence = chromosome[chromosome.find('\n'):-1].replace('\n', '')
			
			length = len(sequence)
			self.chromosomeSeq[header] = sequence
			self.chromosomeLength[header] = length

			if show_genome_stat:
				for i in sequence:
					i = i.upper()
					count_bases[i] += 1

		if show_genome_stat:
			print("Total sequence length:" , "{:0,}".format(sum(count_bases.values())))
			print("Total ungapped length:" , "{:0,}".format(sum(count_bases.values()) - count_bases['N']))
			print("Total spanned gaps:", "{:0,}".format(count_bases['N']))
			print("Number of chromosomes/scaffolds/contigs: ", "{:0,}".format(len(fasta)))
			sumGC = count_bases['G'] + count_bases['C'] + count_bases['S'] + count_bases['Y']/2 + count_bases['K']/2 + count_bases['M']/2 + count_bases['B']*2/3 + count_bases['D']/3 + count_bases['H']/3 + count_bases['V']*2/3 + count_bases['N']/2
			print("GC content (%):", "{:0,.2f}".format(sumGC * 100 / sum(count_bases.values())))
			print("N content (%):", "{:0,.2f}".format(count_bases['N'] * 100 / sum(count_bases.values())))
			scaffold_len = sorted(self.chromosomeLength.values(), reverse=True)
			half_sum_len = sum(scaffold_len)/2

			sum_len = 0
			i = 0
			while i < len(scaffold_len) and sum_len < half_sum_len:
				sum_len += scaffold_len[i]
				i += 1

			print("N50:", "{:0,}".format(scaffold_len[i-1]))
			print("L50:", "{:0,}".format(i))

	def checkChromosome(self, chromosome, start=0, end=1):
		if(start>end):
			print("Error: checkChromosome(chromosome, start, end) of", chromosome, "[" , start, "-", end ,"], the start position should be less than end")
			return False
			exit()
		elif(chromosome in self.chromosomeLength):
			if(end<=self.chromosomeLength[chromosome]):
				return True
			else:
				print("Not found "+chromosome+" at "+ str(end) +", please try again. (the first nucleotide is position = 1)")
				return False
		else:
			print("Not found "+chromosome+" ,please check chromosome again!!!")
			return False

	def getGCcontent(self, sequence):
		GC = sequence.count('G') + sequence.count('C') + sequence.count('g') + sequence.count('c')
		AT = sequence.count('A') + sequence.count('T') + sequence.count('a') + sequence.count('t')
		return float(GC) * 100 / (AT + GC)

	def getGC(self, sequence):
		return sequence.count('G') + sequence.count('C') + sequence.count('g') + sequence.count('c')

	def getStatisticSequence(self, sequence):
		GC = sequence.count('G') + sequence.count('C') + sequence.count('g') + sequence.count('c')
		AT = sequence.count('A') + sequence.count('T') + sequence.count('a') + sequence.count('t')
		N = sequence.count('N') + sequence.count('n')
		return [len(sequence), GC, AT, N, float(GC) * 100 / (AT + GC)]

	def getStatisticSeqFromGenome(self, chromosome, start, end, strand):
		seqLength = self.getChromosomeLength(chromosome)
		if (start > 0 and start < seqLength + 1 and end < seqLength + 1):
			if(strand == '+'):
				return self.getStatisticSequence(self.chromosomeSeq[chromosome][start - 1:end])
			else:
				reverse = self.chromosomeSeq[chromosome][start - 1:end]
				reverse = self.complementary(reverse[::-1])
				return self.getStatisticSequence(reverse)
		else:
			print("Out of length in seq please check again")
			print("chromosome", chromosome, "length:", seqLength)
			print("gene position:", start, "to", end, "on", strand, "strand")
			exit()

	def getChromosomeLength(self, chromosome_name):
		return self.chromosomeLength[chromosome_name]

	def getSequence(self, chromosome, start, end, strand):
		if self.checkChromosome(chromosome, start, end):
			seqLength = self.getChromosomeLength(chromosome)
			if (start > 0 and start < seqLength + 1 and end < seqLength + 1):
				if(strand == '+'):
					return self.chromosomeSeq[chromosome][start - 1:end]
				else:
					reverse = self.chromosomeSeq[chromosome][start - 1:end]
					reverse = self.complementary(reverse[::-1])
					return reverse
			else:
				return False
				print("\nOut of chromosome length, please check again.")
				print("Chromosome length:", seqLength)
				print("Error command: getSequence(", chromosome, start, end, strand, ")", sep=', ')
		else:
			return ""
	def getChrSequence(self, chromosome):
		return self.chromosomeSeq[chromosome]

	def complementary(self, seq):
		new = ""
		for base in seq:
			if(base == 'A'):
				new = new + 'T'
			elif(base == 'T'):
				new = new + 'A'
			elif(base == 'G'):
				new = new + 'C'
			elif(base == 'C'):
				new = new + 'G'
			elif(base == 'a'):
				new = new + 't'
			elif(base == 't'):
				new = new + 'a'
			elif(base == 'g'):
				new = new + 'c'
			elif(base == 'c'):
				new = new + 'g'
			else:
				new = new + base
		return new

	def searchSeqInChromosome(self, chromosome_name, pattern):
		pattern = pattern.upper()
		len_pattern = len(pattern)
		index_found = []
		# Search pattern in plus strand
		index = self.chromosomeSeq[chromosome_name].find(pattern)
		while(index > -1):
			index_found.append([index + 1, index + len_pattern, '+'])
			index = self.chromosomeSeq[chromosome_name].find(pattern, index + 1)
		# Search pattern in minus strand
		pattern = self.complementary(pattern)[::-1]
		index = self.chromosomeSeq[chromosome_name].find(pattern)
		while(index > -1):
			index_found.append([index + 1, index + len_pattern, '-'])
			index = self.chromosomeSeq[chromosome_name].find(pattern, index + 1)
		# Return [fistMatch,endMatch,strand]
		return index_found

	def searchSeqInGenome(self, pattern):
		pattern = pattern.upper()
		len_pattern = len(pattern)
		index_found = []
		for chromosome_name, seq in sorted(self.chromosomeSeq.items()):
			# Search pattern in plus strand
			index = seq.find(pattern)
			while(index > -1):
				index_found.append([chromosome_name , index + 1, index + len_pattern, '+'])
				index = seq.find(pattern, index + 1)
			# Search pattern in minus strand
			pattern = self.complementary(pattern)[::-1]
			index = seq.find(pattern)
			while(index > -1):
				index_found.append([chromosome_name, index + 1, index + len_pattern, '-'])
				index = seq.find(pattern, index + 1)	
		return index_found

class Gff_manager(object):
	def __init__(self, file_name):
		self.data = [] # all line
		self.gene_struc = {} # {'gene1': [line1 ,line2, line 3]}
		self.chromosome_contain_gene = {} # {[(chr1,'+')]: [..........]}

		gene_name = ""
		if(file_name.find('.gz') > 0):
			filegz = gzip.open(file_name, 'rb')
			gff_file = utf8(filegz)
		else:
			gff_file = open(file_name, 'r')
		for line in gff_file:
			if(line[0] != '#' and line != ''):
				line = line.split()
				line[3] = int(line[3])
				line[4] = int(line[4])
				line[8] = line[8].split(';')
				self.data.append(line)
				if(line[2] != 'gene'):

					gene_annotation.append(line)
				else:
					if(gene_name != ''):
						# gene_annotation = sorted(gene_annotation,key=itemgetter(3,4))
						self.gene_struc[gene_name] = gene_annotation
					gene_annotation = [line]
					gene_name = line[8][1][5:]
		# gene_annotation = sorted(gene_annotation,key=itemgetter(3,4))
		self.gene_struc[gene_name] = gene_annotation

		table = self.getTableSpecificType("gene")
		table = sorted(table, key=itemgetter(0,6,3,4))
		for line in table:
			if (line[0],line[6]) in self.chromosome_contain_gene:
				self.chromosome_contain_gene[(line[0],line[6])].append(line)
			else:
				self.chromosome_contain_gene[(line[0],line[6])]=[line]
		for key, value in self.chromosome_contain_gene.items():
			if (key[1] == '-'):
				self.chromosome_contain_gene[key] = sorted(value, key=itemgetter(4,3), reverse=True)

	def getNumgerOfGffLine(self):
		return len(self.data)

	def getTable(self):
		return self.data

	def getTableSpecificType(self, gene_struc_type):
		table = []
		for line in self.data:
			if(line[2] == gene_struc_type):
				table.append(line)
		return table

	def getTableSpecificTypeAndStrand(self, gene_struc_type, strand):
		table = []
		for line in self.data:
			if(line[2] == gene_struc_type and line[6]==strand):
				table.append(line)
		return table

	def printdata(self,type="five_prime_UTR"):
		countLine = 0
		for line in self.data:
			if(line[2] == type):
				print(line[0] + "\t" + line[2] + "\t" + str(line[3]) + "\t" + str(line[4]) + "\t" + line[6] + "\t" + line[8][0])
				countLine += 1

	def getTableDataOfGeneAndType(self, geneName,Type):
		table = []
		for i in self.gene_struc[geneName]:
			if(i[2]==Type):
				table.append(i)
		return table

	def getTableDataOfGene(self, geneName):
		return self.gene_struc[geneName]

	def getTranscripthave5UTR(self):
		print("gene", "transcript", "label5UTR", "lengthOf5UTR", "strand", "start", "stop", sep='\t')
		for line in self.data:
			if(line[2] == 'gene'):
				geneName = line[8][0][3:]
			elif(line[2] == 'five_prime_UTR' or line[2] == '5-UTR'):
				transcriptName = line[8][0][3:26]
				label5UTR = line[8][0][-1:]
				start5UTR = int(line[3])
				stop5UTR = int(line[4])
				len5UTR = stop5UTR - start5UTR + 1
				strand = line[6]
				print(geneName, transcriptName, label5UTR, len5UTR, strand, start5UTR, stop5UTR, sep='\t')

	def getGeneList(self):
		return sorted(list(self.gene_struc.keys()))

	def getDataSpecificType(self,gene_component):
		table = []
		for line in self.data:
			if(line[2] == gene_component):
				table.append(line)
		return table

	def getTranscript(self):
		for line in self.data:
			if(line[2] == 'mRNA'):
				print(line[8][0][3:])

	def checkGene(self, gene_name):
		if gene_name in list(self.gene_struc.keys()):
			return True
		else:
			return False

	def getGeneForward(self,gene_name):
		# return end position of forward gene, if don't have forward gene return False
		x = self.gene_struc[gene_name]
		# for i in self.gene_struc[gene_name]:
		# 	print(i)
		chromosome = x[0][0]
		strand = x[0][6]
		start=x[0][3]
		end=x[0][4]
		table_gene = self.chromosome_contain_gene[(chromosome, strand)]
	
		if(strand=="+"):
			i=0
			while(i < len(table_gene) and table_gene[i][3] < start):
				i=i+1
			i=i-1
			if(i==-1):
				return False
			else:
				return table_gene[i][4]
		else:
			i=0
			while(i < len(table_gene) and end < table_gene[i][4]):
				i=i+1
			i=i-1
			if(i==-1):
				return False
			else:
				# print(gene_name, strand, start, end)
				# print(table_gene[i])
				return table_gene[i][3]	

class Genome_manager(Fasta_manager, Gff_manager):
	def __init__(self, fastaFile, GffFile):
		self.fastaFile = fastaFile
		Fasta_manager.__init__(self, fastaFile)
		Gff_manager.__init__(self, GffFile)
		self.list_of_gene_no_promoter = []

	def getListOfGeneNoPromoter(self):
		return self.list_of_gene_no_promoter

	def getGCcontentInTranscript(self, type):
		sumGC = 0
		sumAT = 0
		for line in self.data:
			if(line[2] == type):
				# print(line[8][0][3:], line[0], line[3], line[4] , line[6], sep='\t',end = '\t')
				statistic = Fasta_manager.getStatisticSeqFromGenome(self, line[0], line[3], line[4] , line[6])
				# print(statistic[0], statistic[1], statistic[2], sep='\t')
				sumGC += statistic[1]
				sumAT += statistic[2]
		print("Summary GC content in", type, ":", float(sumGC) * 100 / (sumGC + sumAT))

	def selectedTSSProtein(self, upstream, downstream):
		file_write = open("%s_upstream_-%dto+%d.fa" % (self.fastaFile[:-6], upstream, downstream), 'w')
		statistic_of_5_prime_length = []
		geneListSelected = []
		geneCount = 0
		transcriptName = geneName = ''
		five_prime_UTR = []
		three_prime_UTR = []
		CDS = []
		count_five_prime_UTR_selected = 0
		count_five_prime_UTR_total = 0
		count_upstream_out_of_criteria = 0
		count_seq = 0

		for line in self.data:
			if(line[2] == 'gene'):
				geneName = line[8][0][3:]
				geneCount += 1
			elif(line[2] == 'mRNA'):
				count_five_prime = len(five_prime_UTR)
				if(count_five_prime > 0):
					# Gene have five_prime_UTR
					count_five_prime_UTR_selected += 1
					count_five_prime_UTR_total += count_five_prime
					if geneName not in geneListSelected:
						geneListSelected.append(geneName)
					if(five_prime_UTR[0][6] == '+'):
						five_prime_UTR.sort(key=itemgetter (3, 4))
						selected_five_prime = five_prime_UTR[count_five_prime - 1]
					else:
						five_prime_UTR.sort(key=itemgetter (4, 3))
						selected_five_prime = five_prime_UTR[0]
					sequence = Fasta_manager.getSequence(self, selected_five_prime[0], selected_five_prime[3], selected_five_prime[4], selected_five_prime[6])
					statistic_of_5_prime_length.append(len(sequence))
					# print(">", transcriptName, sep="")
					# print(sequence)
					text = self.getPromoterOfGene(upstream, downstream, selected_five_prime)
					if(text == False):
						count_upstream_out_of_criteria += 1
					else:
						file_write.writelines(text)
						count_seq += 1
				else:
					# Gene have not five_prime_UTR
					pass

				transcriptName = line[8][0][3:]
				five_prime_UTR = []
				three_prime_UTR = []
				CDS = []
			elif(line[2] == 'five_prime_UTR' or line[2] == '5-UTR'):
				five_prime_UTR.append(line)
			elif(line[2] == 'tree_prime_UTR' or line[2] == '3-UTR'):
				three_prime_UTR.append(line)
			elif(line[2] == 'CDS'):
				CDS.append(line)
		# lastLine imporve data
		count_five_prime = len(five_prime_UTR)
		if(count_five_prime > 0):
			count_five_prime_UTR_selected += 1
			count_five_prime_UTR_total += count_five_prime
			if geneName not in geneListSelected:
				geneListSelected.append(geneName)
			if(five_prime_UTR[0][6] == '+'):
				five_prime_UTR.sort(key=itemgetter (3, 4))
				selected_five_prime = five_prime_UTR[count_five_prime - 1]
			else:
				five_prime_UTR.sort(key=itemgetter (4, 3))
				selected_five_prime = five_prime_UTR[0]
			sequence = Fasta_manager.getSequence(self, selected_five_prime[0], selected_five_prime[3], selected_five_prime[4], selected_five_prime[6])
			statistic_of_5_prime_length.append(len(sequence))
			# print(">", transcriptName, sep="")
			# print(sequence)
			text = self.getPromoterOfGene(upstream, downstream, selected_five_prime)
			if(text == False):
				count_upstream_out_of_criteria += 1
			else:
				file_write.writelines(text)
				count_seq += 1

		# Get statistic
		print("Statistic of genome", "%s_upstream_-%dto+%d.fa" % (self.fastaFile[:-6], upstream, downstream))
		print("Number of annotated gene:", geneCount)
		print("Number of 5'UTR of known gene:", len(geneListSelected))
		print("Number of alternative 5'UTR transcript:", count_five_prime_UTR_total)
		print("Number of selected 5'UTR transcript (unique):", count_five_prime_UTR_selected)
		print("Upstream correct:", count_seq)
		print("Upstream out of criteria:", count_upstream_out_of_criteria)
		# Number of 5'UTR of selected transcript

	def getPromoterOfGene(self, upstream, downstream, five_prime_UTR):
		if(five_prime_UTR[6] == '+'):
			seq = Fasta_manager.getSequence(self, five_prime_UTR[0], five_prime_UTR[3] - upstream, five_prime_UTR[3] + downstream, five_prime_UTR[6])
		else:
			seq = Fasta_manager.getSequence(self, five_prime_UTR[0], five_prime_UTR[4] - downstream, five_prime_UTR[4] + upstream, five_prime_UTR[6])
			
		if(seq == False):
			return False
		else:
			if(seq.count('N') == 0):
				if(five_prime_UTR[6] == '+'):
					text = ">" + five_prime_UTR[8][0][3:] + "|" + str(five_prime_UTR[3] - upstream) + "|" + str(five_prime_UTR[3] + downstream) + "|+\n"
				else:
					text = ">" + five_prime_UTR[8][0][3:] + "|" + str(five_prime_UTR[4] - downstream) + "|" + str(five_prime_UTR[4] + upstream) + "|-\n"
				
				if(len(seq) != upstream + downstream + 1):
					print("\nLength of sequence not correct please check code it again.")
					exit()
				text = text + str(seq) + "\n"
				 # print(text)
				return text
			else:
				return False	

	def getAllPromoterKnownTSS(self, upstream, downstream):
		# Retrive upstream and downstream sequence from TSS
		not_selected = 0
		not_selected_polyN = 0
		count_seq = 0
		for line in self.data:
			if(line[2] == 'five_prime_UTR'):
				if(line[6] == '+'):
					if(line[3] > upstream):
						seq = Fasta_manager.getSequence(self, line[0], line[3] - upstream, line[3] + downstream, line[6])
					else:
						seq = Fasta_manager.getSequence(self, line[0], 1, line[3] + downstream, line[6])
				else:
					if(line[4]+upstream <= Fasta_manager.getChromosomeLength(self, line[0])):
						seq = Fasta_manager.getSequence(self, line[0], line[4] - downstream, line[4] + upstream, line[6])
					else:
						seq = Fasta_manager.getSequence(self, line[0], line[4] - downstream, Fasta_manager.getChromosomeLength(self, line[0]), line[6])
				if(seq == False):
					not_selected += 1
				else:
					if(seq.count('N') == 0):
						if(len(seq) == upstream + downstream + 1):
							if(line[6] == '+'):
								print(">", line[8][0][3:],"|",line[0],"|",line[3]-upstream,"|",line[3]+downstream,"|+" ,sep='')
							else:
								print(">", line[8][0][3:],"|",line[0],"|",line[4]-downstream,"|",line[4]+upstream, "|-" ,sep='')
							print(seq)
							count_seq += 1
						else:
							not_selected +=1
					else:
						not_selected_polyN += 1
		print("not selected sequence:", not_selected)
		print("not selected sequence because N:", not_selected_polyN)
		print("It including ", count_seq, "sequences for next step")

	def check_correct_position(self, chromosome_name, gene_name, prom_start, prom_end, strand, min_len, removed_N_gap):
		# Return False when postion of promoter is not correct, if promoter region is correct, it return promoter old postion or correct position
		
		# Check the promoter is inside chromosome
		chromosome_len = Fasta_manager.getChromosomeLength(self, chromosome_name)
		if prom_start < 1:
			prom_start = 1
		elif prom_start > chromosome_len:
			prom_start = chromosome_len
			prom_end = chromosome_len
		elif prom_end > chromosome_len:
			prom_end = chromosome_len
		if prom_end < 1:
			prom_end = 1

		# Check the promoter is not overlap forward genes
		forward_end_pos = self.getGeneForward(gene_name)
		if(forward_end_pos != False):
			if strand == '+':
				if prom_start < forward_end_pos +1 and prom_end > forward_end_pos:
					prom_start = forward_end_pos + 1
				elif prom_end == forward_end_pos:
					prom_start = prom_end
				elif prom_end < forward_end_pos:
					return False
			elif strand == '-':
				if prom_end > forward_end_pos - 1 and prom_start < forward_end_pos:
					prom_end = forward_end_pos - 1
				elif prom_start == forward_end_pos:
					prom_end = prom_start
				elif prom_start > forward_end_pos:
					return False

		# Check promoter not contain poly N in the end of promoter [NNNNNNNNNNNNNatgATGGCAAATCGCCNNNN  --->   atgATGGCAAATCGCCNNNN]
		# If length of promoter more than min_len is return currect postion, else return False (This gene not have promoter)
		if (removed_N_gap == True):
			sequence = Fasta_manager.getSequence(self, chromosome_name, prom_start, prom_end, strand)
			if sequence[0] == 'N':
				pos = re.search('[ATGCatgc]+', sequence)
				if(pos != None):
					seq = sequence[pos.start():]
					if strand == '+' and len(seq)>=min_len:
						prom_start += pos.start()
						return {'promoter_start': prom_start, 'promoter_end': prom_end}
					if strand == '-' and len(seq)>=min_len:
						prom_end -= pos.start()
						return {'promoter_start': prom_start, 'promoter_end': prom_end}
					else:
						return False
				else:
					return False
			elif prom_end - prom_start +1 >= min_len:
				return {'promoter_start': prom_start, 'promoter_end': prom_end}
			else:
				return False
		else:
			seq = Fasta_manager.getSequence(self, chromosome_name, prom_start, prom_end, strand)
			if strand == '+' and len(seq)>=min_len:
				return {'promoter_start': prom_start, 'promoter_end': prom_end}
			if strand == '-' and len(seq)>=min_len:
				return {'promoter_start': prom_start, 'promoter_end': prom_end}
			else:
				return False

	def getPromoterOfGeneFromTLS(self, gene_name, upstream, downstream, promoter_min_len, removed_N_gap, output_format):
		gene_struc_table = Gff_manager.getTableDataOfGeneAndType(self, gene_name, "CDS")
		if(len(gene_struc_table)==0):
			print("Gene name is not currect, please check it again")
			exit()
		else:
			strand = gene_struc_table[0][6]
			chromosome = gene_struc_table[0][0]
			if(strand == '+'):
				promoter_start = gene_struc_table[0][3] - upstream
				promoter_end = gene_struc_table[0][3] + downstream - 1
			else:
				gene_struc_table = sorted(gene_struc_table,key=itemgetter(4), reverse=True)
				promoter_start = gene_struc_table[0][4] - downstream + 1
				promoter_end = gene_struc_table[0][4] + upstream

			new_promoter_position = self.check_correct_position(chromosome, gene_name, promoter_start, promoter_end, strand, promoter_min_len, removed_N_gap)
			if(new_promoter_position==False):
				self.list_of_gene_no_promoter.append(gene_name)
				return ''
			else:
				promoter_start = new_promoter_position['promoter_start']
				promoter_end = new_promoter_position['promoter_end']
				seq = Fasta_manager.getSequence(self, chromosome, promoter_start, promoter_end, strand)

				if (output_format.lower() == 'fasta' or output_format.lower() == 'fa'): 
					# Fasta writing
					text = ">" + gene_name + "_promoter|" + chromosome + "|" + str(promoter_start) + "|" + str(promoter_end) + "|" + strand + "|length=" + str(promoter_end - promoter_start + 1) + "|Promoter from CDS|" + version + "\n"
					text = text + seq + "\n"
				elif (output_format.lower() == 'gff' or output_format.lower() == 'gff3'):
					# GFF writing
					text = chromosome + "\t" + version + "\t" + "promoter" + "\t" + str(promoter_start) + "\t" + str(promoter_end) + "\t.\t" + strand + "\t.\t" + "ID=" + gene_name + "_promoter;Name=" + gene_name + ";length=" + str(promoter_end-promoter_start+1) + "\n"
				return text

	def getAllPromoterOfGeneFromTLS(self, upstream, downstream, promoter_min_len, removed_N_gap, output_format):
		for gene_name in Gff_manager.getGeneList(self):
			self.getPromoterOfGeneFromTLS(gene_name, upstream, downstream, promoter_min_len, removed_N_gap, output_format)
		print("\n-----------List of gene no promoter-----------")
		for gene_name in self.list_of_gene_no_promoter:
			print(gene_name)

	def getPromoterOfGeneFromTSS(self, gene_name, upstream, downstream, promoter_min_len, removed_N_gap, output_format):
		gene_struc_table = Gff_manager.getTableDataOfGeneAndType(self, gene_name, "five_prime_UTR")
		if(len(gene_struc_table)==0):
			#print("No information of 5'UTR of gene", gene_name)
			return self.getPromoterOfGeneFromTLS(gene_name, upstream, downstream, promoter_min_len)
		else:
			strand = gene_struc_table[0][6]
			chromosome = gene_struc_table[0][0]
			if(strand == '+'):
				gene_struc_table = sorted(gene_struc_table,key=itemgetter(3), reverse=True)
				promoter_start = gene_struc_table[0][3] - upstream
				promoter_end = gene_struc_table[0][3] + downstream - 1
			else:
				gene_struc_table = sorted(gene_struc_table,key=itemgetter(4))
				promoter_start = gene_struc_table[0][4] - downstream + 1
				promoter_end = gene_struc_table[0][4] + upstream

			new_promoter_position = self.check_correct_position(chromosome, gene_name, promoter_start, promoter_end, strand, promoter_min_len,removed_N_gap)
			if(new_promoter_position==False):
				self.list_of_gene_no_promoter.append(gene_name)
				return ''
			else:
				promoter_start = new_promoter_position['promoter_start']
				promoter_end = new_promoter_position['promoter_end']
				seq = Fasta_manager.getSequence(self, chromosome, promoter_start, promoter_end, strand)
				
				if (output_format.lower() == 'fasta' or output_format.lower() == 'fa'): 
					# Fasta writing
					text = ">" + gene_name + "_promoter|" + chromosome + "|" + str(promoter_start) + "|" + str(promoter_end) + "|" + strand + "|length=" + str(promoter_end - promoter_start + 1) + "|Promoter from 5'UTR|" + version + "\n"
					text = text + seq + "\n"
				elif (output_format.lower() == 'gff' or output_format.lower() == 'gff3'):
					text = chromosome + "\t" + version + "\t" + "promoter" + "\t" + str(promoter_start) + "\t" + str(promoter_end) + "\t.\t" + strand + "\t.\t" + "ID=" + gene_name + "_promoter;Name=" + gene_name + ";length=" + str(promoter_end-promoter_start+1) +"\n"
				return text

	def getAllPromoterOfGeneFromTSS(self, upstream, downstream, promoter_min_len, removed_N_gap, output_format):
		for gene_name in Gff_manager.getGeneList(self):
			self.getPromoterOfGeneFromTSS(gene_name, upstream, downstream, promoter_min_len, removed_N_gap, output_format)
			
		print("\n-----------List of gene no promoter-----------")
		for gene_name in self.list_of_gene_no_promoter:
			print(gene_name)
