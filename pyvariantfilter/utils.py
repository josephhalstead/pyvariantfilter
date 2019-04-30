def parse_csq_field(csq_fields, field_description):
	"""
	Get the VEP CSQ field as a list of dictionaries.

	Each transcript will be its own dictionary in the list.

	Input:

	csq_fields - A tuple containing the different transcipt annotations for VEP e.g ('A|missense_variant', 'A|5_prime_UTR_variant' )

	field_description - List of CSQ field descriptions from VCF header e.g. ['Allele', 'Consequence']

	Returns:

		A list of dictionaries - each transcript the variant falls within has its own dictionary. The key to each dictionary comes from the field_description input.

	"""

	consequence_list = []

	for csq in csq_fields:

		csq_dict = {}

		csq = csq.split('|')

		for key, value in zip(field_description, csq):

			csq_dict[key] = value

		consequence_list.append(csq_dict)

	return consequence_list


def get_info_field_dict(info_fields, vep_csq_key='CSQ'):
	"""
	Get the info fields from a VCF as a dictionary.

	Exclude the VEP annotation field e.g. CSQ.

	Input:

	info_fields - The info_fields object from the PySam VCF parser.
	vep_csq_key - The key to access the CSQ field.


	"""

	info_dict = {}

	for key in info_fields.keys():

		if key != vep_csq_key:

			if isinstance(info_fields[key], tuple) and len(info_fields[key]) ==1:

				info_dict[key] = info_fields[key][0]

			else:

				info_dict[key] = info_fields[key]


	return info_dict

def compound_het_pair_pass_filter(pair,
							 affected,
							 unaffected,
							 proband_dad,
							 proband_mum,
							 include_denovo=True,
							 allow_hets_in_unaffected=False,
							 check_affected=True):

	"""
	Filter compound hets in a proband with both parents. Return True if they are genuine compoun hets.

	Input:

	pair - a list containing a compound het pair
	affected - a list containing affected family members.
	unaffected - A list containing unaffected family members.

	Output:

	True - If the pair pass the compound het filter
	False - If the pair fail the compound het filter.

	Rules:

	1) No unaffected samples can have the pair of variants. Can be adjusted using the allow_hets_in_unaffected argument.
	2) All affected samples must have the pair of variants or be missing the genotype data. Can be adjusted using the check_affected argument.
	3) a) One of the pair must be inherited from mum and the other from dad.
	   b) If include_denovo is True then one of the pair can be de_novo and the other inherited from either parent or both can be de_novo. There are no minimum requirements e.g. depth on the de_novo calls.

	"""

	var1 = pair[0]
	var2 = pair[1]

	# Check unaffected  - if unaffected people have pair then break
	if allow_hets_in_unaffected == False:

		for sample_id in unaffected:

			if var1.is_het(sample_id) and var2.is_het(sample_id):

				return False

	# Check affected - all affected must have the variant pair or be missing the variant
	if check_affected == True:

		for sample_id in affected:

			if var1.is_hom_ref(sample_id) or var2.is_hom_ref(sample_id) and (var1.is_missing(sample_id) == False or var2.is_missing(sample_id) == False) :

				return False

	# if var 1 comes from mum and var 2 comes from dad
	if var1.has_no_alt(proband_dad) and var1.is_het(proband_mum) and var2.has_no_alt(proband_mum) and var2.is_het(proband_dad): 
		return True

	# if var 2 comes from mum and var 1 comes from dad
	elif var1.has_no_alt(proband_mum) and var1.is_het(proband_dad) and var2.has_no_alt(proband_dad) and var2.is_het(proband_mum):
		return True

	# mum is het for var1 and hom ref for var2 and dad is missing both genotypes for var 1 and var 2
	elif var1.is_het(proband_mum) and var2.is_hom_ref(proband_mum) and var1.is_missing(proband_dad) and var2.is_missing(proband_dad):
		return True

	# dad is het for var1 and hom ref for var2 and mum is missing both genotypes for var 1 and var 2
	elif var1.is_het(proband_dad) and var2.is_hom_ref(proband_dad) and var1.is_missing(proband_mum) and var2.is_missing(proband_mum):
		return True

	# if var1 is denovo and var2 is het in dad
	elif (var1.matches_denovo(min_parental_gq=0, min_parental_depth=-1, max_parental_alt_ref_ratio=1) and
		  var2.is_het(proband_dad) and
		  var2.has_no_alt(proband_mum) and
		  include_denovo == True):
		return True

	# if var1 is denovo and var2 is het in mum
	elif (var1.matches_denovo(min_parental_gq=0, min_parental_depth=-1, max_parental_alt_ref_ratio=1) and
		  var2.is_het(proband_mum) and
		  var2.has_no_alt(proband_dad) and
		  include_denovo == True):
		return True

   # if var2 is denovo  and var1 is het in mum
	elif (var2.matches_denovo(min_parental_gq=0, min_parental_depth=-1, max_parental_alt_ref_ratio=1) and
		  var1.is_het(proband_mum) and
		  var1.has_no_alt(proband_dad) and
		  include_denovo == True):
		return True

   # if var2 is denovo  and var1 is het in dad
	elif (var2.matches_denovo(min_parental_gq=0, min_parental_depth=-1, max_parental_alt_ref_ratio=1) and
		  var1.is_het(proband_dad) and
		  var1.has_no_alt(proband_mum) and
		  include_denovo == True):
		return True

	# if both var1 and var2 are denovo
	elif (var1.matches_denovo(min_parental_gq=0, min_parental_depth=-1, max_parental_alt_ref_ratio=1) and
		  var2.matches_denovo(min_parental_gq=0, min_parental_depth=-1, max_parental_alt_ref_ratio=1) and
		  include_denovo == True):
		return True

	# Options below will only be True if allow_hets_in_unaffected is True

	# if mum is het for var1 and dad is het for var1 and var2
	elif var1.is_het(proband_mum) and var2.has_no_alt(proband_mum) and var1.is_het(proband_dad) and var2.is_het(proband_dad):
		return True
	
	# if mum is het for var2 and dad is het for var1 and var2
	elif var2.is_het(proband_mum) and var1.has_no_alt(proband_mum) and var1.is_het(proband_dad) and var2.is_het(proband_dad):
		return True

	# if dad is het for var1 and mum is het for var1 and var2
	elif var1.is_het(proband_dad) and var2.has_no_alt(proband_dad) and var1.is_het(proband_mum) and var2.is_het(proband_mum):
		return True
	
	# if dad is het for var2 and mum is het for var1 and var2
	elif var2.is_het(proband_dad) and var1.has_no_alt(proband_dad) and var1.is_het(proband_mum) and var2.is_het(proband_mum):
		return True

	# if both parents are het for both var1 and var2
	elif var1.is_het(proband_dad) and var2.is_het(proband_dad) and var1.is_het(proband_mum) and var2.is_het(proband_mum):
		return True 

	# if mum is het for both var1 and var2 and dad is missing both var1 and var2
	elif var1.is_het(proband_mum) and var2.is_het(proband_mum) and var1.is_missing(proband_dad) and var2.is_het(proband_dad):
		return True

	# if dad is het for both var1 and var2 and mum is missing both var1 and var2
	elif var1.is_het(proband_dad) and var2.is_het(proband_dad) and var1.is_missing(proband_mum) and var2.is_het(proband_mum):
		return True
	else:
		return False



		