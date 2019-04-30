class FamilyMember:
	"""
	A FamilyMember Class. Stores the information for a specific member of the family.

	family_member_id: within Familt unique id (String)
	family_id: id for the Family the FamilyMember is within (String)
	sex: Sex (1 = Male, 2 = Female) (Integer)
	affected: Whether the family member is affected (Boolean)
	mum: Another FamilyMember instance which is the FamilyMember's mother.
	dad:  Another FamilyMember instance which is the FamilyMember's dad.
	proband: Whether the FamilyMember is the FamilyMember of interest in this family.

	"""
	
	def __init__(self, family_member_id, family_id, sex, affected, mum=None, dad=None, proband=False):
		
		self.family_member_id = family_member_id
		self.family_id = family_id
		self.sex = sex
		self.affected = affected
		self.mum = mum
		self.dad = dad
		self.proband = proband


		self.check_valid()
		
	def __repr__(self):
		 return self.family_member_id
		
	def get_id(self):
		"""
		Return the FamilyMember family_member_id

		Returns:

			family_member_id: family_member_id
		"""
		
		return self.family_member_id
	
	def get_mum(self):
		"""
		Return the FamilyMember mum attribute

		Returns:

			mum: mum
		"""
		
		return self.mum
	
	def get_dad(self):
		"""
		Return the FamilyMember dad attribute

		Returns:

			dad: dad
		"""
		
		return self.dad

	def check_valid(self):
		"""
		Checks the constructor inputs are valid.
		"""

		if self.sex not in [1,2]:

			raise ValueError(f'The sex of the family member must be either 1 (Male) or 2 (Female). The {self.family_id} object was {self.sex}')

		if self.affected not in [True, False]:

			raise ValueError(f'The affected status of the family member must be either True or False. The {self.family_id} object was {self.affected}')

		if isinstance(self.family_member_id, str) == False:

			raise ValueError(f'The family_member_id attribute must be a string.')

		if isinstance(self.family_id, str) == False:

			raise ValueError(f'The family_id attribute must be a string.')

		if self.mum != None:

			if isinstance(self.mum, FamilyMember) == False:

				raise ValueError(f'The mother must be a valid FamilyMember instance. You entered {self.mum}')

			if self.mum.sex != 2:

				raise ValueError(f'The mother must be female (2). You entered {self.mum.sex}')

			if self.mum.family_id != self.family_id:

				raise ValueError(f'The mother must have the same family_id as this object. The mother\'s family_id was {self.mum.family_id}')

			if self.mum.get_id() == self.get_id():

				raise ValueError(f'FamilyMember cannot be own mother.')

		if self.dad != None:

			if isinstance(self.dad, FamilyMember) == False:

				raise ValueError(f'The father must be a valid FamilyMember instance. You entered {self.dad}')

			if self.dad.sex != 1:

				raise ValueError(f'The mother must be female (2). You entered {self.dad.sex}')

			if self.dad.family_id != self.family_id:

				raise ValueError(f'The father must have the same family_id as this object. The father\'s family_id was {self.dad.family_id}')

			if self.dad.get_id() == self.get_id():

				raise ValueError(f'FamilyMember cannot be own father.')

		if self.proband == True and self.affected == False:

			raise ValueError(f'FamilyMember object cannot be the proband and be unaffected.')






