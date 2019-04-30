from pyvariantfilter.family_member import FamilyMember
import csv

class Family:
	"""
	A Family class for holding information



	"""
	
	def __init__(self, family_id):
		
		self.family_id = family_id
		self.family_members = []
		
	def __repr__(self):
		 return self.family_id
		
	def add_family_member(self, family_member):
		"""
		Add a FamilyMember to an Family.

		Input:

			family_member(FamilyMember :  Parents must already be family_members.

		Returns:

			None

		"""
		assert isinstance(family_member, FamilyMember)

		all_family_members = self.get_all_family_member_ids()

		if family_member.dad != None:

			if family_member.dad.get_id() not in all_family_members:

				raise ValueError(f'{family_member.get_id()} not in Family.')

		if family_member.mum != None:

			if family_member.mum.get_id()  not in all_family_members:

				raise ValueError(f'{family_member.get_id()} not in Family.')

		for existing_member in self.family_members:
			
			if family_member.family_member_id == existing_member.family_member_id:
				
				raise ValueError(f'Family member ({family_member.family_member_id}) already in Family.')
		
		self.family_members.append(family_member)
		
	def get_affected_family_members(self):
		"""
		Return those family members who are affected.

		Input: Self

		Returns:

			list: List of affected family member ids.
		"""
		
		return [family_member.get_id() for family_member in self.family_members if family_member.affected == True]
	
	def get_unaffected_family_members(self):
		"""
		Return those family members who are unaffected.

		Input: Self

		Returns:

			list: List of unaffected family member ids.
		"""
		
		return [family_member.get_id() for family_member in self.family_members if family_member.affected == False]
	
	def get_male_family_members(self):
		"""
		Return Male (1) family members.

		Input: Self

		Returns:

			list: List of Male (1) family member ids.

		"""
		return [family_member.get_id() for family_member in self.family_members if family_member.sex == 1]
	
	def get_female_family_members(self):
		"""
		Return Female (2) family members.

		Input: Self

		Returns:

			list: List of Male (2) family member ids.

		"""
		return [family_member.get_id() for family_member in self.family_members if family_member.sex == 2]
	
	def get_all_family_members(self):
		"""
		Return all family members objects in the family.

		Input: Self

		Returns:

			list: List of FamilyMember objects in the family.

		"""
		
		return self.family_members

	def get_all_family_member_ids(self):
		"""
		Returns the ids of all FamilyMember objects in the family.

		Input: Self

		Returns:

			list: List of all FamilyMember ids in the family.

		"""
		
		return [family_member.get_id() for family_member in self.get_all_family_members()]
	
	def set_proband(self, family_member_id):
		"""
		Set a specific sample as the proband.

		Input:

			family_member_id (String) : The family_member_id attribute of a FamilyMember within the family.

		Returns:

			None

		"""

		
		for existing_member in self.family_members:
			
			# Remove existing proband attribute
			existing_member.proband = False
			
			if existing_member.get_id() == family_member_id:

				assert existing_member.affected == True
				
				existing_member.proband = True
				
				return
		
		# If the user tries to assign a FamilyMember not in the family.
		raise ValueError(f'No Family Member with id: {family_member_id}')
		
	def get_proband(self):
		"""
		Return the proband within the Family. Only one sample can be the proband.

		Input: Self

		Returns:

			proband (FamilyMember): The FamilyMember object instance of the proband in the Family.

		"""
		
		probands = [family_member for family_member in self.family_members if family_member.proband == True]

		assert len(probands) == 1

		return probands[0]


	def proband_has_both_parents(self):
		"""
		Return whether the proband has both parents availible?

		Input: Self

		Returns:

			True - If proband has a mum and dad
			False - Otherwise.

		"""

		proband = self.get_proband()

		if proband.mum != None and proband.dad != None:

			return True

		return False


	def get_proband_id(self):
		"""
		Return the family_member_id within the Family. Only one sample can be the proband.

		Input: Self

		Returns:

			family_member_id (String): The FamilyMember object instance of the proband in the Family.

		"""
		
		probands = [family_member for family_member in self.family_members if family_member.proband == True]

		assert len(probands) == 1

		return probands[0].get_id()
	
	def get_affected_female_members(self):
		"""
		Returns all affected Female (2) members of the Family.

		Input: Self

		Returns:

			list: A list containing the family_member_ids of the affected Female members of the Family.

		"""
		return [family_member.get_id() for family_member in self.family_members if family_member.sex == 2 and family_member.affected == True]
	
	def get_unaffected_female_members(self):
		"""
		Returns all unaffected Female (2) members of the Family.

		Input: Self

		Returns:

			list: A list containing the family_member_ids of the unaffected Female members of the Family.

		"""
		return [family_member.get_id() for family_member in self.family_members if family_member.sex == 2 and family_member.affected == False]
	
	def get_affected_male_members(self):
		"""
		Returns all affected Male (1) members of the Family.

		Input: Self

		Returns:

			list: A list containing the family_member_ids of the affected Memale members of the Family.

		"""
		
		return [family_member.get_id() for family_member in self.family_members if family_member.sex == 1 and family_member.affected == True]
	
	def get_unaffected_male_members(self):
		"""
		Returns all unaffected Male (1) members of the Family.

		Input: Self

		Returns:

			list: A list containing the family_member_ids of the unaffected Memale members of the Family.

		"""
		
		return [family_member.get_id() for family_member in self.family_members if family_member.sex == 1 and family_member.affected == False]
	
	def get_daughters(self, family_member_id):
		"""
		Get the daughters of a FamilyMember object.

		Input:

			family_member_id (String): family_member_id of a FamilyMember object in the family.

		Returns:

			daughters (List) : List of daughter FamilyMember's  belonging to the FamilyMember object specified by family_member_id.

		"""
		
		daughters = []

		assert family_member_id in self.get_all_family_member_ids()
		
		for family_member in self.family_members: 
						
			if family_member.dad != None:
						
				if family_member.dad.get_id() == family_member_id and family_member.sex == 2:
				
					daughters.append(family_member)
					
			if family_member.mum != None:
								
				if family_member.mum.get_id() == family_member_id and family_member.sex == 2:
				
					daughters.append(family_member)           
				
		return daughters

	def get_daughter_ids(self, family_member_id):
		"""
		Get the daughters of a FamilyMember object.

		Input:

			family_member_id (String): family_member_id of a FamilyMember object in the family.

		Returns:

			daughters (list): List of daughter family_member_ids  belonging to the FamilyMember object specified by family_member_id.

		"""
		
		daughters = []

		assert family_member_id in self.get_all_family_member_ids()
		
		for family_member in self.family_members: 
						
			if family_member.dad != None:
						
				if family_member.dad.get_id() == family_member_id and family_member.sex == 2:
				
					daughters.append(family_member.get_id())
					
			if family_member.mum != None:
								
				if family_member.mum.get_id() == family_member_id and family_member.sex == 2:
				
					daughters.append(family_member.get_id())           
				
		return daughters

	
	def get_sons(self, family_member_id):
		"""
		Get the sons of a FamilyMember object.

		Input:

			family_member_id (String): family_member_id of a FamilyMember object in the family.

		Returns:

			sons (List): List of son family_member_ids belonging to the FamilyMember object specified by family_member_id.

		"""
		
		sons = []

		assert family_member_id in self.get_all_family_member_ids()
		
		for family_member in self.family_members: 
						
			if family_member.dad != None:
						
				if family_member.dad.get_id() == family_member_id and family_member.sex ==1:
				
					sons.append(family_member)
					
			if family_member.mum != None:
				
				if family_member.mum.get_id() == family_member_id and family_member.sex ==1:
				
					sons.append(family_member)           
				
		return sons

	def get_son_ids(self, family_member_id):
		"""
		Get the sons of a FamilyMember object.

		Input:

			family_member_id (String): family_member_id of a FamilyMember object in the family.

		Returns:

			sons (List) : List of son family_member_ids belonging to the FamilyMember object specified by family_member_id.

		"""
		
		sons = []

		assert family_member_id in self.get_all_family_member_ids()
		
		for family_member in self.family_members: 
						
			if family_member.dad != None:
						
				if family_member.dad.get_id() == family_member_id and family_member.sex ==1:
				
					sons.append(family_member.get_id())
					
			if family_member.mum != None:
				
				if family_member.mum.get_id() == family_member_id and family_member.sex ==1:
				
					sons.append(family_member.get_id())           
				
		return sons

	def read_from_ped_file(self, ped_file_path, family_id, proband_id):
		"""
		Populate a family object with information from a PED file.

		See https://gatkforums.broadinstitute.org/gatk/discussion/7696/pedigree-ped-files

		Input:

			ped_file_path (String): Path to the PED file.
			family_id (String): Family to extract from the PED file.
			proband_id (String): The ID of the sample in the PED file to set as the proband.

		Returns:

			None - Populates the Family object with PED information.

		"""

		family_dict = {}

		with open(ped_file_path, 'r') as csvfile:

			pedreader = csv.reader(csvfile, delimiter='\t')

			for row in pedreader:
 
				if row[0] == family_id:

					if row[5] == '2':

						affected = True

					elif row[5] == '1':

						affected = False

					new_family_member = FamilyMember(family_member_id=row[1],family_id=family_id, sex=int(row[4]), affected=affected)

					family_dict[new_family_member.get_id()] = new_family_member

					self.add_family_member(new_family_member)


		with open(ped_file_path, 'r') as csvfile:

			pedreader = csv.reader(csvfile, delimiter='\t')

			for row in pedreader:

				if row[2] in family_dict:

					family_dict[row[1]].dad = family_dict[row[2]]

				if row[3] in family_dict:

					family_dict[row[1]].mum = family_dict[row[3]]


		self.set_proband(proband_id)




