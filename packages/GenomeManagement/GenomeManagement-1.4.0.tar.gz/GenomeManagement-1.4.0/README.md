# Genome Management Package
This package allows users to obtain genomic statistics from an assembled genome. With an easy way to manipulate genomic data, for example, get the promoter region of each gene and select interseted proteins from a FASTA file of all proteins.


# Usage: Promoter of genes retrieving
Then run python script by used command line on windows or unix::

    python3 promoter_retrieve.py \
		--output <output_file.fa> \
		--output_format <fasta/gff> \
		--genome <genome.fa> \
		--gff <genome.gff> \
		--type <TLS/TSS> \
		--upstream <bp> \
		--downstream <bp> \
		--all_gene <Y/N> \
		--selected_gene_list <gene_list.txt, is optional if all_gene is N> \
		--remove_n_gap <Y/N> \
		--min_length <default is 100 bp>

# Usage: Get protein or gene sequences from genome
	python3 proteins_retrieve.py \
		--input <input_fasta_file> \
		--list_of_interest <list_of_protein_id.txt> \
		--output <output_file.fa>

# Usage: Get genome statistic
	python3 get_genome_statistic.py \
		--genome <genome.fa>
