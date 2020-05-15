from pyvariantfilter.family import Family
import statistics

class Variant:
	
	def __init__(self, chrom, pos, ref, alt, filter_status=None, quality=None):
		
		self.chrom = chrom
		self.pos = pos
		self.ref = ref
		self.alt = alt
		self.filter_status = filter_status
		self.quality = quality
		self.info_annotations = None
		self.transcript_annotations = None
		self.variant_id = f'{self.chrom}:{self.pos}{self.ref}>{self.alt}'
		self.family = None
		self.genotypes = {}

		self.is_valid()
			
	def __repr__(self):
		 return self.variant_id

	def is_valid(self):
		"""
		Check the newly constructed Variant is valid.

		Returns:

			None

		"""

		valid_chroms = {'1': None, '2': None, '3': None, '4': None,
		 '5': None, '6': None, '7': None, '8': None, '9': None,
		 '10': None, '11': None, '12': None, '13': None,
		 '14': None, '15': None, '16': None, '17': None,
		 '18': None, '19': None, '20': None, '21': None,
		 '22': None, 'X': None, 'Y': None, 'MT': None, 'M': None}

		# Chromosome is correct
		if self.chrom not in valid_chroms:

			raise ValueError(f'Chromosome not in {valid_chroms} for variant {self.variant_id}.')

		# Position must be an Integer
		if isinstance(self.pos, int) == False:

			raise ValueError('Position not an integer.')

		# ref and alt must be an Integer
		if isinstance(self.ref, str) == False or isinstance(self.alt, str) == False:

			raise ValueError('The Ref and Alt must be strings.')

		 
	def add_genotype(self, family_member_id, genotype, allele_depths, genome_quality, depth):
		"""
		Add a genotype to a Varaint object.

		Input:

			family_member_id: family_member_id from the FamilyMember object. (String)
			genotype: List of genotypes e.g ['A', 'T'] (List of Strings)
			allele_depths List of allele_depths - First item in list should be ref and second alt e.g. [10, 5] (List of Integers)
			genome_quality - The genome quality (GQ) score. Integer

		Returns:

			None
		"""

		assert isinstance(self.family, Family) == True
		assert family_member_id in self.family.get_all_family_member_ids()
		assert isinstance(genotype, list)
		assert len(genotype) == 2
		assert genotype[0] in [self.ref, self.alt, '.', '*']
		assert genotype[1] in [self.ref, self.alt, '.', '*']
		assert isinstance(allele_depths, list)
		assert len(allele_depths) == 2
		assert isinstance(allele_depths[0], int)
		assert isinstance(allele_depths[1], int)
		assert isinstance(depth, int)
		assert isinstance(genome_quality, int)

		self.genotypes[family_member_id] = {'genotype': genotype,
									'allele_depths': allele_depths,
									'genotype_quality': genome_quality,
									'depth': depth}
		  
	def add_family(self, family):
		"""
		Associate a family object with this variant.

		Input:

			family: Family object instance

		Returns:

			None
		
		"""
		assert isinstance(family, Family)
	
		self.family = family
		
	def get_genes(self, feature_key='Feature'):
		"""
		Get the genes associated with a variant.

		This function can be used to get any features associated with a variant by changing the feature_key.

		Input: feature_key - A key for each transcript in the self.transcript_annotations list

		Returns: genes - A list of all the features/genes in all transcripts.

		"""

		genes = []

		if self.transcript_annotations != None:

			for csq_dict in self.transcript_annotations:

				genes.append(csq_dict[feature_key])

		else:

			raise ValueError('No gene annotations present.')

		return genes
	
	def get_worst_consequence(self, consequence_severity=[
		'transcript_ablation', 
		'splice_acceptor_variant', 
		'splice_donor_variant', 
		'stop_gained', 
		'frameshift_variant',
		'stop_lost',
		'start_lost',
		'transcript_amplification',
		'inframe_insertion',
		'inframe_deletion',
		'missense_variant',
		'protein_altering_variant',
		'splice_region_variant',
		'incomplete_terminal_codon_variant',
		'start_retained_variant',
		'stop_retained_variant',
		'synonymous_variant',
		'coding_sequence_variant',
		'mature_miRNA_variant',
		'5_prime_UTR_variant',
		'3_prime_UTR_variant',
		'non_coding_transcript_exon_variant',
		'intron_variant',
		'NMD_transcript_variant',
		'non_coding_transcript_variant',
		'upstream_gene_variant',
		'downstream_gene_variant',
		'TFBS_ablation',
		'TFBS_amplification',
		'TF_binding_site_variant',
		'regulatory_region_ablation',
		'regulatory_region_amplification',
		'feature_elongation',
		'regulatory_region_variant',
		'feature_truncation',
		'intergenic_variant'], consequence_key='Consequence'):
		"""
		Get the worst consequence of all the transcripts in the self.transcript_annotations.

		The order of severity can be changed using the consequence_severity variable.

		Input:

		consequence_severity: list of consequences from worst to best.
		consequence_key: The key to use to look for the consequence. 
		


		"""
		
		if self.transcript_annotations == None:

			raise ValueError('No transcript annotations present.')

		else:

			consequences = []

			for csq_dict in self.transcript_annotations:

				if consequence_key not in csq_dict:

					raise ValueError(f'The consequence key ({consequence_key}) does not exist in the transcript annotations.')

				consequences.append(csq_dict[consequence_key])

			worst_index = 9999
			
			for consequence in consequences:
				
				if consequence == None:
					
					break
				
				split_consequences = consequence.split('&')
				
				for c in split_consequences:
				
					index = consequence_severity.index(c)
				
					if index < worst_index:
					
						worst_index = index
			
			if worst_index == 9999:
				
				return None
			
			else:
					
				return consequence_severity[worst_index]


		
	def is_hom_ref(self, family_member_id):
		"""
		Is a variant genotype homozygous reference?

		Input:

			family_member_id: family_member_id of a Family Member object.

		Returns:

			True: If family_member_id is homozygous reference for the variant.
			False: If family_member_id is not homozygous reference for the variant.

		"""
		
		gt = self.genotypes[family_member_id]['genotype']
		
		if gt.count(self.ref) == 2:
			
			return True
		
		else:
			
			return False
		
	def has_no_alt(self, family_member_id):
		"""
		Does the alt allele not exist in the genotype?

		Input:

			family_member_id: family_member_id of a Family Member object.

		Returns:

			True: If family_member_id does not have the alt allele.
			False: If family_member_id does have the alt allele.

		"""
		
		gt = self.genotypes[family_member_id]['genotype']
			
		if gt.count(self.alt) == 0:
			
			return True
		
		else:
			
			return False
		
	
	def is_het(self, family_member_id):
		"""
		Does the alt allele have a count of one in the genotype?

		Input:

			family_member_id: family_member_id of a Family Member object.

		Returns:

			True: If family_member_id has an alt count of one.
			False: If family_member_id does not have an alt count of one.

		"""
		
		gt = self.genotypes[family_member_id]['genotype']
		
		if gt.count(self.alt) == 1:
			
			return True
		
		else:
			
			return False
		
	def has_alt(self, family_member_id):
		"""
		Does the alt allele exist in the genotype?

		Input:

			family_member_id: family_member_id of a Family Member object.

		Returns:

			True: If family_member_id genotype has the alt.
			False: If family_member_id does not have the alt.

		"""
		
		gt = self.genotypes[family_member_id]['genotype']
		
		if gt.count(self.alt) == 0:
			
			return False
		
		else:
			
			return True
	
	def is_hom_alt(self, family_member_id):
		"""
		Does the alt allele have a count of two?

		Input:

			family_member_id: family_member_id of a Family Member object.

		Returns:

			True: If family_member_id genotype has an alt count of two.
			False: If family_member_id does not have an alt count of two.

		"""
		
		gt = self.genotypes[family_member_id]['genotype']
		
		if gt.count(self.alt) == 2:
			
			return True
		
		else:
			
			return False

	def is_homozygous(self, family_member_id):
		"""
		Is the family member homozygous for either the reference or alt allele?

		Input:

			family_member_id: family_member_id of a Family Member object.

		Returns:

			True: If family_member_id genotype has an allele count of 2 for either the reference or alt allele.
			False: If family_member_id genotype does not have an allele count of 2 for either the reference or alt allele.

		"""

		if self.is_hom_ref(family_member_id) == True:

			return True

		if self.is_hom_alt(family_member_id) == True:

			return True

		return False

	
	def is_missing(self, family_member_id):
		"""
		Are both alleles missing i.e ./. in VCF form.

		Input:

			family_member_id: family_member_id of a Family Member object.

		Returns:

			True: if the genotype is missing.
			False: if the genotype is not missing.

		"""
		
		gt = self.genotypes[family_member_id]['genotype']
		
		if gt.count('.') == 2:
			
			return True
		
		else:
			
			return False
		
	def is_mixed(self, family_member_id):
		"""
		Is one allele missing i.e 1/. in VCF form?

		Input:

			family_member_id: family_member_id of a Family Member object.

		Returns:

			True: if the genotype is mixed.
			False: if the genotype is not mixed.

		"""
		
		gt = self.genotypes[family_member_id]['genotype']
		
		if gt.count('.') == 1:
			
			return True
		
		else:
			
			return False
	
	def get_depth(self, family_member_id):
		"""
		Get the genotype depth for a family_member.

		Input:

			family_member_id: family_member_id of a Family Member object.

		Returns:

			ad: genotype depth

		"""
		
		ad = self.genotypes[family_member_id]['depth']
		
		return ad
	
	def get_genotype_quality(self, family_member_id):
		"""
		Get the genotype quality for a family_member.

		Input:

			family_member_id: family_member_id of a Family Member object.

		Returns:

			gq: genotype quality

		"""

		
		gq = self.genotypes[family_member_id]['genotype_quality']
		
		return gq
	
	def get_alt_reads(self, family_member_id):
		"""
		Get the alt read count for a family_member.

		Input:

			family_member_id: family_member_id of a Family Member object.

		Returns:

			ad: alt read count

		"""	
		ad = self.genotypes[family_member_id]['allele_depths']
		
		return ad[1]

	def get_ref_reads(self, family_member_id):
		"""
		Get the ref read count for a family_member.

		Input:

			family_member_id: family_member_id of a Family Member object.

		Returns:

			ad: ref read count

		"""	
		ad = self.genotypes[family_member_id]['allele_depths']
		
		return ad[0]
	
	def matches_autosomal_dominant(self, lenient=False, low_penetrance_genes={}):
		"""
		Does the variant match an autosomal dominant inheritance pattern?
				
		Input:

			lenient: (Boolean) - allow affected who are not the proband to be homozygous alternate
			low_penetrance_genes: (Dict) - Dictionary of low penetrance genes - \
			variants within genes in this dictionary are allowed to have unaffected  \
			people with the variant.

		Returns:

			True - If matches autosomal dominant inheritance pattern.
			False - If does not match autosomal dominant inheritance pattern.


		Rules:

			1) Variant must be on an autosome.
			2) All affected samples must be heterozygous or missing e.g. ./. See lenient option to allow homozygous alternate genotypes in affected samples other than the proband.
			3) If the variant is not in a low penetrant gene then all unaffected samples must be homozygous reference or have a missing genotype.

		"""

		if self.chrom in ['X', 'Y', 'MT', 'M']:
			
			return False
	
		
		# Check that all affected are het
		affected = self.family.get_affected_family_members()
		
		if lenient == False:
		
			for family_member_id in affected:

				if self.is_het(family_member_id) == False and self.is_missing(family_member_id) == False:

					return False
				
		else:
			
			# affected people who are not the proband are allowed to be hom alt
			for family_member_id in affected:
					
				if self.family.get_proband_id() != family_member_id:
					
					if self.has_alt(family_member_id) == False and self.is_missing(family_member_id) == False:

						return False
					
				else:
										
					if self.is_het(family_member_id) == False and self.is_missing(family_member_id) == False:

						return False

		check_unaffected = True

		if low_penetrance_genes:

			genes = self.get_genes(feature_key='SYMBOL')

			for gene in genes:

				if gene in low_penetrance_genes:

					check_unaffected = False
					break

		if check_unaffected == True:

			# Check that all unaffected are hom ref and not missing if they are return false
			unaffected = self.family.get_unaffected_family_members()
				
			for family_member_id in unaffected:
					
				if self.has_alt(family_member_id) == True:
						
					return False
				
		return True
		
	
	def matches_autosomal_reccessive(self):
		"""
		Does the variant match an autosomal reccessive inheritance pattern?   
		
		Input: Self

		Returns:

			True - If matches autosomal reccessive inheritance pattern.
			False - If does not match autosomal reccessive inheritance pattern.

		Rules:

		1) Variant must be on an Autosome.
		2) All affected samples must be homozygous for the alternate allele. Can be missing.
		3) No unaffected samples can be homozygous for the alternate allele. Can be missing.

		"""
		
		if self.chrom in ['X', 'Y', 'MT', 'M']:
			
			return False
		
		# Check that all affected are hom alt
		affected = self.family.get_affected_family_members()
		
		for family_member_id in affected:
					
			if self.is_hom_alt(family_member_id) == False and self.is_missing(family_member_id) == False:
									
				return False
		
		# Check that unaffected are not hom alt 
		unaffected = self.family.get_unaffected_family_members()
			
		for family_member_id in unaffected:
							
			if self.is_hom_alt(family_member_id) == True:
					
				return False      
			
		return True
		
	
	def matches_denovo(self, min_parental_gq=30, min_parental_depth=10, max_parental_alt_ref_ratio=0.04):
		"""
		Given a sample as a proband did the variant arise de novo?

		Input:

			min_parental_gq: int - Both parental genotypes must have a GQ value above this.
			min_parental_depth: int - Both parental genotypes must have a depth above this.
			max_parental_alt_ref_ratio: int - Parents cannot have an alt/ref ratio higher than this.

		Returns:

			True - If matches de novo inheritance pattern.
			False - If does not match de novo autosomal inheritance pattern. 

		Rules:

			1) Variant in proband and not in either parent.
			2) Parents must have a GQ value above min_parental_gq
			3) Parents must have a DP value above min_parental_depth
			4) Parents must have a alt/ref ratio below max_parental_alt_ref_ratio

		
		"""
		proband = self.family.get_proband()
		
		mum = proband.get_mum()
		dad = proband.get_dad()

		if self.has_alt(proband.get_id()):
			
			# Must have both parents to calculate
			if mum == None or dad == None:
				
				return False

			else:
			
				mum_id = mum.get_id()
				dad_id = dad.get_id()
				
				mum_gq = self.get_genotype_quality(mum_id)
				mum_dp = self.get_depth(mum_id)
				mum_alt = self.get_alt_reads(mum_id)
				mum_ref = self.get_ref_reads(mum_id)

				# no div by 0 - what if ads are 0,0
				if mum_ref == 0:

					mum_ad_ratio = 0

				else:

					mum_ad_ratio = mum_alt / mum_ref
				
				dad_gq = self.get_genotype_quality(dad_id)
				dad_dp = self.get_depth(dad_id)
				dad_alt = self.get_alt_reads(dad_id) 
				dad_ref = self.get_ref_reads(dad_id)

				# no div by 0
				if dad_ref == 0:

					dad_ad_ratio = 0

				else:

					dad_ad_ratio = dad_alt / dad_ref
				
				if (self.has_alt(mum_id) == False and 
					mum_gq >= min_parental_gq and 
					mum_dp >= min_parental_depth and 
					mum_ad_ratio <= max_parental_alt_ref_ratio and
					self.has_alt(dad_id) == False and
					dad_gq >= min_parental_gq and
					dad_dp >= min_parental_depth and
					dad_ad_ratio < max_parental_alt_ref_ratio):
					
					return True
				
				else:
					
					return False

		else:

			return False
		
	def matches_x_reccessive(self):
		"""
		Does the variant match an X reccessive inheritance pattern?
		
		Input: Self.

		Returns:

			True - If matches X reccessive inheritance pattern.
			False - If does not match X reccessive inheritance pattern. 

		Rules:

			1) Variant must be on the X chromosome.
			2) All affected female samples must be hom_alt or missing.
			3) No unaffected female samples can be hom_alt.
			4) All affected male samples must have the variant or be missing.
			5) No unaffected male samples can have the variant.

		"""
		
		if self.chrom != 'X':
			
			return False
		
		affected_females = self.family.get_affected_female_members()
		
		for family_member_id in affected_females:
			
			if self.is_hom_alt(family_member_id) == False and self.is_missing(family_member_id) == False:
				
				return False
			
			
		unaffected_females = self.family.get_unaffected_female_members()
		
		for family_member_id in unaffected_females:
			
			if self.is_hom_alt(family_member_id) == True:
				
				return False
	
	
		affected_males = self.family.get_affected_male_members()
		
		for family_member_id in affected_males:
			
			if self.is_hom_ref(family_member_id) == True and self.is_missing(family_member_id) == False:
				
				return False    
	
		unaffected_males = self.family.get_unaffected_male_members()
		
		for family_member_id in unaffected_males:
			
			if self.has_alt(family_member_id) == True:
				
				return False 
			
		return True
	

	def matches_x_dominant(self):
		"""
		Does the variant match an X dominant inheritance pattern?
		
		Input: Self.

		Returns:

			True - If matches X dominant inheritance pattern.
			False - If does not match X dominant inheritance pattern. 

		Rules:

			1) Variant must be on the X chromosome.
			2) The daughters of affected male samples must be affected.
			3) The sons of affected males must not be affected.
			4) Affected male samples must have the variant or be missing.
			5) Affected female samples must be heterozygous or missing.
			6) Unaffected samples must not have the variant.

		"""
		
		# Must be on X chromosome
		if self.chrom != 'X':
			
			return False 
		
		# Check affected males children,
		affected_males = self.family.get_affected_male_members()	
		for family_member_id in affected_males:
			
			# if an affected male has unaffected daughters then no match
			daughters = self.family.get_daughters(family_member_id)
			
			for daughter in daughters:
				
				if daughter.affected == False:
					
					return False
			
			# if an affected male has an affected son then no match
			sons = self.family.get_sons(family_member_id)
			
			for son in sons:
				
				if son.affected == True:
					
					return False
		
		# Affected males must not be hom ref
		for family_member_id in affected_males:
			
			if self.is_hom_ref(family_member_id) == True and self.is_missing(family_member_id) == False :
					
					return False
		
		
		# Affected females must be het or missing.
		affected_females = self.family.get_affected_female_members()
		for family_member_id in affected_females:
			
			if self.is_het(family_member_id) == False and self.is_missing(family_member_id) == False:
				
				return False
			
		# Unaffected samples must not have the variant.
		unaffected = self.family.get_unaffected_family_members()
		for family_member_id in unaffected:
			
			if self.has_alt(family_member_id) == True:
				
				return False 
			
		return True
			
	def matches_uniparental_isodisomy(self, min_parental_gq=30, min_parental_depth=10):
		"""
		Does the variant match a uniparental_isodisomy pattern?
		
		Input:

			min_parental_gq: int - Both parental genotypes must have a GQ value above this.
			min_parental_depth: int - Both parental genotypes must have a depth above this.

		Returns:

			True - If matches uniparental_isodisomy pattern.
			False - If does not match uniparental_isodisomy pattern. 

		"""

		proband = self.family.get_proband()
		mum = proband.get_mum()
		dad = proband.get_dad()

		# Must have both parents to calculate
		if mum == None or dad == None:

			return False

		proband_id = proband.get_id()
		mum_id = mum.get_id()
		dad_id = dad.get_id()
		
		if self.chrom not in ['X', 'Y', 'MT', 'M']:

			if (self.is_hom_alt(proband_id) and (self.is_het(mum_id) and self.has_no_alt(dad_id)) and 
				self.get_depth(mum_id) >= min_parental_depth and self.get_depth(dad_id) >= min_parental_depth and
				self.get_genotype_quality(mum_id) >= min_parental_gq and self.get_genotype_quality(dad_id) >= min_parental_gq):

				return True

			if (self.is_hom_alt(proband_id) and (self.is_het(dad_id) and self.has_no_alt(mum_id)) and 
				self.get_depth(mum_id) >= min_parental_depth and self.get_depth(dad_id) >= min_parental_depth and
				self.get_genotype_quality(mum_id) >= min_parental_gq and self.get_genotype_quality(dad_id) >= min_parental_gq):

				return True


		elif self.is_on_autosome_or_xfemale() == True:

			if (self.is_hom_alt(proband_id) and (self.is_het(mum_id) and self.has_no_alt(dad_id)) and 
				self.get_depth(mum_id) >= min_parental_depth and self.get_depth(dad_id) >= min_parental_depth and
				self.get_genotype_quality(mum_id) >= min_parental_gq and self.get_genotype_quality(dad_id) >= min_parental_gq):

				return True

			if (self.is_hom_alt(proband_id) and (self.has_no_alt(mum_id) and self.has_no_alt(dad_id)) and 
				self.get_depth(mum_id) >= min_parental_depth and self.get_depth(dad_id) >= min_parental_depth and
				self.get_genotype_quality(mum_id) >= min_parental_gq and self.get_genotype_quality(dad_id) >= min_parental_gq):

				return True

		return False

	def matches_compound_het(self, compound_het_dict):
		"""
		Is the variant in the compound het dict?

		Input: compound_het_dict - A dictionary containing variants which are compound hets

		Returns:

			True - If variant is in dict.
			False - If variant not in dict.

		"""

		if self.variant_id in compound_het_dict:

			return True

		else:

			return False

	def matches_mitochrondrial(self):
		"""
		Is the variant on the mitochrondial chromosome?

		Input: self

		Returns:

			True - If variant is on mitochrondial chromosome.
			False - If variant is not on mitochrondial chromosome.

		"""

		if self.chrom =='MT' or self.chrom =='M':

			return True

	def matches_y(self):
		"""
		Is the variant on the Y chromosome?

		Input: self

		Returns:

			True - If variant is on Y chromosome.
			False - If variant is not on Y chromosome.

		"""

		if self.chrom == 'Y':

			return True

	def matches_inheritance_model(self,
								 models,
								 compound_het_dict,
								 lenient=False,
								 low_penetrance_genes={},
								 min_parental_gq_dn=30,
								 min_parental_depth_dn=10,
								 max_parental_alt_ref_ratio_dn=0.03,
								 min_parental_gq_upi=30,
								 min_parental_depth_upi=10):
		"""
		Does the variant match the inputted inheritiance patterns?

		Input:

		models: list of models - possibilities are:

		na - return true ragardless of model.
		autosomal_dominant
		autosomal_reccessive
		x_reccessive
		x_dominant
		de_novo
		uniparental_isodisomy
		mitochrondrial
		y_chrom

		compound_het_dict - Dictionary containing variants which are compound hets
		lenient - In the autosomal_dominant inhertiance pattern whether to allow affected other than the proband to be hom_alt as well as het.
		low_penetrance_genes -  In the autosomal_dominant inhertiance pattern gene symbols in this list will be treated as low penetrance and unaffected samples can have the variant.
		min_parental_gq_dn - Min parental genome quality score for de novo calculations
		min_parental_depth_dn - Min parental depth for de novo calculations
		min_parental_gq_upi - Min parental genome quality score for uniparental isodisomy calculations
		min_parental_depth_upi - Min parental depth for uniparental isodisomy calculations


		Returns:

		True - if the variant matches one of the inhertiance models in the models variable
		False - otherwise.
		"""

		if 'na' in models:

			return True

		if 'autosomal_dominant' in models:

			if self.matches_autosomal_dominant(lenient=lenient, low_penetrance_genes= low_penetrance_genes):

				return True

		if 'autosomal_reccessive' in models:

			if self.matches_autosomal_reccessive():

				return True

		if 'x_reccessive' in models:

			if self.matches_x_reccessive():

				return True

		if 'x_dominant' in models:

			if self.matches_x_dominant():

				return True

		if 'de_novo' in models:

			if self.matches_denovo(min_parental_gq=min_parental_gq_dn, min_parental_depth=min_parental_depth_dn, max_parental_alt_ref_ratio=max_parental_alt_ref_ratio_dn):

				return True

		if 'uniparental_isodisomy' in models:

			if self.matches_uniparental_isodisomy(min_parental_depth=min_parental_depth_upi, min_parental_gq=min_parental_gq_upi):

				return True

		if 'mitochrondrial' in models:

			if self.matches_mitochrondrial():

				return True

		if 'y_chrom' in models:

			if self.matches_y():

				return True

		if 'compound_het' in models:

			if self.matches_compound_het(compound_het_dict):

				return True

		return False

	def get_matching_inheritance_models(self, compound_het_dict, lenient=False, low_penetrance_genes={}, min_parental_gq_dn=30, min_parental_depth_dn=10, max_parental_alt_ref_ratio_dn=0.04, min_parental_gq_upi=30, min_parental_depth_upi=10):
		"""
		Return a list of all matching inheritance models.

		Input:

		models: list of models - possibilities are:
		autosomal_dominant
		autosomal_reccessive
		x_reccessive
		x_dominant
		de_novo
		uniparental_isodisomy
		mitochrondrial
		y_chrom

		compound_het_dict - Dictionary containing variants which are compound hets
		lenient - In the autosomal_dominant inhertiance pattern whether to allow affected other than the proband to be hom_alt as well as het.
		low_penetrance_genes -  In the autosomal_dominant inhertiance pattern gene symbols in this list will be treated as low penetrance and unaffected samples can have the variant.
		min_parental_gq_dn - Min parental genome quality score for de novo calculations
		min_parental_depth_dn - Min parental depth for de novo calculations
		min_parental_gq_upi - Min parental genome quality score for uniparental isodisomy calculations
		min_parental_depth_upi - Min parental depth for uniparental isodisomy calculations


		Returns:

		A list of all matching inheritance models.
		"""

		matching_models =[]

		if self.matches_autosomal_dominant(lenient=lenient, low_penetrance_genes= low_penetrance_genes):

			matching_models.append('autosomal_dominant')

		if self.matches_autosomal_reccessive():

			matching_models.append('autosomal_reccessive')

		if self.matches_x_reccessive():

			matching_models.append('x_reccessive')

		if self.matches_x_dominant():

			matching_models.append('x_dominant')

		if self.matches_denovo(min_parental_gq=min_parental_gq_dn, min_parental_depth=min_parental_depth_dn, max_parental_alt_ref_ratio=max_parental_alt_ref_ratio_dn):

			matching_models.append('de_novo')

		if self.matches_uniparental_isodisomy(min_parental_depth=min_parental_depth_upi, min_parental_gq=min_parental_gq_upi):

			matching_models.append('uniparental_isodisomy')

		if self.matches_mitochrondrial():

			matching_models.append('mitochrondrial')

		if self.matches_y():

			matching_models.append('y_chrom')

		if self.matches_compound_het(compound_het_dict):

			matching_models.append('compound_het')

		return matching_models



	def passes_gt_filter(self, family_member_id, min_dp=20, min_gq=30):
		"""
		Does the genotypes for a sample pass minimum depth and genotype quality requirements?

		Input:
		
		family_member_id: The family_member_id of the genotype the user wants to check
		min_dp: The minimum depth required to pass
		min_gq: The minimin genome quality required to pass.

		Returns:

		True - if the variant passes the filter
		False - otherwise.

		"""

		if self.get_depth(family_member_id) >= min_dp and self.get_genotype_quality(family_member_id) >= min_gq:

			return True

		return False


	def passes_filter(self):
		"""
		Does the variant pass the variant level filter?

		Input: self

		Returns:

		True - if the filter is PASS or None
		False - otherwise.

		"""

		if len(self.filter_status) == 1:

			if self.filter_status[0] == 'PASS' or self.filter_status[0] == None:

				return True


		return False

	def transcript_has_any(feature_key, value):
		"""
		Do any of the transcript annotations for feature_key qual the value?

		For example does the consequence for any transcript equal missense_variant?

		"""

		if self.transcript_annotations == None:

			return False

		for transcript in self.transcript_annotations:

			if transcript[feature_key] == value:

				return True

		return False


	
	def is_hom_alt_in_unaffected(self):
		"""
		Is the variant homozygous for the alt allele in unaffected samples?

		Input: self

		Returns:

		True - If the variant is homozygous alt in any unaffected sample
		False - Otherwise


		"""
		
		unaffected = self.family.get_unaffected_family_members()
		
		for family_member_id in unaffected:
			
			if self.is_hom_alt(family_member_id) == True:
				
				return True
			
		return False
	
	def is_on_autosome_or_xfemale(self):
		"""
		Is the variant on an autosome or on the x chromosome in a female sample.

		Applies to proband only.

		Input: self

		Returns:

			True - If the variant is on an autosome or on the x chromosome in a female
			False - otherwise


		"""
		
		proband = self.family.get_proband()
		
		if self.chrom not in ['X', 'Y', 'MT', 'M'] or (proband.sex == 2 and self.chrom =='X'):
		
			return True
		
		return False


	def add_transcript_annotations(self, transcript_annotations):
		"""
		Add a transcript annotation. This should be a list of dictionaries

		Input:
		
		transcript_annotations: A list of dictionaries containing transcript annotations.

		Returns:

		None

		"""

		assert isinstance(transcript_annotations, list)

		self.transcript_annotations = transcript_annotations

	def add_info_annotations(self, info_annotations):
		"""
		Add an info annotation. This should be a dictionary.

		Input:
		
		transcript_annotations: dictionary containing the info annotations.

		Returns:

		None

		"""

		assert isinstance(info_annotations, dict)

		self.info_annotations = info_annotations

	def get_numerical_transcript_annotation(self, annotation_key, zero_values=['.', '', None], agg_func='min'):
		"""
		Returns a numerical transcript annotation. If there are multiple values these can be aggregated using
		the add_func option.

		Input:
		
		annotation_key - A key to the numerical value in the self.transcript_annotations list of dicts
		zero_values - Values which should be changed to zero e.g. '.'
		agg_func - How to aggregate multiple values - possibilities = min, max, mean


		Returns:

		The numerical value as a float.
		"""

		annotations = []

		for transcript in self.transcript_annotations:

			annotation = transcript[annotation_key]

			if annotation in zero_values:

				annotations.append(0.0)

			elif '&' in annotation:

				annotation = annotation.split('&')

				for sub_annotation in annotation:

					if sub_annotation in zero_values:

						annotations.append(0.0)

					else:

						annotations.append(sub_annotation)


			else:

				annotations.append(annotation)

		annotations = [float(annotation) for annotation in annotations]

		if agg_func  == 'min':

			return min(annotations)

		elif agg_func == 'max':

			return max(annotations)

		elif agg_func == 'mean':

			return statistics.mean(annotations)

		else:

			raise ValueError('Invalid aggregation function supplied')


	def get_numerical_info_annotation(self, annotation_key, zero_values=['.', '', None], agg_func='min'):
		"""
		Returns a numerical info annotation. If there are multiple values these can be aggregated using
		the add_func option.

		Input:
		
		annotation_key - A key to the numerical value in the self.transcript_annotations list of dicts
		zero_values - Values which should be changed to zero e.g. '.'
		agg_func - How to aggregate multiple values - possibilities = min, max, mean


		Returns:

		The numerical value as a float.
		"""

		annotations = []

		annotation = self.info_annotations[annotation_key]

		if annotation in zero_values:

			annotations.append(0.0)

		elif isinstance(annotation, str):

			if '&' in annotation:

				annotation = annotation.split('&')

				for sub_annotation in annotation:

					if sub_annotation in zero_values:

						annotations.append(0.0)

					else:

						annotations.append(sub_annotation)

			else:

				annotations.append(annotation)

		else:

			annotations.append(annotation)

		annotations = [float(annotation) for annotation in annotations]

		if agg_func  == 'min':

			return min(annotations)

		elif agg_func == 'max':

			return max(annotations)

		elif agg_func == 'mean':

			return statistics.mean(annotations)

		else:

			raise ValueError('Invalid aggregation function supplied')


	def filter_on_numerical_transcript_annotation_gte(self,
												 annotation_key,
												 ad_het,
												 ad_hom_alt,
												 x_male,
												 x_female_het,
												 x_female_hom,
												 compound_het,
												 y,
												 mt,
												 zero_values=['.', '', None],
												 agg_func='min',
												 compound_het_dict = {}):

		"""
		Filter on a numerical value. Is the value is larger or equal to the provided value?

		Different values can be provided for different variant types. For example we can provide different 
		values for ad_het (autosomal heterozygous) and x_male (variants on x chromsome in men).

		Uses the genotype of whichever sample is set as the proband.

		Input:

			annotation_key - which annotation in the self.transcript_annotations list of dictionaries to get
			ad_het - the value to filter on for variants in which the proband is heterozygouse on an autosome.
			ad_hom_alt - the value to filter on for variants in which the proband is homozygous alt on an autosome.
			x_male - the value to filter on for variants on the X chromsome in which the proband is male.  
			x_female_het - the value to filter on for heterozygous variants on the X chromsome in which the proband is female. 
			x_female_hom - the value to filter on for homozygous variants on the X chromsome in which the proband is female.
			compound_het - the value to filter on if the variant is a compound het.
			y - the value to filter on if the variant is on the Y chromosome.
			mt - teh value to filter on if the variant is on the Mitochondrial chromosome.
			zero_values - list of values which should be considered as 0 in the annotation.
			agg_func - how to aggregate multiple values - min, max, mean
			compound_het_dict - A dictionary of variants which are compound hets.

		Returns:

			True - if the variant has a value above the supplied value
			False - otherwise.

		"""


		annotation = self.get_numerical_transcript_annotation(annotation_key, zero_values, agg_func)
		proband = self.family.get_proband()
		proband_id = proband.get_id()


		if self.variant_id in compound_het_dict:

			if annotation >= compound_het:

					return True

			else:

				return False


		if self.chrom not in ['X', 'Y', 'MT', 'M'] and self.is_het(proband_id):

			if annotation >= ad_het:

				return True

			else:

				return False

		elif self.chrom not in ['X', 'Y', 'MT', 'M'] and self.is_hom_alt(proband_id):

			if annotation >= ad_hom_alt:

				return True

			else:

				return False

		elif self.chrom == 'X' and proband.sex == 1 and self.has_alt(proband_id):

			if annotation >= x_male:

				return True

			else:

				return False	

		elif self.chrom == 'X' and proband.sex == 2 and self.is_het(proband_id):

			if annotation >= x_female_het:

				return True

			else:

				return False	

		elif self.chrom == 'X' and proband.sex == 2 and self.is_hom_alt(proband_id):

			if annotation >= x_female_hom:

				return True

			else:

				return False

		elif self.chrom =='Y':

			if annotation >= y:

				return True

			else:

				return False

		elif self.chrom =='MT' or self.chrom =='M':

			if annotation >= mt:

				return True

			else:

				return False

		else:

			raise ValueError('Variant does not have a a recognised workflow - is the proband homozygous reference?')

	def filter_on_numerical_info_annotation_gte(self,
													 annotation_key,
													 ad_het,
													 ad_hom_alt,
													 x_male,
													 x_female_het,
													 x_female_hom,
													 compound_het,
													 y,
													 mt,
													 zero_values=['.', '', None],
													 agg_func='min',
													 compound_het_dict = {}):

			"""
			Filter on a numerical value. Is the value is larger or equal to the provided value?

			Different values can be provided for different variant types. For example we can provide different 
			values for ad_het (autosomal heterozygous) and x_male (variants on x chromsome in men).

			Uses the genotype of whichever sample is set as the proband.

			Input:

				annotation_key - which annotation in the self.info list of dictionaries to get
				ad_het - the value to filter on for variants in which the proband is heterozygouse on an autosome.
				ad_hom_alt - the value to filter on for variants in which the proband is homozygous alt on an autosome.
				x_male - the value to filter on for variants on the X chromsome in which the proband is male.  
				x_female_het - the value to filter on for heterozygous variants on the X chromsome in which the proband is female. 
				x_female_hom - the value to filter on for homozygous variants on the X chromsome in which the proband is female.
				compound_het - the value to filter on if the variant is a compound het.
				y - the value to filter on if the variant is on the Y chromosome.
				mt - teh value to filter on if the variant is on the Mitochondrial chromosome.
				zero_values - list of values which should be considered as 0 in the annotation.
				agg_func - how to aggregate multiple values - min, max, mean
				compound_het_dict - A dictionary of variants which are compound hets.

			Returns:

				True - if the variant has a value above the supplied value
				False - otherwise.

			"""


			annotation = self.get_numerical_info_annotation(annotation_key, zero_values, agg_func)
			proband = self.family.get_proband()
			proband_id = proband.get_id()


			if self.variant_id in compound_het_dict:

				if annotation >= compound_het:

						return True

				else:

					return False


			if self.chrom not in ['X', 'Y', 'MT', 'M'] and self.is_het(proband_id):

				if annotation >= ad_het:

					return True

				else:

					return False

			elif self.chrom not in ['X', 'Y', 'MT', 'M'] and self.is_hom_alt(proband_id):

				if annotation >= ad_hom_alt:

					return True

				else:

					return False

			elif self.chrom == 'X' and proband.sex == 1 and self.has_alt(proband_id):

				if annotation >= x_male:

					return True

				else:

					return False	

			elif self.chrom == 'X' and proband.sex == 2 and self.is_het(proband_id):

				if annotation >= x_female_het:

					return True

				else:

					return False	

			elif self.chrom == 'X' and proband.sex == 2 and self.is_hom_alt(proband_id):

				if annotation >= x_female_hom:

					return True

				else:

					return False

			elif self.chrom =='Y':

				if annotation >= y:

					return True

				else:

					return False

			elif self.chrom =='MT' or self.chrom =='M':

				if annotation >= mt:

					return True

				else:

					return False

			else:

				raise ValueError('Variant does not have a a recognised workflow - is the proband homozygous reference?')

	def filter_on_numerical_transcript_annotation_lte(self,
												 annotation_key,
												 ad_het,
												 ad_hom_alt,
												 x_male,
												 x_female_het,
												 x_female_hom,
												 compound_het,
												 y,
												 mt,
												 zero_values=['.', '', None],
												 agg_func='min',
												 compound_het_dict = {}):
		"""
		Filter on a numerical value. Is the value is less than or equal to the provided value?

		Different values can be provided for different variant types. For example we can provide different 
		values for ad_het (autosomal heterozygous) and x_male (variants on x chromsome in men).

		Uses the genotype of whichever sample is set as the proband.

		Input:

			annotation_key - which annotation in the self.transcript_annotations list of dictionaries to get
			ad_het - the value to filter on for variants in which the proband is heterozygouse on an autosome.
			ad_hom_alt - the value to filter on for variants in which the proband is homozygous alt on an autosome.
			x_male - the value to filter on for variants on the X chromsome in which the proband is male.  
			x_female_het - the value to filter on for heterozygous variants on the X chromsome in which the proband is female. 
			x_female_hom - the value to filter on for homozygous variants on the X chromsome in which the proband is female.
			compound_het - the value to filter on if the variant is a compound het.
			y - the value to filter on if the variant is on the Y chromosome.
			mt - teh value to filter on if the variant is on the Mitochondrial chromosome.
			zero_values - list of values which should be considered as 0 in the annotation.
			agg_func - how to aggregate multiple values - min, max, mean
			compound_het_dict - A dictionary of variants which are compound hets.

		Returns:

			True - if the variant has a value below the supplied value
			False - otherwise.

		"""


		annotation = self.get_numerical_transcript_annotation(annotation_key, zero_values, agg_func)
		proband = self.family.get_proband()
		proband_id = proband.get_id()

		if self.variant_id in compound_het_dict:

			if annotation <= compound_het:

				return True

			else:

				return False

		elif self.chrom not in ['X', 'Y', 'MT', 'M'] and self.is_het(proband_id):

			if annotation <= ad_het:

				return True

			else:

				return False

		elif self.chrom not in ['X', 'Y', 'MT', 'M'] and self.is_hom_alt(proband_id):

			if annotation <= ad_hom_alt:

				return True

			else:

				return False

		elif self.chrom == 'X' and proband.sex == 1 and self.has_alt(proband_id):

			if annotation <= x_male:

				return True

			else:

				return False	

		elif self.chrom == 'X' and proband.sex == 2 and self.is_het(proband_id):

			if annotation <= x_female_het:

				return True

			else:

				return False	

		elif self.chrom == 'X' and proband.sex == 2 and self.is_hom_alt(proband_id):

			if annotation <= x_female_hom:

				return True

			else:

				return False

		elif self.chrom =='Y':

			if annotation <= y:

				return True

			else:

				return False

		elif self.chrom =='MT' or self.chrom == 'M':

			if annotation <= mt:

				return True

			else:

				return False

		else:

			raise ValueError('Variant does not have a a recognised workflow - is the proband homozygous reference?')


	def filter_on_numerical_info_annotation_lte(self,
													 annotation_key,
													 ad_het,
													 ad_hom_alt,
													 x_male,
													 x_female_het,
													 x_female_hom,
													 compound_het,
													 y,
													 mt,
													 zero_values=['.', '', None],
													 agg_func='min',
													 compound_het_dict = {}):
			"""
			Filter on a numerical value. Is the value is less than or equal to the provided value?

			Different values can be provided for different variant types. For example we can provide different 
			values for ad_het (autosomal heterozygous) and x_male (variants on x chromsome in men).

			Uses the genotype of whichever sample is set as the proband.

			Input:

				annotation_key - which annotation in the self.info dictionary to get
				ad_het - the value to filter on for variants in which the proband is heterozygouse on an autosome.
				ad_hom_alt - the value to filter on for variants in which the proband is homozygous alt on an autosome.
				x_male - the value to filter on for variants on the X chromsome in which the proband is male.  
				x_female_het - the value to filter on for heterozygous variants on the X chromsome in which the proband is female. 
				x_female_hom - the value to filter on for homozygous variants on the X chromsome in which the proband is female.
				compound_het - the value to filter on if the variant is a compound het.
				y - the value to filter on if the variant is on the Y chromosome.
				mt - teh value to filter on if the variant is on the Mitochondrial chromosome.
				zero_values - list of values which should be considered as 0 in the annotation.
				agg_func - how to aggregate multiple values - min, max, mean
				compound_het_dict - A dictionary of variants which are compound hets.

			Returns:

				True - if the variant has a value below the supplied value
				False - otherwise.

			"""


			annotation = self.get_numerical_info_annotation(annotation_key, zero_values, agg_func)
			proband = self.family.get_proband()
			proband_id = proband.get_id()

			if self.variant_id in compound_het_dict:

				if annotation <= compound_het:

					return True

				else:

					return False

			elif self.chrom not in ['X', 'Y', 'MT', 'M'] and self.is_het(proband_id):

				if annotation <= ad_het:

					return True

				else:

					return False

			elif self.chrom not in ['X', 'Y', 'MT', 'M'] and self.is_hom_alt(proband_id):

				if annotation <= ad_hom_alt:

					return True

				else:

					return False

			elif self.chrom == 'X' and proband.sex == 1 and self.has_alt(proband_id):

				if annotation <= x_male:

					return True

				else:

					return False	

			elif self.chrom == 'X' and proband.sex == 2 and self.is_het(proband_id):

				if annotation <= x_female_het:

					return True

				else:

					return False	

			elif self.chrom == 'X' and proband.sex == 2 and self.is_hom_alt(proband_id):

				if annotation <= x_female_hom:

					return True

				else:

					return False

			elif self.chrom =='Y':

				if annotation <= y:

					return True

				else:

					return False

			elif self.chrom =='MT' or self.chrom == 'M':

				if annotation <= mt:

					return True

				else:

					return False

			else:

				raise ValueError('Variant does not have a a recognised workflow - is the proband homozygous reference?')


	def matches_paternal_uniparental_ambiguous(self,  min_parental_gq=30, min_parental_depth=10):
		"""
		A type of mendelian error symptomatic of a UPD event.

		Where the dad has allele AA and mum BB and child has AA

		This could happen from either a heterodisomic or isodisomic event

		"""

		proband = self.family.get_proband()
		
		mum = proband.get_mum()
		dad = proband.get_dad()

		# Must have both parents to calculate
		if mum == None or dad == None:
				
			return False

		mum_id = mum.get_id()
		dad_id = dad.get_id()
		proband_id = proband.get_id()

		mum_gq = self.get_genotype_quality(mum_id)
		mum_dp = self.get_depth(mum_id)
		dad_gq = self.get_genotype_quality(dad_id)
		dad_dp = self.get_depth(dad_id)

		# dad must be homozygous and mum must be homozygous for other allele and child homozygouse for same allele as dad


		if (self.is_hom_ref(dad_id) and
			self.is_hom_alt(mum_id) and 
			self.is_hom_ref(proband_id) and
			mum_gq >= min_parental_gq and
			mum_dp >= min_parental_depth and
			dad_gq >= min_parental_gq and
			dad_dp >= min_parental_depth):
			return True

		if (self.is_hom_alt(dad_id) and
			self.is_hom_ref(mum_id) and 
			self.is_hom_alt(proband_id) and
			mum_gq >= min_parental_gq and
			mum_dp >= min_parental_depth and
			dad_gq >= min_parental_gq and
			dad_dp >= min_parental_depth):
			return True 

		return False


	def matches_maternal_uniparental_ambiguous(self,  min_parental_gq=30, min_parental_depth=10):
		"""
		A type of mendelian error symptomatic of a UPD event.

		Where the dad has allele AA and mum BB and child has AA

		This could happen from either a heterodisomic or isodisomic event

		"""

		proband = self.family.get_proband()
		
		mum = proband.get_mum()
		dad = proband.get_dad()

		# Must have both parents to calculate
		if mum == None or dad == None:
				
			return False

		mum_id = mum.get_id()
		dad_id = dad.get_id()
		proband_id = proband.get_id()

		mum_gq = self.get_genotype_quality(mum_id)
		mum_dp = self.get_depth(mum_id)
		dad_gq = self.get_genotype_quality(dad_id)
		dad_dp = self.get_depth(dad_id)

		# dad must be homozygous and mum must be homozygous for other allele and child homozygouse for same allele as dad


		if (self.is_hom_ref(mum_id) and
			self.is_hom_alt(dad_id) and 
			self.is_hom_ref(proband_id) and
			mum_gq >= min_parental_gq and
			mum_dp >= min_parental_depth and
			dad_gq >= min_parental_gq and
			dad_dp >= min_parental_depth):
			return True

		if (self.is_hom_alt(mum_id) and
			self.is_hom_ref(dad_id) and 
			self.is_hom_alt(proband_id) and
			mum_gq >= min_parental_gq and
			mum_dp >= min_parental_depth and
			dad_gq >= min_parental_gq and
			dad_dp >= min_parental_depth):
			return True 

		return False

	def matches_paternal_uniparental_isodisomy(self,  min_parental_gq=30, min_parental_depth=10):

		proband = self.family.get_proband()
		
		mum = proband.get_mum()
		dad = proband.get_dad()

		# Must have both parents to calculate
		if mum == None or dad == None:
				
			return False

		mum_id = mum.get_id()
		dad_id = dad.get_id()
		proband_id = proband.get_id()

		mum_gq = self.get_genotype_quality(mum_id)
		mum_dp = self.get_depth(mum_id)
		dad_gq = self.get_genotype_quality(dad_id)
		dad_dp = self.get_depth(dad_id)

		# mum homozygous ref dad het and kid homozygous for alt
		if (self.is_hom_ref(mum_id) and 
			self.is_het(dad_id) and 
			self.is_hom_alt(proband_id) and
			mum_gq >= min_parental_gq and
			mum_dp >= min_parental_depth and
			dad_gq >= min_parental_gq and
			dad_dp >= min_parental_depth):

			return True

		# mum homozygous alt dad het and kid homozygous for ref
		if (self.is_hom_alt(mum_id) and 
			self.is_het(dad_id) and 
			self.is_hom_ref(proband_id) and
			mum_gq >= min_parental_gq and
			mum_dp >= min_parental_depth and
			dad_gq >= min_parental_gq and
			dad_dp >= min_parental_depth):

			return True

		return False


	def matches_maternal_uniparental_isodisomy(self,  min_parental_gq=30, min_parental_depth=10):

		proband = self.family.get_proband()
		
		mum = proband.get_mum()
		dad = proband.get_dad()

		# Must have both parents to calculate
		if mum == None or dad == None:
				
			return False

		mum_id = mum.get_id()
		dad_id = dad.get_id()
		proband_id = proband.get_id()

		mum_gq = self.get_genotype_quality(mum_id)
		mum_dp = self.get_depth(mum_id)
		dad_gq = self.get_genotype_quality(dad_id)
		dad_dp = self.get_depth(dad_id)

		# mum homozygous ref dad het and kid homozygous for alt
		if (self.is_hom_ref(dad_id) and 
			self.is_het(mum_id) and 
			self.is_hom_alt(proband_id) and
			mum_gq >= min_parental_gq and
			mum_dp >= min_parental_depth and
			dad_gq >= min_parental_gq and
			dad_dp >= min_parental_depth):

			return True

		# mum homozygous alt dad het and kid homozygous for ref
		if (self.is_hom_alt(dad_id) and 
			self.is_het(mum_id) and 
			self.is_hom_ref(proband_id) and
			mum_gq >= min_parental_gq and
			mum_dp >= min_parental_depth and
			dad_gq >= min_parental_gq and
			dad_dp >= min_parental_depth):

			return True

		return False


	def alleles_identical_to_dad(self, min_parental_gq=30, min_parental_depth=10):
		"""
		Does the proband have identical alleles to dad?

		"""

		proband = self.family.get_proband()
		
		mum = proband.get_mum()
		dad = proband.get_dad()

		# Must have both parents to calculate
		if mum == None or dad == None:
				
			return False

		mum_id = mum.get_id()
		dad_id = dad.get_id()
		proband_id = proband.get_id()

		if self.is_missing(proband_id) or self.is_missing(dad_id):

			return False

		dad_gq = self.get_genotype_quality(dad_id)
		dad_dp = self.get_depth(dad_id)

		gt_proband = self.genotypes[proband_id]['genotype']
		gt_dad = self.genotypes[dad_id]['genotype']

		if (set(gt_proband) == set(gt_dad) and 
			dad_gq >= min_parental_gq and
			dad_dp >= min_parental_depth):

			return True

		return False

	def alleles_identical_to_mum(self, min_parental_gq=30, min_parental_depth=10):
		"""
		Does the proband have identical alleles to mum?

		"""

		proband = self.family.get_proband()
		
		mum = proband.get_mum()
		dad = proband.get_dad()

		# Must have both parents to calculate
		if mum == None or dad == None:
				
			return False

		mum_id = mum.get_id()
		dad_id = dad.get_id()
		proband_id = proband.get_id()

		if self.is_missing(proband_id) or self.is_missing(mum_id):

			return False

		mum_gq = self.get_genotype_quality(mum_id)
		mum_dp = self.get_depth(mum_id)

		gt_proband = self.genotypes[proband_id]['genotype']
		gt_mum = self.genotypes[mum_id]['genotype']

		if (set(gt_proband) == set(gt_mum) and 
			mum_gq >= min_parental_gq and
			mum_dp >= min_parental_depth):

			return True

		return False

	def is_snp(self):
		"""
		Is the variant a simple snp with a ref and alt length of 1?
		"""

		if len(self.ref) == 1 and len(self.alt) == 1:

			return True

		return False


	def all_samples_pass_genotype_quality(self , min_dp=10, min_gq=20):
		"""
		Check all sample genotypes are not missing and have depths and gqs above the minimum.
		"""

		for sample_id in self.family.get_all_family_member_ids():

			gq = self.get_genotype_quality(sample_id)
			dp = self.get_depth(sample_id)

			if dp < min_dp:

				return False

			if gq < min_gq:

				return False

			if self.is_missing(sample_id) == True:

				return False

		return True

	def get_quality(self):
		"""	
		Return the quality
		"""

		return self.quality


	def is_biparental_inheritance(self, min_parental_gq=30, min_parental_depth=10):
		"""
		Is the site one in which the proband inherits a different allele from each parent?

		Or at least a site where this is provable who transmits what!

		Can be used to rule out UPD across a region

		"""

		proband = self.family.get_proband()
		
		mum = proband.get_mum()
		dad = proband.get_dad()

		# Must have both parents to calculate
		if mum == None or dad == None:
				
			return False

		mum_id = mum.get_id()
		dad_id = dad.get_id()
		proband_id = proband.get_id()

		mum_gq = self.get_genotype_quality(mum_id)
		mum_dp = self.get_depth(mum_id)

		dad_gq = self.get_genotype_quality(dad_id)
		dad_dp = self.get_depth(dad_id)

		if self.is_missing(proband_id) or self.is_missing(mum_id):

			return False

		# dad is hom for alt mum is hom for ref and kid is het

		if (self.is_hom_alt(dad_id) and 
			self.is_hom_ref(mum_id) and 
			self.is_het(proband_id) and
			mum_gq >= min_parental_gq and
			mum_dp >= min_parental_depth and
			dad_gq >= min_parental_gq and
			mum_dp >= min_parental_depth):

			return True

		# dad is hom for ref mum is hom for alt and kid is het
		if (self.is_hom_ref(dad_id) and 
			self.is_hom_alt(mum_id) and 
			self.is_het(proband_id) and
			mum_gq >= min_parental_gq and
			mum_dp >= min_parental_depth and
			dad_gq >= min_parental_gq and
			mum_dp >= min_parental_depth):

			return True	

		return False