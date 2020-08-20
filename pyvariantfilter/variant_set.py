from pyvariantfilter.variant import Variant
from pyvariantfilter.family import Family
from pyvariantfilter.utils import parse_csq_field, get_info_field_dict, compound_het_pair_pass_filter
from pysam import VariantFile
import itertools
import pandas as pd
from copy import deepcopy

class VariantSet:
	"""
	A VariantSet object allows multiple variants within a single family to be associated with each other.
	"""
	
	def __init__(self):
		
		self.candidate_compound_het_dict = {}
		self.filtered_compound_het_dict = {}
		self.variant_dict = {}
		self.final_compound_hets = {}
		self.family = None

	def add_family(self, family):
		"""
		Add a family to a VariantSet

		Input:

			family: (Family) - A family object to associate with the VariantSet

		Returns:

			None 

		"""

		assert isinstance(family, Family)
		assert bool(self.variant_dict) == False
		self.family = family
	
	def add_variant(self, variant):
		"""
		Add a variant to a VariantSet.

		Input:
		
			variant: (Variant) - A Variant object to add to the variant set.

		"""

		assert variant.family.family_id == self.family.family_id
		
		if variant.variant_id not in self.variant_dict:
		
			self.variant_dict[variant.variant_id] = variant


	def read_variants_from_vcf(self, vcf_file, parse_csq=True, vep_csq_key='CSQ', proband_variants_only=True, filter_func=None, args=None):
		"""
		Read variants from a standard VCF. Must have AD,GQ and DP fields in the Format section for each sample.

		Input:

			vcf_file: (String) Path to the VCF file to read.
			parse_csq: (Boolean) Whether to attempt to parse the CSQ field added by VEP.
			vep_csq_key: (String) The key of the CSQ field in the VCF INFO section.
			proband_variants_only (Boolean) Only load variants which the proband has an alt allele.
			import_filtered (Boolean) Whether to import variants which fail the VCF Filter

		Returns:

			None - loads variants into self.variant_dict

		"""

		valid_chroms = {'1': None, '2': None, '3': None, '4': None,
		 '5': None, '6': None, '7': None, '8': None, '9': None,
		 '10': None, '11': None, '12': None, '13': None,
		 '14': None, '15': None, '16': None, '17': None,
		 '18': None, '19': None, '20': None, '21': None,
		 '22': None, 'X': None, 'Y': None, 'MT': None, 'M': None}

		assert self.family != None

		family_member_ids = self.family.get_all_family_member_ids()

		if proband_variants_only == True:

			proband_id = self.family.get_proband().get_id()

		bcf_in = VariantFile(vcf_file)

		if parse_csq == True:

			csq_fields = str(bcf_in.header.info[vep_csq_key].record)

			csq_fields = csq_fields = csq_fields.strip()

			index = csq_fields.index('Format:') + 8

			csq_fields = csq_fields[index:len(csq_fields)-2].split('|')

		for rec in bcf_in.fetch():
			
			chrom = rec.chrom
			pos = rec.pos
			ref = rec.ref
			alt = rec.alts
			filter_status = rec.filter.keys()
			info = rec.info
			quality = rec.qual

			if 'chr' in chrom:

				chrom = chrom.strip('chr')

			# Chromosome is correct
			if chrom not in valid_chroms:

				print (f'{chrom} is not a valid chromosome. Not entered into variant set.')

				continue

			info_dict = get_info_field_dict(info, vep_csq_key)

			assert len(alt) == 1

			alt = alt[0]

			if alt == '*':
				continue

			if parse_csq == True:

				csq = rec.info[vep_csq_key]

				transcript_annotations = parse_csq_field(csq, csq_fields)

			new_variant = Variant(chrom=chrom, pos=pos, ref=ref, alt=alt, filter_status=filter_status, quality=quality)
			new_variant.add_family(self.family)
			new_variant.add_transcript_annotations(transcript_annotations)
			new_variant.add_info_annotations(info_dict)

			for family_member_id in family_member_ids:

				sample_genotype_data = rec.samples[family_member_id]
				
				ref_and_alt = [ref, alt]
				
				gts =[]
				ads =[]
				
				for allele in sample_genotype_data['GT']:
					
					if allele == None:
						
						gts.append('.')
						
					else:
						
						gts.append(ref_and_alt[allele])

				if gts[0] == '.' and gts[1] == '.':

						ads.append(0)
						ads.append(0)

				elif len(sample_genotype_data['AD']) == 1 and sample_genotype_data['AD'][0] == None:

						ads.append(0)
						ads.append(0)

				else:

					assert len(sample_genotype_data['AD']) ==2

					for ad in sample_genotype_data['AD']:
					
						if ad == None:
						
							ads.append(0)
						
						else:
						
							ads.append(ad)
				try:

					gq = sample_genotype_data['GQ']

				except:

					print (f'Warning No GQ for variant {new_variant.variant_id}. This could cause filtering errors.')
					# set to high so we don't accidently filter out
					gq = 100

				if gq == None:

					gq = 0

				dp = sample_genotype_data['DP']

				if dp == None:

					dp  = 0
				
				new_variant.add_genotype(family_member_id, gts, ads, gq, dp)

			passes_filter = True

			if filter_func != None and args != None:

				passes_filter = filter_func(new_variant, *args)

				assert passes_filter == True or passes_filter == False

			if proband_variants_only == True:

				if new_variant.has_alt(proband_id) == True and passes_filter == True:

					self.add_variant(new_variant)

			elif passes_filter == True:

				self.add_variant(new_variant)

	def read_variants_from_platypus_vcf(self, vcf_file, parse_csq=True, vep_csq_key='CSQ', proband_variants_only=True, filter_func=None, args=None):
		"""
		Read variants from a platypus VCF. Must have NR, NV and GQ fields in the Format section for each sample.

		Input:

			vcf_file: (String) Path to the VCF file to read.
			parse_csq: (Boolean) Whether to attempt to parse the CSQ field added by VEP.
			vep_csq_key: (String) The key of the CSQ field in the VCF INFO section.
			proband_variants_only (Boolean) Only load variants which the proband has an alt allele.
			import_filtered (Boolean) Whether to import variants which fail the VCF Filter

		Returns:

			None - loads variants into self.variant_dict

		"""
		valid_chroms = {'1': None, '2': None, '3': None, '4': None,
		 '5': None, '6': None, '7': None, '8': None, '9': None,
		 '10': None, '11': None, '12': None, '13': None,
		 '14': None, '15': None, '16': None, '17': None,
		 '18': None, '19': None, '20': None, '21': None,
		 '22': None, 'X': None, 'Y': None, 'MT': None, 'M': None}

		assert self.family != None

		family_member_ids = self.family.get_all_family_member_ids()

		if proband_variants_only == True:

			proband_id = self.family.get_proband().get_id()

		bcf_in = VariantFile(vcf_file)

		if parse_csq == True:

			csq_fields = str(bcf_in.header.info[vep_csq_key].record)

			csq_fields = csq_fields = csq_fields.strip()

			index = csq_fields.index('Format:') + 8

			csq_fields = csq_fields[index:len(csq_fields)-2].split('|')

		for rec in bcf_in.fetch():
			
			chrom = rec.chrom
			pos = rec.pos
			ref = rec.ref
			alt = rec.alts
			filter_status = rec.filter.keys()
			info = rec.info
			quality = rec.qual

			info_dict = get_info_field_dict(info, vep_csq_key)

			if 'chr' in chrom:

				chrom = chrom.strip('chr')

			# Chromosome is correct
			if chrom not in valid_chroms:

				print (f'{chrom} is not a valid chromosome. Not entered into variant set.')

				continue
			
			assert len(alt) == 1

			alt = alt[0]

			if alt == '*':
				continue

			if parse_csq == True:

				csq = rec.info[vep_csq_key]

				transcript_annotations = parse_csq_field(csq, csq_fields)

			new_variant = Variant(chrom=chrom, pos=pos, ref=ref, alt=alt, filter_status=filter_status, quality=quality)
			new_variant.add_family(self.family)
			new_variant.add_transcript_annotations(transcript_annotations)
			new_variant.add_info_annotations(info_dict)


			for family_member_id in family_member_ids:

				sample_genotype_data = rec.samples[family_member_id]
				
				ref_and_alt = [ref, alt]
				
				gts =[]
				ads =[]
				
				for allele in sample_genotype_data['GT']:
					
					if allele == None:
						
						gts.append('.')
						
					else:
						
						gts.append(ref_and_alt[allele])

				if gts[0] == '.' and gts[1] == '.':

						ads.append(0)
						ads.append(0)


				else:

					total_depth = sample_genotype_data['NR']
					variant_depth = sample_genotype_data['NV']

					assert len(total_depth) == 1
					assert len(variant_depth) == 1

					allele_depth_ref = total_depth[0] - variant_depth[0]
					allele_depth_alt = variant_depth[0]


					ads.append(allele_depth_ref)
					ads.append(allele_depth_alt)

				gq = sample_genotype_data['GQ'][0]

				if gq == None:

					gq = 0

				dp = sample_genotype_data['NR'][0]

				if dp == None:

					dp  = 0

				
				new_variant.add_genotype(family_member_id, gts, ads, gq, dp)

			passes_filter = True

			if filter_func != None and args != None:

				passes_filter = filter_func(new_variant, *args)

				assert passes_filter == True or passes_filter == False


			if proband_variants_only == True:

				if new_variant.has_alt(proband_id) == True and passes_filter == True:

					self.add_variant(new_variant)

			elif passes_filter == True:

				self.add_variant(new_variant)
	
				
	def get_candidate_compound_hets(self, feature_key='Feature', consequences={'transcript_ablation': None,
													'splice_acceptor_variant': None,
													'splice_donor_variant': None,
													'stop_gained': None,
													'frameshift_variant': None,
													'stop_lost': None,
													'start_lost': None,
													'transcript_amplification': None,
													'inframe_insertion': None,
													'inframe_deletion': None,
													'missense_variant': None,
													'protein_altering_variant': None,
													'splice_region_variant': None,
													'incomplete_terminal_codon_variant': None,
													'start_retained_variant': None,
													'stop_retained_variant': None,
													'synonymous_variant': None,
													'coding_sequence_variant': None,
													'mature_miRNA_variant': None,
													'5_prime_UTR_variant': None,
													'3_prime_UTR_variant': None,
													'non_coding_transcript_exon_variant': None,
													'intron_variant': None,
													'NMD_transcript_variant': None,
													'non_coding_transcript_variant': None,
													'upstream_gene_variant': None,
													'downstream_gene_variant': None,
													'TFBS_ablation': None,
													'TFBS_amplification': None,
													'TF_binding_site_variant': None,
													'regulatory_region_ablation': None,
													'regulatory_region_amplification': None,
													'feature_elongation': None,
													'regulatory_region_variant': None,
													'feature_truncation': None,
													} ):

		"""
		Go though each variant in the self.variant_dict and build a dictionary of with each transcript as a key 
		and variants within that transcript as a value.

		Only include variants where the proband is heterozozygous, the variant is on an autosome or the X in a female,
		the worst consequence of the variant is in the consequences dict and the variant is not hom_alt in any unaffected 
		samples.

		Input:

			feature_key: (String) The feature to group compound hets on. WARNING - must be unique to a variant - don't use SYMBOL use transcript ID.
			consequences: (Dict) A dictionary containing the consequences to include as a compound het.

		Returns:

			None - loads self.candidate_compound_het_dict

		"""


		assert isinstance(self.family, Family)

		self.candidate_compound_het_dict = {}

		proband = self.family.get_proband()
				
		for variant in self.variant_dict:
			
			if (self.variant_dict[variant].is_on_autosome_or_xfemale() and
				self.variant_dict[variant].is_het(proband.get_id()) and 
				self.variant_dict[variant].get_worst_consequence() in consequences):

				if self.variant_dict[variant].is_hom_alt_in_unaffected() == False:
			
					for gene in self.variant_dict[variant].get_genes(feature_key=feature_key):

						if gene not in self.candidate_compound_het_dict:

							self.candidate_compound_het_dict[gene] = [self.variant_dict[variant]]

						else:

							self.candidate_compound_het_dict[gene].append(self.variant_dict[variant])


	def get_unfiltered_compound_hets_as_dict(self):
		"""
		Flatten the candidate compound het dict. When a gene has two or more variants as values then 
		each of these variants are added to the dict.

		Use for singlton analysis.

		Input: Self

		Returns: None - Loads self.final_compound_hets

		"""

		assert self.candidate_compound_het_dict != False

		self.final_compound_hets = {}

		for gene in self.candidate_compound_het_dict:

			if len(self.candidate_compound_het_dict[gene]) > 1:

				for variant in self.candidate_compound_het_dict[gene]:

					self.final_compound_hets[variant.variant_id] = None

	
	def filter_compound_hets(self, include_both_parents_missing=True,
							 include_denovo=True,
							 allow_hets_in_unaffected=False,
							 check_affected=True):

		"""
		Filter compound hets by phasing them by descent using parental information.

		Input:
		
		include_both_parents_missing (Boolean)
		include_denovo (Boolean)
		allow_hets_in_unaffected (Boolean)
		check_affected (Boolean)

		Returns: None - creates self.filtered_compound_het_dict

		"""

		self.filtered_compound_het_dict = {}
	
		proband = self.family.get_proband()
		proband_id = proband.get_id()
		
		proband_dad = proband.get_dad().get_id()
		proband_mum = proband.get_mum().get_id()
		
		affected = self.family.get_affected_family_members()
		unaffected = self.family.get_unaffected_family_members()
				
		for gene in self.candidate_compound_het_dict:
			
			# If we have more than one candidate in the gene
			if len(self.candidate_compound_het_dict[gene]) > 1:
				
				# Get all candidate combinations within gene
				all_combinations = list(itertools.combinations(self.candidate_compound_het_dict[gene],2))
				
				# Loop Through each pair
				for pair in all_combinations:

					if compound_het_pair_pass_filter(pair,
													 affected,
													 unaffected,
													 proband_dad,
													 proband_mum,
													 include_denovo=include_denovo,
													 allow_hets_in_unaffected=allow_hets_in_unaffected,
													 check_affected=check_affected) == True:
						
						if gene not in self.filtered_compound_het_dict:
							
							self.filtered_compound_het_dict[gene] = [pair]
							
						else:


							self.filtered_compound_het_dict[gene].append(pair)
						

	def get_filtered_compound_hets_as_dict(self):
		"""
		Flatten the filtered_compound_het_dict. Variants in the self.filtered_compound_het_dict will be added to 
		a flat self.final_compound_hets dict.

		Use for trio analysis.

		Input: Self

		Returns: None - Loads self.final_compound_hets

		"""

		self.final_compound_hets = {}

		assert self.filtered_compound_het_dict != False

		for gene in self.filtered_compound_het_dict:

			for pair in self.filtered_compound_het_dict[gene]:

				for variant in pair:

					self.final_compound_hets[variant.variant_id] = None


	def filter_variants(self, function, args):
		"""
		Apply a filtering function to the self.variant_dict.

		Input:

			function: (function) A Python function that should take a Variant object as its first argument.
			args: (Tuple) A tuple of additional arguments to the function argument e.g. (1,2,)

		Returns:

			None - filters self.variant_dict

		"""

		self.variant_dict = {k : v for k,v in filter(lambda x: function(x[1], *args), self.variant_dict.items())}


	def to_df(self, add_inheritance=True,
				 lenient=False,
				 low_penetrance_genes={},
				 min_parental_gq_dn=10,
				 min_parental_depth_dn=10,
				 max_parental_alt_ref_ratio_dn=0.04,
				 min_parental_gq_upi=10,
				 min_parental_depth_upi=10):
		"""
		Convert variant_dict to Pandas DataFrame.

		Input: None

		Returns: Pandas DataFrame object.

		"""

		df_list = []

		for variant in self.variant_dict :
	
			var = self.variant_dict [variant]
			
			for transcript in var.transcript_annotations:
				
				row = {}
				
				row['chromosome'] = var.chrom
				row['position'] = var.pos
				row['ref'] = var.ref
				row['alt'] = var.alt
				row['filter_status'] = '|'.join(var.filter_status)
				row['family_id'] = var.family.family_id
				row['variant_id'] = var.variant_id

				if add_inheritance == True:

					row['inheritance_models'] = '|'.join(var.get_matching_inheritance_models(compound_het_dict= self.final_compound_hets,
																							lenient=lenient,
																							min_parental_gq_dn=min_parental_gq_dn,
																							min_parental_depth_dn =min_parental_depth_dn,
																							max_parental_alt_ref_ratio_dn= max_parental_alt_ref_ratio_dn,
																							min_parental_gq_upi = min_parental_gq_upi,
																							min_parental_depth_upi = min_parental_depth_upi
																							))

				row['worst_consequence'] = var.get_worst_consequence()
				
				for sample in var.genotypes:
						   
					row[f'{sample}_GT'] = '/'.join(var.genotypes[sample]['genotype'])
					row[f'{sample}_AD'] =  ','.join(str(x) for x in var.genotypes[sample]['allele_depths'])
					row[f'{sample}_DP'] = var.genotypes[sample]['depth']
					row[f'{sample}_GQ'] = var.genotypes[sample]['genotype_quality']
					
				for info_annotation in var.info_annotations:
					
					row[f'info_{info_annotation}'] = var.info_annotations[info_annotation]
					
				for transcript_annotation in transcript:
					
					row[f'csq_{transcript_annotation}'] = transcript[transcript_annotation]
				
				
				df_list.append(row)

		df = pd.DataFrame(df_list)

		return df



	def to_dict(self, add_inheritance=True,
				 lenient=False,
				 low_penetrance_genes={},
				 min_parental_gq_dn=10,
				 min_parental_depth_dn=10,
				 max_parental_alt_ref_ratio_dn=0.04,
				 min_parental_gq_upi=10,
				 min_parental_depth_upi=10,
				 get_picked=True):
		"""
		Convert variant_dict to a dict fro json processing

		Input: None

		Returns: Python Dict object.

		"""
		variant_set_dict = {}

		variant_set_dict['family'] = deepcopy(self.family.__dict__)

		member_list = []

		for member in variant_set_dict['family']['family_members']:
			member_list.append(deepcopy(member.__dict__))

		variant_set_dict['family']['family_members'] = deepcopy(member_list)

		variant_set_dict['variants'] = []

		for variant in self.variant_dict:

			var = self.variant_dict[variant]

			individual_variant_dict = {}

			individual_variant_dict['chromosome'] = var.chrom
			individual_variant_dict['position'] = var.pos
			individual_variant_dict['ref'] = var.ref
			individual_variant_dict['alt'] = var.alt
			individual_variant_dict['filter_status'] = '|'.join(var.filter_status)

			individual_variant_dict['worst_consequence'] = var.get_worst_consequence()

			individual_variant_dict['all_genes'] = '|'.join(list(set(var.get_genes(feature_key='SYMBOL'))))

			if add_inheritance == True:

				individual_variant_dict['inheritance_models'] = '|'.join(var.get_matching_inheritance_models(compound_het_dict= self.final_compound_hets,
																							lenient=lenient,
																							min_parental_gq_dn=min_parental_gq_dn,
																							min_parental_depth_dn =min_parental_depth_dn,
																							max_parental_alt_ref_ratio_dn= max_parental_alt_ref_ratio_dn,
																							min_parental_gq_upi = min_parental_gq_upi,
																							min_parental_depth_upi = min_parental_depth_upi
																							))

			individual_variant_dict['info_annotations'] = deepcopy(var.info_annotations)

			individual_variant_dict['transcript_annotations'] = deepcopy(var.transcript_annotations)

			if get_picked == True:

				individual_variant_dict['picked_transcript_annotations'] = []
				individual_variant_dict['extra_transcript_annotations'] = []

				for transcript in individual_variant_dict['transcript_annotations']:

					if transcript['PICK'] == '1':

						individual_variant_dict['picked_transcript_annotations'].append(transcript)

					else:

						individual_variant_dict['extra_transcript_annotations'].append(transcript)


			del individual_variant_dict['transcript_annotations']

			individual_variant_dict['genotypes'] = {}
		
			for sample in var.genotypes:

					individual_variant_dict['genotypes'][sample] ={}
					individual_variant_dict['genotypes'][sample]['genotype'] = '/'.join(var.genotypes[sample]['genotype'])
					individual_variant_dict['genotypes'][sample]['allele_depths'] = ','.join(str(x) for x in var.genotypes[sample]['allele_depths'])
					individual_variant_dict['genotypes'][sample]['depth'] = var.genotypes[sample]['depth']
					individual_variant_dict['genotypes'][sample]['genotype_quality'] = var.genotypes[sample]['genotype_quality']

			variant_set_dict['variants'].append(individual_variant_dict)

		return variant_set_dict





