import os
import csv
import glob

def run_phenolyzer(perl_executable, phenolyzer_script, temp_dir, job_name, hpo_terms, symbol=True):
	"""
	Python wrapper for running Phenolyzer on default settings.

	Input:

		perl_executable (String): Location of the perl executable.
		phenolyzer_script (String): The location of the disease_annotation.pl script.
		temp_dir (String): A temporary directory to store results.
		job_name (String): A name for the temporary files.
		hpo_terms (List): List of HPO terms to use.
		symbol (Boolean): Whether to use the gene symbol or the gene_id as the key in the output dictionary.

	Output:
		
		gene_score_dict (Dict): A dictionary with the gene as the key and the score as the value.

	"""

	assert temp_dir != '' and job_name != ''

	final_gene_list = f'{temp_dir}/phenolyser_result_{job_name}.final_gene_list'

	gene_score_dict = {}

	for term in hpo_terms:

		if term[0:3] != 'HP:':

			raise ValueError(f'{term} does not begin with HP:')


	hpo_terms = ';'.join(hpo_terms)
	command = f'{perl_executable} {phenolyzer_script} "{hpo_terms}" -p -ph -logistic -out {temp_dir}/phenolyser_result_{job_name}'

	os.system(command)

	exists = os.path.isfile(final_gene_list)

	if not exists:

		raise ValueError('No output file created.')

	with open(final_gene_list) as csvfile:

		reader = csv.reader(csvfile, delimiter='\t')

		for row in reader:

			if row[1] != 'Gene':

				if symbol:

					gene_score_dict[row[1]] = row[3]

				else:

					gene_score_dict[row[2]] = row[3]


	# Remove old files.

	file_roots = f'{temp_dir}/phenolyser_result_{job_name}'

	files = glob.glob(f'{file_roots}*')

	for file in files:

		os.remove(file)

	return gene_score_dict

def run_phen2gene(phen2gene_dir, temp_dir, job_name, hpo_terms, symbol=True):
	"""
	Python wrapper for running Phen2Gene on default settings.

	Input:

		phen2gene_dir (String): Location of the directory containing the Phen2Gene script.
		temp_dir (String): A temporary directory to store results.
		job_name (String): A name for the temporary files.
		hpo_terms (List): List of HPO terms to use.
		symbol (Boolean): Whether to use the gene symbol or the gene_id as the key in the output dictionary.

	Output:
		
		gene_score_dict (Dict): A dictionary with the gene as the key and the score as the value.

	"""

	assert temp_dir != '' and job_name != ''

	gene_score_dict = {}

	hpo_terms = ' '.join(hpo_terms)

	command = f'cd {phen2gene_dir} && python {phen2gene_dir}/phen2gene.py -m  {hpo_terms} -out temp/{job_name}'
	os.system(command)

	final_gene_list = f'{phen2gene_dir}/temp/{job_name}/input_case.final_candidate_gene_list'

	exists = os.path.isfile(final_gene_list)

	if not exists:

		raise ValueError('No output file created.')

	with open(final_gene_list) as csvfile:

		reader = csv.reader(csvfile, delimiter='\t')

		for row in reader:

			if row[1] != 'Gene':

				if symbol:

					gene_score_dict[row[1]] = row[3]

				else:

					gene_score_dict[row[2]] = row[3]


	os.remove(final_gene_list)

	return gene_score_dict











