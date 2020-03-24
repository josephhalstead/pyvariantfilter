import unittest
from pyvariantfilter.family_member import FamilyMember
from pyvariantfilter.family import Family
from pyvariantfilter.variant import Variant
from pyvariantfilter.variant_set import VariantSet


class TestCreateFamilyMember(unittest.TestCase):
	"""
	Test the creation of family members
	"""

	def test_valid_creation(self):
		"""
		Test the simple creation of an object
		"""

		member = FamilyMember('mum', 'FAM001', 2, False)

		self.assertEqual(member.get_id(), 'mum')

	def test_invalid_sex(self):
		"""
		Test that the creation of an object with invalid sex value fails.
		"""

		try:

			member = FamilyMember('mum', 'FAM001', 3, False)
			self.fail()

		except ValueError:

			self.assertEqual(1,1)

	def test_invalid_affected(self):
		"""
		Test that the creation of an object with affected value fails.
		"""

		try:

			member = FamilyMember('mum', 'FAM001', 2, None)
			self.fail()

		except ValueError:

			self.assertEqual(1,1)


	def test_valid_parent_assigment(self):
		"""
		Test that we can assign parents to a family member

		"""

		
		mum = FamilyMember('mum', 'FAM001', 2, True)
		dad = FamilyMember('dad', 'FAM001', 1, True)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)

		self.assertEqual(proband.mum.get_id(), 'mum')
		self.assertEqual(proband.dad.get_id(), 'dad')

	def test_invalid_parent_family_id(self):
		"""
		Test that FamilyMember creation fails when parents have a different family id.
		"""

		try:
			mum = FamilyMember('mum', 'FAM001', 2, True)
			dad = FamilyMember('dad', 'FAM002', 1, True)
			proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)

		except ValueError:

			self.assertEqual(1,1)

	def test_invalid_parent_sex(self):
		"""
		Test that FamilyMember creation fails when parents have an invalid sex e.g. mum is male.
		"""

		try:
			mum = FamilyMember('mum', 'FAM001', 2, True)
			dad = FamilyMember('dad', 'FAM001', 2, True)
			proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)

		except ValueError:

			self.assertEqual(1,1)

	def test_invalid_proband(self):
		"""
		Test that FamilyMember creation fails when we set the proband to affected=False.

		"""

		try:
			proband = FamilyMember('proband', 'FAM001', 1, False, proband=True)
			self.fail()

		except ValueError:

			self.assertEqual(1,1)

	def test_cannot_be_own_mum(self):
		"""	
		Test that that FamilyMember creation fails when we try to set itself as mum.
		"""	

		try:
			mum = FamilyMember('mum', 'FAM001', 2, True)
			dad = FamilyMember('dad', 'FAM001', 2, True)
			proband = FamilyMember('proband', 'FAM001', 1, True, mum=proband, dad=dad)

		except UnboundLocalError:

			self.assertEqual(1,1)


class TestCreateFamily(unittest.TestCase):
	"""
	Test the creation of a family with one or more members.
	"""

	def test_valid_trio_creation(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)

		my_family = Family('FAM001')

		my_family.add_family_member(mum)
		my_family.add_family_member(dad)
		my_family.add_family_member(proband)


		my_family.set_proband(proband.get_id())

		self.assertCountEqual(my_family.get_affected_family_members(), ['proband'])
		self.assertCountEqual(my_family.get_unaffected_family_members(), ['mum', 'dad'])
		self.assertCountEqual(my_family.get_male_family_members(), ['proband', 'dad'])
		self.assertCountEqual(my_family.get_female_family_members(), ['mum'])
		self.assertCountEqual(my_family.get_all_family_member_ids(), ['proband', 'mum', 'dad'])
		self.assertEqual(my_family.get_proband().get_id(), 'proband')
		self.assertEqual(my_family.get_proband_id(), 'proband')
		self.assertCountEqual(my_family.get_affected_female_members(), [])
		self.assertCountEqual(my_family.get_unaffected_female_members(), ['mum'])
		self.assertCountEqual(my_family.get_affected_male_members(), ['proband'])
		self.assertCountEqual(my_family.get_unaffected_male_members(), ['dad'])
		self.assertCountEqual(my_family.get_daughter_ids('dad'), [])
		self.assertCountEqual(my_family.get_daughter_ids('mum'), [])
		self.assertCountEqual(my_family.get_son_ids('dad'), ['proband'])
		self.assertCountEqual(my_family.get_son_ids('mum'), ['proband'])


	def test_valid_multiple_affected(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		sibling = FamilyMember('sibling', 'FAM001', 1, True, mum=mum, dad=dad)

		my_family = Family('FAM001')

		my_family.add_family_member(mum)
		my_family.add_family_member(dad)
		my_family.add_family_member(proband)
		my_family.add_family_member(sibling)

		my_family.set_proband(proband.get_id())

		self.assertCountEqual(my_family.get_affected_family_members(), ['proband', 'sibling'])
		self.assertCountEqual(my_family.get_unaffected_family_members(), ['mum', 'dad'])
		self.assertCountEqual(my_family.get_male_family_members(), ['proband', 'dad', 'sibling'])
		self.assertCountEqual(my_family.get_female_family_members(), ['mum'])
		self.assertCountEqual(my_family.get_all_family_member_ids(), ['proband', 'mum', 'dad', 'sibling'])
		self.assertEqual(my_family.get_proband().get_id(), 'proband')
		self.assertEqual(my_family.get_proband_id(), 'proband')
		self.assertCountEqual(my_family.get_affected_female_members(), [])
		self.assertCountEqual(my_family.get_unaffected_female_members(), ['mum'])
		self.assertCountEqual(my_family.get_affected_male_members(), ['proband', 'sibling'])
		self.assertCountEqual(my_family.get_unaffected_male_members(), ['dad'])
		self.assertCountEqual(my_family.get_daughter_ids('dad'), [])
		self.assertCountEqual(my_family.get_daughter_ids('mum'), [])
		self.assertCountEqual(my_family.get_son_ids('dad'), ['proband', 'sibling'])
		self.assertCountEqual(my_family.get_son_ids('mum'), ['proband', 'sibling'])

	def test_valid_multiple_affected_affected_mum(self):

		mum = FamilyMember('mum', 'FAM001', 2, True)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		sibling = FamilyMember('sibling', 'FAM001', 2, True, mum=mum, dad=dad)

		my_family = Family('FAM001')


		my_family.add_family_member(mum)
		my_family.add_family_member(dad)
		my_family.add_family_member(proband)
		my_family.add_family_member(sibling)

		my_family.set_proband(proband.get_id())

		self.assertCountEqual(my_family.get_affected_family_members(), ['proband', 'sibling', 'mum'])
		self.assertCountEqual(my_family.get_unaffected_family_members(), ['dad'])
		self.assertCountEqual(my_family.get_male_family_members(), ['proband', 'dad'])
		self.assertCountEqual(my_family.get_female_family_members(), ['mum', 'sibling'])
		self.assertCountEqual(my_family.get_all_family_member_ids(), ['proband', 'mum', 'dad', 'sibling'])
		self.assertEqual(my_family.get_proband().get_id(), 'proband')
		self.assertEqual(my_family.get_proband_id(), 'proband')
		self.assertCountEqual(my_family.get_affected_female_members(), ['mum', 'sibling'])
		self.assertCountEqual(my_family.get_unaffected_female_members(), [])
		self.assertCountEqual(my_family.get_affected_male_members(), ['proband'])
		self.assertCountEqual(my_family.get_unaffected_male_members(), ['dad'])
		self.assertCountEqual(my_family.get_daughter_ids('dad'), ['sibling'])
		self.assertCountEqual(my_family.get_daughter_ids('mum'), ['sibling'])
		self.assertCountEqual(my_family.get_son_ids('dad'), ['proband'])
		self.assertCountEqual(my_family.get_son_ids('mum'), ['proband'])

	def test_attempt_duplicate_entry(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)

		my_family = Family('FAM001')

		try:

			my_family.add_family_member(dad)
			my_family.add_family_member(dad)
			my_family.add_family_member(proband)

			self.fail()

		except ValueError:

			self.assertEqual(1,1)

	def test_parents_not_in_family(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		
		try:

			my_family.add_family_member(proband)
			my_family.add_family_member(dad)
			my_family.add_family_member(mum)
			self.fail()

		except ValueError:

			self.assertEqual(1,1)


class TestFamilyMethods(unittest.TestCase):


	def test_proband_has_both_parents(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)

		my_family = Family('FAM001')
		my_family.add_family_member(mum)
		my_family.add_family_member(dad)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		self.assertEqual(my_family.proband_has_both_parents(), True)


		mum = FamilyMember('mum', 'FAM001', 2, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum)

		my_family = Family('FAM001')
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		self.assertEqual(my_family.proband_has_both_parents(), False)


		proband = FamilyMember('proband', 'FAM001', 1, True)

		my_family = Family('FAM001')
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		self.assertEqual(my_family.proband_has_both_parents(), False)


class TestVariant(unittest.TestCase):

	def test_invalid_chrom(self):

		try:

			variant = Variant(chrom='56', pos=10, ref='A', alt='G')
			self.fail()

		except ValueError:

			self.assertEqual(1,1)

	def test_invalid_position(self):

		try:

			variant = Variant(chrom='2', pos='10', ref='A', alt='G')
			self.fail()

		except ValueError:

			self.assertEqual(1,1)

	def test_invalid_ref(self):

		try:

			variant = Variant(chrom='2', pos='10', ref=1, alt='G')
			self.fail()

		except ValueError:

			self.assertEqual(1,1)

	def test_invalid_alt(self):

		try:
			
			variant = Variant(chrom='2', pos='10', ref='G', alt=1)
			self.fail()

		except ValueError:

			self.assertEqual(1,1)

	def test_add_family(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())
		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		try:
			variant.add_family('string')
			self.fail()

		except:

			self.assertEqual(1,1)


	def test_invalid_genotype(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		try:
			variant.add_genotype('proband', ['G', 'T'], [10,7], 99, 20 )
		except AssertionError:
			self.assertEqual(1,1)

		try:
			variant.add_genotype('proband', ['G', 'A', 'A'], [10,7], 99,20 )
		except AssertionError:
			self.assertEqual(1,1)

		try:
			variant.add_genotype('proband', '0/1', [10,7], 99,20 )
		except AssertionError:
			self.assertEqual(1,1)

	def test_invalid_allele_depths(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		try:
			variant.add_genotype('proband', ['G', 'A'], ['10',7], 99,20 )
		except AssertionError:
			self.assertEqual(1,1)

		try:
			variant.add_genotype('proband', ['G', 'A'], [], 99,20 )
		except AssertionError:
			self.assertEqual(1,1)

		variant.add_genotype('proband', ['G', 'A'], [10,2], 99,20 )
		self.assertEqual(variant.genotypes['proband']['allele_depths'], [10,2])

	def test_invalid_genome_quality(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		try:
			variant.add_genotype('proband', ['G', 'A'], ['10',7], '99',20 )
		except AssertionError:
			self.assertEqual(1,1)

		variant.add_genotype('proband', ['G', 'A'], [10,2], 99,20 )
		self.assertEqual(variant.genotypes['proband']['genotype_quality'], 99)

	def test_homozygous_ref(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		self.assertEqual(variant.is_hom_ref('proband'), False)

		variant.add_genotype('proband', ['G', 'G'], [10, 2], 99, 20 )
		self.assertEqual(variant.is_hom_ref('proband'), True)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		self.assertEqual(variant.is_hom_ref('proband'), False)

		variant.add_genotype('proband', ['.', '.'], [10, 2], 99, 20 )
		self.assertEqual(variant.is_hom_ref('proband'), False)	

	def test_has_no_alt(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['G', 'G'], [10, 2], 99, 20 )
		self.assertEqual(variant.has_no_alt('proband'), True)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		self.assertEqual(variant.has_no_alt('proband'), False)

		variant.add_genotype('proband', ['.', '.'], [10, 2], 99, 20 )
		self.assertEqual(variant.has_no_alt('proband'), True)

	def test_is_het(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		self.assertEqual(variant.is_het('proband'), True)

		variant.add_genotype('proband', ['.', 'A'], [10, 2], 99, 20 )
		self.assertEqual(variant.is_het('proband'), True)

		variant.add_genotype('proband', ['A', '.'], [10, 2], 99, 20 )
		self.assertEqual(variant.is_het('proband'), True)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		self.assertEqual(variant.is_het('proband'), False)

	def test_has_alt(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		self.assertEqual(variant.has_alt('proband'), True)

		variant.add_genotype('proband', ['.', 'A'], [10, 2], 99, 20 )
		self.assertEqual(variant.has_alt('proband'), True)

		variant.add_genotype('proband', ['A', '.'], [10, 2], 99, 20 )
		self.assertEqual(variant.has_alt('proband'), True)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		self.assertEqual(variant.has_alt('proband'), True)

		variant.add_genotype('proband', ['.', '.'], [10, 2], 99, 20 )
		self.assertEqual(variant.has_alt('proband'), False)

		variant.add_genotype('proband', ['G', 'G'], [10, 2], 99, 20 )
		self.assertEqual(variant.has_alt('proband'), False)	




class TestDominantTrioUnaffectedParents(unittest.TestCase):
	"""
	Test that in a trio with unaffected parents a het variant does not match

	"""

	def test_not_dominant(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_autosomal_dominant(), False)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_autosomal_dominant(), False)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['A', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_autosomal_dominant(), False)

		# De novo
		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_autosomal_dominant(), True)

	
	def test_dominant(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_autosomal_dominant(), True)


		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['.', '.'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_autosomal_dominant(), True)

		
		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', '.'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_autosomal_dominant(), True)




class TestDominantTrioUnaffectedParentsLowPenetrance(unittest.TestCase):
	"""
	Test that in a trio with unaffected parents a het variant does not match

	"""

	def test_not_dominant(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)
		variant.add_transcript_annotations([{'SYMBOL': 'geneA','Consequence': 'missense_variant'}])

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_autosomal_dominant(low_penetrance_genes={'geneA'}), True)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_autosomal_dominant(low_penetrance_genes={'geneA'}), True)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['A', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_autosomal_dominant(low_penetrance_genes={'geneA'}), True)

		# De novo
		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_autosomal_dominant(low_penetrance_genes={'geneA'}), True)



class TestDominantOneParentOnly(unittest.TestCase):

	def test_one_parent_only(self):

		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_autosomal_dominant(), True)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_autosomal_dominant(), False)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['.', '.'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_autosomal_dominant(), True)


class TestDominantTwoAffectedSiblingsOnly(unittest.TestCase):

		def test_two_affected_siblings_only(self):

			sibling = FamilyMember('sibling', 'FAM001', 1, True)
			proband = FamilyMember('proband', 'FAM001', 1, True)
			my_family = Family('FAM001')
			my_family.add_family_member(sibling)
			my_family.add_family_member(proband)
			my_family.set_proband(proband.get_id())

			variant = Variant(chrom='2', pos=10, ref='G', alt='A')
			variant.add_family(my_family)

			variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
			variant.add_genotype('sibling', ['G', 'G'], [10, 2], 99, 20 )

			self.assertEqual(variant.matches_autosomal_dominant(), False)

			variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
			variant.add_genotype('sibling', ['G', 'A'], [10, 2], 99, 20 )

			self.assertEqual(variant.matches_autosomal_dominant(), True)

			variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
			variant.add_genotype('sibling', ['.', '.'], [10, 2], 99, 20 )

			self.assertEqual(variant.matches_autosomal_dominant(), True)

			variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
			variant.add_genotype('sibling', ['A', 'A'], [10, 2], 99, 20 )

			self.assertEqual(variant.matches_autosomal_dominant(), False)
			self.assertEqual(variant.matches_autosomal_dominant(lenient=True), True)

class TestDominantTrioAffectedParent(unittest.TestCase):
	"""
	Check that variants which match interitance in a trio with an affected parent
	"""

	def test_affected_mum(self):

		mum = FamilyMember('mum', 'FAM001', 2, True)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_autosomal_dominant(), True)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_autosomal_dominant(), False)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_autosomal_dominant(), False)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['.', '.'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_autosomal_dominant(), True)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['.', '.'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_autosomal_dominant(), True)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_autosomal_dominant(), False)
		self.assertEqual(variant.matches_autosomal_dominant(lenient=True), True)

		variant.add_genotype('proband', ['.', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_autosomal_dominant(), True)

		variant.add_genotype('proband', ['.', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['.', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_autosomal_dominant(), True)


class TestDominantAffectedSiblingAffectedDad(unittest.TestCase):
	"""
	Test that we find dominant variants in a family with two affected siblings and an affected parent.

	"""

	def test_affected_sibling(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, True)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		sibling = FamilyMember('sibling', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.add_family_member(sibling)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('sibling', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_autosomal_dominant(), False)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('sibling', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['A', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_autosomal_dominant(), True)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('sibling', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['A', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_autosomal_dominant(), False)
		self.assertEqual(variant.matches_autosomal_dominant(lenient=True), True)


class TestDominantUnAffectedSiblingAffectedDad(unittest.TestCase):
	"""
	Test that we find dominant variants in a family with two affected siblings and an affected parent.

	"""

	def test_affected_sibling(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, True)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		sibling = FamilyMember('sibling', 'FAM001', 1, False, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.add_family_member(sibling)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('sibling', ['G', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_autosomal_dominant(), True)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('sibling', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_autosomal_dominant(), False)


class TestDominantSingleton(unittest.TestCase):

	def test_dominant_singleton(self):

		proband = FamilyMember('proband', 'FAM001', 1, True)
		my_family = Family('FAM001')
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())
		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)


		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		self.assertEqual(variant.matches_autosomal_dominant(), True)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		self.assertEqual(variant.matches_autosomal_dominant(), False)

		variant.add_genotype('proband', ['.', 'A'], [10, 2], 99, 20 )
		self.assertEqual(variant.matches_autosomal_dominant(), True)

		variant.add_genotype('proband', ['.', '.'], [10, 2], 99, 20 )
		self.assertEqual(variant.matches_autosomal_dominant(), True)

class TestAutosomalReccessiveTrioUnaffectedParents(unittest.TestCase):

	def test_ar_trio(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_autosomal_reccessive(), False)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_autosomal_reccessive(), False)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_autosomal_reccessive(), True)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_autosomal_reccessive(), False)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['.', '.'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_autosomal_reccessive(), True)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_autosomal_reccessive(), True)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['.', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_autosomal_reccessive(), True)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['.', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_autosomal_reccessive(), True)


class TestAutosomalReccessiveUnaffectedParentsAffectedSibling(unittest.TestCase):

	def test_ar_unaffected_parents_affected_sibling(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		sibling = FamilyMember('sibling', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(sibling)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('sibling', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_autosomal_reccessive(), True)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('sibling', ['A', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [10, 2], 99, 20 )	

		self.assertEqual(variant.matches_autosomal_reccessive(), False)

		variant.add_genotype('proband', ['A', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('sibling', ['A', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [10, 2], 99, 20 )	

		self.assertEqual(variant.matches_autosomal_reccessive(), False)	

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('sibling', ['.', '.'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [10, 2], 99, 20 )	

		self.assertEqual(variant.matches_autosomal_reccessive(), True)

		# Should mixed genotypes count?
		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('sibling', ['.', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [10, 2], 99, 20 )	

		self.assertEqual(variant.matches_autosomal_reccessive(), False)	

class TestAutosomalReccessiveSingleton(unittest.TestCase):

	def test_ar_singleton(self):

		proband = FamilyMember('proband', 'FAM001', 1, True)

		my_family = Family('FAM001')
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		self.assertEqual(variant.matches_autosomal_reccessive(), True)

		variant.add_genotype('proband', ['A', '.'], [10, 2], 99, 20 )
		self.assertEqual(variant.matches_autosomal_reccessive(), False)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		self.assertEqual(variant.matches_autosomal_reccessive(), False)

class TestDeNovo(unittest.TestCase):


	def test_denovo_no_parents(self):

		proband = FamilyMember('proband', 'FAM001', 1, True)

		my_family = Family('FAM001')
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['A', 'G'], [10, 3], 99, 20 )

		self.assertEqual(variant.matches_denovo('proband'), False)


	def test_one_parent(self):

		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [12, 0], 99, 20 )

		self.assertEqual(variant.matches_denovo(), False)

	def test_trio(self):

		dad = FamilyMember('dad', 'FAM001', 1, False)
		mum = FamilyMember('mum', 'FAM001', 2, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, dad=dad, mum=mum)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [12, 0], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [12, 0], 99, 20 )

		self.assertEqual(variant.matches_denovo(), True)


		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [12, 0], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [12, 0], 99, 20 )

		self.assertEqual(variant.matches_denovo(), True)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', '.'], [12, 0], 99, 20 )
		variant.add_genotype('dad', ['.', 'G'], [12, 0], 99, 20 )

		self.assertEqual(variant.matches_denovo(), True)


		variant.add_genotype('proband', ['.', '.'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', '.'], [12, 0], 99, 20 )
		variant.add_genotype('dad', ['.', 'G'], [12, 0], 99, 20 )

		self.assertEqual(variant.matches_denovo(), False)

	def test_no_proband_set(self):

		dad = FamilyMember('dad', 'FAM001', 1, False)
		mum = FamilyMember('mum', 'FAM001', 2, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, dad=dad, mum=mum)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [12, 0], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [12, 0], 99, 20 )

		try:

			self.assertEqual(variant.matches_denovo(), False)
			self.fail()

		except AssertionError:

			self.assertEqual(1,1)

	def test_too_high_alt_ref_ratio(self):

		dad = FamilyMember('dad', 'FAM001', 1, False)
		mum = FamilyMember('mum', 'FAM001', 2, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, dad=dad, mum=mum)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [30, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [12, 0], 99, 20 )

		self.assertEqual(variant.matches_denovo(), False)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [30, 0], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [30, 5], 99, 20 )

		self.assertEqual(variant.matches_denovo(), False)


class TestXReccessiveTrioUnaffectedParents(unittest.TestCase):

	def test_affected_son(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='X', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_reccessive(), True)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_reccessive(), True)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_reccessive(), False)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_reccessive(), False)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_reccessive(), True)

	def test_affected_daughter(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 2, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='X', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_reccessive(), False)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_reccessive(), True)


class TestXReccessiveTrioAffectedDad(unittest.TestCase):

	def test_affected_dad(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, True)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='X', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['A', 'A'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_reccessive(), True)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['.', 'A'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_reccessive(), True)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['.', '.'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_reccessive(), True)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_reccessive(), False)


		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_reccessive(), False)

class TestXReccessiveTrioAffectedMum(unittest.TestCase):

	def test_affected_dad(self):

		mum = FamilyMember('mum', 'FAM001', 2, True)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='X', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_reccessive(), True)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_reccessive(), False)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_reccessive(), False)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_reccessive(), True)

		variant.add_genotype('proband', ['.', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_reccessive(), True)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['.', '.'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_reccessive(), True)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['.', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_reccessive(), False)


class TestXReccessiveSingleton(unittest.TestCase):

	def test_male_proband(self):

		proband = FamilyMember('proband', 'FAM001', 1, True)
		my_family = Family('FAM001')
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='X', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		self.assertEqual(variant.matches_x_reccessive(), True)

		variant.add_genotype('proband', ['A', 'G'], [10, 2], 99, 20 )
		self.assertEqual(variant.matches_x_reccessive(), True)

		variant.add_genotype('proband', ['A', '.'], [10, 2], 99, 20 )
		self.assertEqual(variant.matches_x_reccessive(), True)

	def test_female_proband(self):

		proband = FamilyMember('proband', 'FAM001', 2, True)
		my_family = Family('FAM001')
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='X', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		self.assertEqual(variant.matches_x_reccessive(), True)

		variant.add_genotype('proband', ['A', 'G'], [10, 2], 99, 20 )
		self.assertEqual(variant.matches_x_reccessive(), False)

		variant.add_genotype('proband', ['A', '.'], [10, 2], 99, 20 )
		self.assertEqual(variant.matches_x_reccessive(), False)


class TestXReccessiveSingleUnaffectedParent(unittest.TestCase):

	def test_male_proband_with_mum(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum)
		my_family = Family('FAM001')
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='X', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_reccessive(), True)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['A', 'A'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_reccessive(), False)


	def test_male_proband_with_dad(self):

		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='X', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_reccessive(), False)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['A', 'A'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_reccessive(), False)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_reccessive(), True)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['.', '.'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_reccessive(), True)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['.', '.'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_reccessive(), True)

class TestXReccessiveSingleAffectedParent(unittest.TestCase):

	def test_male_proband_with_mum(self):

		mum = FamilyMember('mum', 'FAM001', 2, True)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum)
		my_family = Family('FAM001')
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='X', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_reccessive(), False)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['A', 'A'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_reccessive(), True)


	def test_male_proband_with_dad(self):

		dad = FamilyMember('dad', 'FAM001', 1, True)
		proband = FamilyMember('proband', 'FAM001', 1, True, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='X', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_reccessive(), True)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['A', 'A'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_reccessive(), True)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_reccessive(), False)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['.', '.'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_reccessive(), True)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['.', '.'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_reccessive(), True) 


class TestXDominantTrioUnaffectedParents(unittest.TestCase):

	def test_affected_son(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='X', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_dominant(), False)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_dominant(), False)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['.', '.'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_dominant(), True)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['.', '.'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['.', '.'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_dominant(), True)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['.', '.'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['.', '.'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_dominant(), True)

	def test_affected_daughter(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 2, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='X', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_dominant(), False)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_dominant(), False)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['.', '.'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_dominant(), True)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['.', '.'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['.', '.'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_dominant(), True)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['.', '.'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['.', '.'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_dominant(), False)
		self.assertEqual(variant.matches_x_reccessive(), True)


class TestXDominantTrioAffectedMum(unittest.TestCase):

	def test_affected_son(self):

		mum = FamilyMember('mum', 'FAM001', 2, True)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='X', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_dominant(), True)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_dominant(), False)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['.', '.'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_dominant(), True)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['.', '.'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['.', '.'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_dominant(), True)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['.', '.'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['.', '.'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_dominant(), True)


	def test_affected_daughter(self):

		mum = FamilyMember('mum', 'FAM001', 2, True)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 2, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='X', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_dominant(), True)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_dominant(), False)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['.', '.'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_dominant(), True)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['.', '.'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['.', '.'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_dominant(), True)

		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['.', '.'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['.', '.'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_dominant(), False)
		self.assertEqual(variant.matches_x_reccessive(), True)	



class TestXDominantTrioAffectedDad(unittest.TestCase):

	def test_affected_son(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, True)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='X', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		# affected male cannot have an affected son
		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_dominant(), False)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['.', '.'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['.', '.'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_dominant(), False)


	def test_affected_daughter(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, True)
		proband = FamilyMember('proband', 'FAM001', 2, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='X', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		#Affected males's daughters must be affected

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_dominant(), True)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_dominant(), False)

		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_dominant(), False)


class TestXDominantMutipleSiblings(unittest.TestCase):

	def test_affected_son(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, True)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		sibling = FamilyMember('sibling', 'FAM001', 2, False, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.add_family_member(sibling)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='X', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		# affected male cannot have an affected son
		variant.add_genotype('proband', ['A', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('sibling', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_dominant(), False)

	def test_affected_daughter(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, True)
		proband = FamilyMember('proband', 'FAM001', 2, True, mum=mum, dad=dad)
		sibling = FamilyMember('sibling', 'FAM001', 1, False, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.add_family_member(sibling)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='X', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		# affected male cannot have an affected son
		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('sibling', ['G', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_dominant(), True)


	def test_two_daughter_different_status(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, True)
		proband = FamilyMember('proband', 'FAM001', 2, True, mum=mum, dad=dad)
		sibling = FamilyMember('sibling', 'FAM001', 2, False, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.add_family_member(sibling)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='X', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		# affected male cannot have an unaffected daughter
		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('sibling', ['.', '.'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_dominant(), False)

	def test_two_daughter_same_status(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, True)
		proband = FamilyMember('proband', 'FAM001', 2, True, mum=mum, dad=dad)
		sibling = FamilyMember('sibling', 'FAM001', 2, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.add_family_member(sibling)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='X', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		# affected male cannot have an unaffected daughter
		variant.add_genotype('proband', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('sibling', ['.', '.'], [10, 2], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [10, 2], 99, 20 )

		self.assertEqual(variant.matches_x_dominant(), True)



class TestUniParentalIsoDisomy(unittest.TestCase):

	def test_trio_autosome(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 2, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['A', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [12, 0], 99, 20 )

		self.assertEqual(variant.matches_uniparental_isodisomy(), True)

		variant.add_genotype('proband', ['A', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 5, 20 )
		variant.add_genotype('dad', ['G', 'G'], [12, 0], 99, 20 )

		self.assertEqual(variant.matches_uniparental_isodisomy(), False)

		variant.add_genotype('proband', ['A', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [12, 0], 5, 20 )

		self.assertEqual(variant.matches_uniparental_isodisomy(), False)

		variant.add_genotype('proband', ['A', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [2, 2], 99, 4 )
		variant.add_genotype('dad', ['G', 'G'], [12, 0], 5, 20 )

		self.assertEqual(variant.matches_uniparental_isodisomy(), False)

		variant.add_genotype('proband', ['A', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [12, 0], 99, 20 )

		self.assertEqual(variant.matches_uniparental_isodisomy(), False)

		variant.add_genotype('proband', ['A', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [12, 0], 99, 20 )

		self.assertEqual(variant.matches_uniparental_isodisomy(), True)

		variant.add_genotype('proband', ['A', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [12, 0], 99, 20 )

		self.assertEqual(variant.matches_uniparental_isodisomy(), True)

		variant.add_genotype('proband', ['A', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['A', 'A'], [12, 0], 99, 20 )

		self.assertEqual(variant.matches_uniparental_isodisomy(), False)


	def test_trio_X_chrom_male_proband(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='X', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['A', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [12, 0], 99, 20 )

		self.assertEqual(variant.matches_uniparental_isodisomy(), False)

		variant.add_genotype('proband', ['A', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [12, 0], 99, 20 )

		self.assertEqual(variant.matches_uniparental_isodisomy(), False)

	def test_trio_X_chrom_female_proband(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 2, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='X', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['A', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [12, 0], 99, 20 )

		self.assertEqual(variant.matches_uniparental_isodisomy(), True)

		variant.add_genotype('proband', ['A', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 5, 20 )
		variant.add_genotype('dad', ['G', 'G'], [12, 0], 99, 20 )

		self.assertEqual(variant.matches_uniparental_isodisomy(), False)


class TestCandidateCompoundHets(unittest.TestCase):


	def test_compound_het_pair_autosome_trio(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 2, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)
		variant.add_transcript_annotations([{'Feature': 'geneA', 'Consequence': 'missense_variant'}])

		variant2 = Variant(chrom='2', pos=100, ref='G', alt='A')
		variant2.add_family(my_family)
		variant2.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		variant.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [12, 0], 99, 20 )

		variant2.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant2.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant2.add_genotype('dad', ['G', 'A'], [12, 0], 99, 20 )


		variant_set = VariantSet()
		variant_set.add_family(my_family)

		variant_set.add_variant(variant)
		variant_set.add_variant(variant2)

		variant_set.get_candidate_compound_hets()

		self.assertEqual(len(variant_set.candidate_compound_het_dict['geneA']), 2) 


	def test_compound_het_single_autosome_trio(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 2, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)
		variant.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		variant.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [12, 0], 99, 20 )

		variant_set = VariantSet()
		variant_set.add_family(my_family)

		variant_set.add_variant(variant)

		variant_set.get_candidate_compound_hets()
		variant_set.get_unfiltered_compound_hets_as_dict()

		self.assertEqual(len(variant_set.candidate_compound_het_dict['geneA']), 1)
		self.assertCountEqual(variant_set.final_compound_hets, {}) 


	def test_compound_het_pair_autosome_trio_hom_alt_unaffected(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 2, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)
		variant.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		variant2 = Variant(chrom='2', pos=100, ref='G', alt='A')
		variant2.add_family(my_family)
		variant2.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		variant.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['A', 'A'], [12, 0], 99, 20 )

		variant2.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant2.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant2.add_genotype('dad', ['G', 'A'], [12, 0], 99, 20 )


		variant_set = VariantSet()
		variant_set.add_family(my_family)

		variant_set.add_variant(variant)
		variant_set.add_variant(variant2)

		variant_set.get_candidate_compound_hets()

		self.assertEqual(len(variant_set.candidate_compound_het_dict['geneA']), 1) 


	def test_compound_het_pair_autosome_trio_hom_alt_proband(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 2, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)
		variant.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		variant2 = Variant(chrom='2', pos=100, ref='G', alt='A')
		variant2.add_family(my_family)
		variant2.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		variant.add_genotype('proband', ['A', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [12, 0], 99, 20 )

		variant2.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant2.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant2.add_genotype('dad', ['G', 'A'], [12, 0], 99, 20 )


		variant_set = VariantSet()
		variant_set.add_family(my_family)

		variant_set.add_variant(variant)
		variant_set.add_variant(variant2)

		variant_set.get_candidate_compound_hets()

		self.assertEqual(len(variant_set.candidate_compound_het_dict['geneA']), 1) 

	def test_compound_het_pair_female_x_trio(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 2, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='X', pos=10, ref='G', alt='A')
		variant.add_family(my_family)
		variant.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		variant2 = Variant(chrom='X', pos=100, ref='G', alt='A')
		variant2.add_family(my_family)
		variant2.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		variant.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [12, 0], 99, 20 )

		variant2.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant2.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant2.add_genotype('dad', ['G', 'A'], [12, 0], 99, 20 )


		variant_set = VariantSet()
		variant_set.add_family(my_family)

		variant_set.add_variant(variant)
		variant_set.add_variant(variant2)

		variant_set.get_candidate_compound_hets()

		self.assertEqual(len(variant_set.candidate_compound_het_dict['geneA']), 2) 


	def test_compound_het_pair_male_x_trio(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='X', pos=10, ref='G', alt='A')
		variant.add_family(my_family)
		variant.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		variant2 = Variant(chrom='X', pos=100, ref='G', alt='A')
		variant2.add_family(my_family)
		variant2.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		variant.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [12, 0], 99, 20 )

		variant2.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant2.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant2.add_genotype('dad', ['G', 'A'], [12, 0], 99, 20 )


		variant_set = VariantSet()
		variant_set.add_family(my_family)

		variant_set.add_variant(variant)
		variant_set.add_variant(variant2)

		variant_set.get_candidate_compound_hets()

		self.assertEqual(len(variant_set.candidate_compound_het_dict), 0) 


class TestFilterCompoundHetsAutosome(unittest.TestCase):

	def test_trio_genuine_compound_het(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)
		variant.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		variant2 = Variant(chrom='2', pos=100, ref='G', alt='A')
		variant2.add_family(my_family)
		variant2.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		# Test one from mum and one from dad
		variant.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [12, 0], 99, 20 )

		variant2.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant2.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant2.add_genotype('dad', ['G', 'A'], [12, 0], 99, 20 )

		variant_set = VariantSet()
		variant_set.add_family(my_family)

		variant_set.add_variant(variant)
		variant_set.add_variant(variant2)

		variant_set.get_candidate_compound_hets()
		variant_set.filter_compound_hets()
		variant_set.get_filtered_compound_hets_as_dict()

		self.assertCountEqual(variant_set.final_compound_hets, {'2:10G>A': None, '2:100G>A': None})

		# Test other way around
		variant.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [12, 0], 99, 20 )

		variant2.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant2.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant2.add_genotype('dad', ['G', 'G'], [12, 0], 99, 20 )

		variant_set = VariantSet()
		variant_set.add_family(my_family)

		variant_set.add_variant(variant)
		variant_set.add_variant(variant2)

		variant_set.get_candidate_compound_hets()
		variant_set.filter_compound_hets()
		variant_set.get_filtered_compound_hets_as_dict()

		self.assertCountEqual(variant_set.final_compound_hets, {'2:10G>A': None, '2:100G>A': None})


	def test_trio_nongenuine_compound_het_dad_has_both(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)
		variant.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		variant2 = Variant(chrom='2', pos=100, ref='G', alt='A')
		variant2.add_family(my_family)
		variant2.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		# Test one from mum and one from dad
		variant.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [12, 0], 99, 20 )

		variant2.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant2.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant2.add_genotype('dad', ['G', 'A'], [12, 0], 99, 20 )

		variant_set = VariantSet()
		variant_set.add_family(my_family)

		variant_set.add_variant(variant)
		variant_set.add_variant(variant2)

		variant_set.get_candidate_compound_hets()
		variant_set.filter_compound_hets()
		variant_set.get_filtered_compound_hets_as_dict()

		self.assertCountEqual(variant_set.final_compound_hets, {})

	def test_trio_nongenuine_compound_het_mum_has_both(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)
		variant.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		variant2 = Variant(chrom='2', pos=100, ref='G', alt='A')
		variant2.add_family(my_family)
		variant2.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		# Test one from mum and one from dad
		variant.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [12, 0], 99, 20 )

		variant2.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant2.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant2.add_genotype('dad', ['G', 'G'], [12, 0], 99, 20 )

		variant_set = VariantSet()
		variant_set.add_family(my_family)

		variant_set.add_variant(variant)
		variant_set.add_variant(variant2)

		variant_set.get_candidate_compound_hets()
		variant_set.filter_compound_hets()
		variant_set.get_filtered_compound_hets_as_dict()

		self.assertCountEqual(variant_set.final_compound_hets, {})

	def test_trio_missing_parental_genotypes(self):
		
		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)
		variant.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		variant2 = Variant(chrom='2', pos=100, ref='G', alt='A')
		variant2.add_family(my_family)
		variant2.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		# Test one from mum and one from dad
		variant.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['.', '.'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['.', '.'], [12, 0], 99, 20 )

		variant2.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant2.add_genotype('mum', ['.', '.'], [10, 2], 99, 20 )
		variant2.add_genotype('dad', ['.', '.'], [12, 0], 99, 20 )

		variant_set = VariantSet()
		variant_set.add_family(my_family)

		variant_set.add_variant(variant)
		variant_set.add_variant(variant2)

		variant_set.get_candidate_compound_hets()
		variant_set.filter_compound_hets()
		variant_set.get_filtered_compound_hets_as_dict()

		self.assertCountEqual(variant_set.final_compound_hets, {'2:10G>A': None, '2:100G>A': None})

	def test_trio_missing_parental_genotypes_false(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)
		variant.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		variant2 = Variant(chrom='2', pos=100, ref='G', alt='A')
		variant2.add_family(my_family)
		variant2.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		# Test one from mum and one from dad
		variant.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['.', '.'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['.', '.'], [12, 0], 99, 20 )

		variant2.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant2.add_genotype('mum', ['.', '.'], [10, 2], 99, 20 )
		variant2.add_genotype('dad', ['.', '.'], [12, 0], 99, 20 )

		variant_set = VariantSet()
		variant_set.add_family(my_family)

		variant_set.add_variant(variant)
		variant_set.add_variant(variant2)

		variant_set.get_candidate_compound_hets()
		variant_set.filter_compound_hets(include_denovo=False)
		variant_set.get_filtered_compound_hets_as_dict()

		self.assertCountEqual(variant_set.final_compound_hets, {})


	def test_trio_missing_dad_genotypes(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)
		variant.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		variant2 = Variant(chrom='2', pos=100, ref='G', alt='A')
		variant2.add_family(my_family)
		variant2.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		# Test one from mum and one from dad
		variant.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['.', '.'], [12, 0], 99, 20 )

		variant2.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant2.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant2.add_genotype('dad', ['.', '.'], [12, 0], 99, 20 )

		variant_set = VariantSet()
		variant_set.add_family(my_family)

		variant_set.add_variant(variant)
		variant_set.add_variant(variant2)

		variant_set.get_candidate_compound_hets()
		variant_set.filter_compound_hets(include_denovo=False)
		variant_set.get_filtered_compound_hets_as_dict()

		self.assertCountEqual(variant_set.final_compound_hets, {'2:10G>A': None, '2:100G>A': None})

	def test_trio_missing_mum_genotypes(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)
		variant.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		variant2 = Variant(chrom='2', pos=100, ref='G', alt='A')
		variant2.add_family(my_family)
		variant2.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		# Test one from mum and one from dad
		variant.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['.', '.'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'A'], [12, 0], 99, 20 )

		variant2.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant2.add_genotype('mum', ['.', '.'], [10, 2], 99, 20 )
		variant2.add_genotype('dad', ['G', 'G'], [12, 0], 99, 20 )

		variant_set = VariantSet()
		variant_set.add_family(my_family)

		variant_set.add_variant(variant)
		variant_set.add_variant(variant2)

		variant_set.get_candidate_compound_hets()
		variant_set.filter_compound_hets(include_denovo=False)
		variant_set.get_filtered_compound_hets_as_dict()

		self.assertCountEqual(variant_set.final_compound_hets, {'2:10G>A': None, '2:100G>A': None})


	def test_trio_missing_genotypes_dad_one(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)
		variant.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		variant2 = Variant(chrom='2', pos=100, ref='G', alt='A')
		variant2.add_family(my_family)
		variant2.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		# Test one from mum and one from dad
		variant.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['.', '.'], [12, 0], 99, 20 )

		variant2.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant2.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant2.add_genotype('dad', ['G', 'A'], [12, 0], 99, 20 )

		variant_set = VariantSet()
		variant_set.add_family(my_family)

		variant_set.add_variant(variant)
		variant_set.add_variant(variant2)

		variant_set.get_candidate_compound_hets()
		variant_set.filter_compound_hets(include_denovo=False)
		variant_set.get_filtered_compound_hets_as_dict()

		self.assertCountEqual(variant_set.final_compound_hets, {'2:10G>A': None, '2:100G>A': None})

	def test_trio_missing_genotypes_dad_two(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)
		variant.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		variant2 = Variant(chrom='2', pos=100, ref='G', alt='A')
		variant2.add_family(my_family)
		variant2.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		# Test one from mum and one from dad
		variant.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['.', '.'], [12, 0], 99, 20 )

		variant2.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant2.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant2.add_genotype('dad', ['.', '.'], [12, 0], 99, 20 )

		variant_set = VariantSet()
		variant_set.add_family(my_family)

		variant_set.add_variant(variant)
		variant_set.add_variant(variant2)

		variant_set.get_candidate_compound_hets()
		variant_set.filter_compound_hets(include_denovo=False)
		variant_set.get_filtered_compound_hets_as_dict()

		self.assertCountEqual(variant_set.final_compound_hets, {})

	def test_trio_more_than_two(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)
		variant.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		variant2 = Variant(chrom='2', pos=100, ref='G', alt='A')
		variant2.add_family(my_family)
		variant2.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		variant3 = Variant(chrom='2', pos=1000, ref='G', alt='A')
		variant3.add_family(my_family)
		variant3.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		# Test one from mum and one from dad
		variant.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [12, 0], 99, 20 )

		variant2.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant2.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant2.add_genotype('dad', ['G', 'G'], [12, 0], 99, 20 )

		variant3.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant3.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant3.add_genotype('dad', ['G', 'A'], [12, 0], 99, 20 )

		variant_set = VariantSet()
		variant_set.add_family(my_family)

		variant_set.add_variant(variant)
		variant_set.add_variant(variant2)
		variant_set.add_variant(variant3)

		variant_set.get_candidate_compound_hets()
		variant_set.filter_compound_hets(include_denovo=False)
		variant_set.get_filtered_compound_hets_as_dict()

		self.assertCountEqual(variant_set.final_compound_hets, {'2:10G>A': None, '2:100G>A': None, '2:1000G>A': None})


	def test_trio_more_than_two(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)
		variant.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		variant2 = Variant(chrom='2', pos=100, ref='G', alt='A')
		variant2.add_family(my_family)
		variant2.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		variant3 = Variant(chrom='2', pos=1000, ref='G', alt='A')
		variant3.add_family(my_family)
		variant3.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		# Test one from mum and one from dad
		variant.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [12, 0], 99, 20 )

		variant2.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant2.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant2.add_genotype('dad', ['G', 'A'], [12, 0], 99, 20 )

		variant3.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant3.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant3.add_genotype('dad', ['G', 'A'], [12, 0], 99, 20 )

		variant_set = VariantSet()
		variant_set.add_family(my_family)

		variant_set.add_variant(variant)
		variant_set.add_variant(variant2)
		variant_set.add_variant(variant3)

		variant_set.get_candidate_compound_hets()
		variant_set.filter_compound_hets(include_denovo=False)
		variant_set.get_filtered_compound_hets_as_dict()

		self.assertCountEqual(variant_set.final_compound_hets, {'2:10G>A': None, '2:1000G>A': None})

class TestFilterCompoundHetsAutosomeAffectedSibling(unittest.TestCase):

	def test_sibling_also_has_variants(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		sibling = FamilyMember('sibling', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.add_family_member(sibling)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)
		variant.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		variant2 = Variant(chrom='2', pos=100, ref='G', alt='A')
		variant2.add_family(my_family)
		variant2.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		# Test one from mum and one from dad
		variant.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [12, 0], 99, 20 )
		variant.add_genotype('sibling', ['G', 'A'], [12, 0], 99, 20 )

		variant2.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant2.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant2.add_genotype('dad', ['G', 'A'], [12, 0], 99, 20 )
		variant2.add_genotype('sibling', ['G', 'A'], [12, 0], 99, 20 )

		variant_set = VariantSet()
		variant_set.add_family(my_family)

		variant_set.add_variant(variant)
		variant_set.add_variant(variant2)

		variant_set.get_candidate_compound_hets()
		variant_set.filter_compound_hets(include_denovo=False)
		variant_set.get_filtered_compound_hets_as_dict()

		self.assertCountEqual(variant_set.final_compound_hets, {'2:10G>A': None, '2:100G>A': None})

	def test_sibling_does_not_have_variants(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		sibling = FamilyMember('sibling', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.add_family_member(sibling)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)
		variant.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		variant2 = Variant(chrom='2', pos=100, ref='G', alt='A')
		variant2.add_family(my_family)
		variant2.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		# Test one from mum and one from dad
		variant.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [12, 0], 99, 20 )
		variant.add_genotype('sibling', ['G', 'A'], [12, 0], 99, 20 )

		variant2.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant2.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant2.add_genotype('dad', ['G', 'A'], [12, 0], 99, 20 )
		variant2.add_genotype('sibling', ['G', 'G'], [12, 0], 99, 20 )

		variant_set = VariantSet()
		variant_set.add_family(my_family)

		variant_set.add_variant(variant)
		variant_set.add_variant(variant2)

		variant_set.get_candidate_compound_hets()
		variant_set.filter_compound_hets(include_denovo=False)
		variant_set.get_filtered_compound_hets_as_dict()

		self.assertCountEqual(variant_set.final_compound_hets, {})

	def test_sibling_does_not_have_variants_but_missing(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		sibling = FamilyMember('sibling', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.add_family_member(sibling)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)
		variant.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		variant2 = Variant(chrom='2', pos=100, ref='G', alt='A')
		variant2.add_family(my_family)
		variant2.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		# Test one from mum and one from dad
		variant.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [12, 0], 99, 20 )
		variant.add_genotype('sibling', ['G', 'A'], [12, 0], 99, 20 )

		variant2.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant2.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant2.add_genotype('dad', ['G', 'A'], [12, 0], 99, 20 )
		variant2.add_genotype('sibling', ['.', '.'], [12, 0], 99, 20 )

		variant_set = VariantSet()
		variant_set.add_family(my_family)

		variant_set.add_variant(variant)
		variant_set.add_variant(variant2)

		variant_set.get_candidate_compound_hets()
		variant_set.filter_compound_hets(include_denovo=False)
		variant_set.get_filtered_compound_hets_as_dict()

		self.assertCountEqual(variant_set.final_compound_hets, {'2:10G>A': None, '2:100G>A': None})

	def test_sibling_does_not_have_variants_but_missing(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		sibling = FamilyMember('sibling', 'FAM001', 1, True, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.add_family_member(sibling)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)
		variant.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		variant2 = Variant(chrom='2', pos=100, ref='G', alt='A')
		variant2.add_family(my_family)
		variant2.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		# Test one from mum and one from dad
		variant.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [12, 0], 99, 20 )
		variant.add_genotype('sibling', ['.', '.'], [12, 0], 99, 20 )

		variant2.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant2.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant2.add_genotype('dad', ['G', 'A'], [12, 0], 99, 20 )
		variant2.add_genotype('sibling', ['.', '.'], [12, 0], 99, 20 )

		variant_set = VariantSet()
		variant_set.add_family(my_family)

		variant_set.add_variant(variant)
		variant_set.add_variant(variant2)

		variant_set.get_candidate_compound_hets()
		variant_set.filter_compound_hets(include_denovo=False)
		variant_set.get_filtered_compound_hets_as_dict()

		self.assertCountEqual(variant_set.final_compound_hets, {'2:10G>A': None, '2:100G>A': None})


class TestFilterCompoundHetsAutosomeUnaffectedSibling(unittest.TestCase):

	def test_sibling_also_has_variants(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		sibling = FamilyMember('sibling', 'FAM001', 1, False, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.add_family_member(sibling)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)
		variant.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		variant2 = Variant(chrom='2', pos=100, ref='G', alt='A')
		variant2.add_family(my_family)
		variant2.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		# Test one from mum and one from dad
		variant.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [12, 0], 99, 20 )
		variant.add_genotype('sibling', ['G', 'A'], [12, 0], 99, 20 )

		variant2.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant2.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant2.add_genotype('dad', ['G', 'A'], [12, 0], 99, 20 )
		variant2.add_genotype('sibling', ['G', 'A'], [12, 0], 99, 20 )

		variant_set = VariantSet()
		variant_set.add_family(my_family)

		variant_set.add_variant(variant)
		variant_set.add_variant(variant2)

		variant_set.get_candidate_compound_hets()
		variant_set.filter_compound_hets(include_denovo=False)
		variant_set.get_filtered_compound_hets_as_dict()

		self.assertCountEqual(variant_set.final_compound_hets, {})


	def test_sibling_does_not_have_variants(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		sibling = FamilyMember('sibling', 'FAM001', 1, False, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.add_family_member(sibling)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)
		variant.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		variant2 = Variant(chrom='2', pos=100, ref='G', alt='A')
		variant2.add_family(my_family)
		variant2.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		# Test one from mum and one from dad
		variant.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [12, 0], 99, 20 )
		variant.add_genotype('sibling', ['G', 'A'], [12, 0], 99, 20 )

		variant2.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant2.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant2.add_genotype('dad', ['G', 'A'], [12, 0], 99, 20 )
		variant2.add_genotype('sibling', ['G', 'G'], [12, 0], 99, 20 )

		variant_set = VariantSet()
		variant_set.add_family(my_family)

		variant_set.add_variant(variant)
		variant_set.add_variant(variant2)

		variant_set.get_candidate_compound_hets()
		variant_set.filter_compound_hets(include_denovo=False)
		variant_set.get_filtered_compound_hets_as_dict()

		self.assertCountEqual(variant_set.final_compound_hets, {'2:10G>A': None, '2:100G>A': None})

	def test_sibling_has_missing_genotypes(self):

		mum = FamilyMember('mum', 'FAM001', 2, False)
		dad = FamilyMember('dad', 'FAM001', 1, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, mum=mum, dad=dad)
		sibling = FamilyMember('sibling', 'FAM001', 1, False, mum=mum, dad=dad)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.add_family_member(sibling)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)
		variant.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		variant2 = Variant(chrom='2', pos=100, ref='G', alt='A')
		variant2.add_family(my_family)
		variant2.add_transcript_annotations([{'Feature': 'geneA','Consequence': 'missense_variant'}])

		# Test one from mum and one from dad
		variant.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [10, 2], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [12, 0], 99, 20 )
		variant.add_genotype('sibling', ['.', '.'], [12, 0], 99, 20 )

		variant2.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant2.add_genotype('mum', ['G', 'G'], [10, 2], 99, 20 )
		variant2.add_genotype('dad', ['G', 'A'], [12, 0], 99, 20 )
		variant2.add_genotype('sibling', ['.', '.'], [12, 0], 99, 20 )

		variant_set = VariantSet()
		variant_set.add_family(my_family)

		variant_set.add_variant(variant)
		variant_set.add_variant(variant2)

		variant_set.get_candidate_compound_hets()
		variant_set.filter_compound_hets(include_denovo=False)
		variant_set.get_filtered_compound_hets_as_dict()

		self.assertCountEqual(variant_set.final_compound_hets, {'2:10G>A': None, '2:100G>A': None})

class TestPedReader(unittest.TestCase):

	def test_read_csv(self):

		my_family = Family('FAM001')

		my_family.read_from_ped_file('test_data/FAM001.ped', 'FAM001', 'proband')


class TestPaternalUPDAmbiguous(unittest.TestCase):

	def test_trio_hom_ref_autosome(self):

		dad = FamilyMember('dad', 'FAM001', 1, False)
		mum = FamilyMember('mum', 'FAM001', 2, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, dad=dad, mum=mum)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['G', 'G'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['A', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [12, 0], 99, 20 )

		self.assertEqual(variant.matches_paternal_uniparental_ambiguous(), True)


	def test_trio_hom_alt_autosome(self):

		dad = FamilyMember('dad', 'FAM001', 1, False)
		mum = FamilyMember('mum', 'FAM001', 2, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, dad=dad, mum=mum)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['A', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [12, 0], 99, 20 )
		variant.add_genotype('dad', ['A', 'A'], [12, 0], 99, 20 )

		self.assertEqual(variant.matches_paternal_uniparental_ambiguous(), True)


	def test_trio_not_correct(self):

		dad = FamilyMember('dad', 'FAM001', 1, False)
		mum = FamilyMember('mum', 'FAM001', 2, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, dad=dad, mum=mum)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['A', 'G'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [12, 0], 99, 20 )
		variant.add_genotype('dad', ['A', 'A'], [12, 0], 99, 20 )

		self.assertEqual(variant.matches_paternal_uniparental_ambiguous(), False)

	def test_trio_not_correct2(self):

		dad = FamilyMember('dad', 'FAM001', 1, False)
		mum = FamilyMember('mum', 'FAM001', 2, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, dad=dad, mum=mum)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['A', '.'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [12, 0], 99, 20 )
		variant.add_genotype('dad', ['A', 'A'], [12, 0], 99, 20 )

		self.assertEqual(variant.matches_paternal_uniparental_ambiguous(), False)

	def test_trio_not_correct3(self):

		dad = FamilyMember('dad', 'FAM001', 1, False)
		mum = FamilyMember('mum', 'FAM001', 2, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, dad=dad, mum=mum)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['G', 'G'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [12, 0], 99, 20 )
		variant.add_genotype('dad', ['A', 'A'], [12, 0], 99, 20 )

		self.assertEqual(variant.matches_paternal_uniparental_ambiguous(), False)


class TestMaternalUPDAmbiguous(unittest.TestCase):

	def test_trio_hom_alt_autosome(self):

		dad = FamilyMember('dad', 'FAM001', 1, False)
		mum = FamilyMember('mum', 'FAM001', 2, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, dad=dad, mum=mum)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['A', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['A', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [12, 0], 99, 20 )

		self.assertEqual(variant.matches_maternal_uniparental_ambiguous(), True)


	def test_trio_hom_ref_autosome(self):

		dad = FamilyMember('dad', 'FAM001', 1, False)
		mum = FamilyMember('mum', 'FAM001', 2, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, dad=dad, mum=mum)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['G', 'G'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [12, 0], 99, 20 )
		variant.add_genotype('dad', ['A', 'A'], [12, 0], 99, 20 )

		self.assertEqual(variant.matches_maternal_uniparental_ambiguous(), True)


	def test_trio_not_correct(self):

		dad = FamilyMember('dad', 'FAM001', 1, False)
		mum = FamilyMember('mum', 'FAM001', 2, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, dad=dad, mum=mum)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['A', 'G'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [12, 0], 99, 20 )
		variant.add_genotype('dad', ['A', 'A'], [12, 0], 99, 20 )

		self.assertEqual(variant.matches_maternal_uniparental_ambiguous(), False)

	def test_trio_not_correct2(self):

		dad = FamilyMember('dad', 'FAM001', 1, False)
		mum = FamilyMember('mum', 'FAM001', 2, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, dad=dad, mum=mum)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['A', '.'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [12, 0], 99, 20 )
		variant.add_genotype('dad', ['A', 'A'], [12, 0], 99, 20 )

		self.assertEqual(variant.matches_maternal_uniparental_ambiguous(), False)

	def test_trio_not_correct3(self):

		dad = FamilyMember('dad', 'FAM001', 1, False)
		mum = FamilyMember('mum', 'FAM001', 2, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, dad=dad, mum=mum)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['A', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [12, 0], 99, 20 )
		variant.add_genotype('dad', ['A', 'A'], [12, 0], 99, 20 )

		self.assertEqual(variant.matches_maternal_uniparental_ambiguous(), False)


class TestPaternalUPDIsodisomy(unittest.TestCase):


	def test_trio_paternal_inheritance_ref(self):

		dad = FamilyMember('dad', 'FAM001', 1, False)
		mum = FamilyMember('mum', 'FAM001', 2, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, dad=dad, mum=mum)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['G', 'G'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['A', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('dad', ['A', 'G'], [12, 0], 99, 20 )

		self.assertEqual(variant.matches_paternal_uniparental_isodisomy(), True)


	def test_trio_paternal_inheritance_alt(self):

		dad = FamilyMember('dad', 'FAM001', 1, False)
		mum = FamilyMember('mum', 'FAM001', 2, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, dad=dad, mum=mum)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['A', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [12, 0], 99, 20 )
		variant.add_genotype('dad', ['A', 'G'], [12, 0], 99, 20 )

		self.assertEqual(variant.matches_paternal_uniparental_isodisomy(), True)

class TestMaternalUPDIsodisomy(unittest.TestCase):


	def test_trio_paternal_inheritance_ref(self):

		dad = FamilyMember('dad', 'FAM001', 1, False)
		mum = FamilyMember('mum', 'FAM001', 2, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, dad=dad, mum=mum)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['G', 'G'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['A', 'G'], [12, 0], 99, 20 )
		variant.add_genotype('dad', ['A', 'A'], [12, 0], 99, 20 )

		self.assertEqual(variant.matches_maternal_uniparental_isodisomy(), True)


	def test_trio_paternal_inheritance_alt(self):

		dad = FamilyMember('dad', 'FAM001', 1, False)
		mum = FamilyMember('mum', 'FAM001', 2, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, dad=dad, mum=mum)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['A', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['A', 'G'], [12, 0], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [12, 0], 99, 20 )

		self.assertEqual(variant.matches_maternal_uniparental_isodisomy(), True)


class TestAllelesIdenticalToDad(unittest.TestCase):

	def test_is_identical_to_dad(self):

		dad = FamilyMember('dad', 'FAM001', 1, False)
		mum = FamilyMember('mum', 'FAM001', 2, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, dad=dad, mum=mum)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['G', 'G'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['A', 'G'], [12, 0], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [12, 0], 99, 20 )

		self.assertEqual(variant.alleles_identical_to_dad(), True)

	def test_is_identical_to_dad2(self):

		dad = FamilyMember('dad', 'FAM001', 1, False)
		mum = FamilyMember('mum', 'FAM001', 2, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, dad=dad, mum=mum)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['G', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['A', 'G'], [12, 0], 99, 20 )
		variant.add_genotype('dad', ['A', 'G'], [12, 0], 99, 20 )

		self.assertEqual(variant.alleles_identical_to_dad(), True)


class TestBiparentalInheritance(unittest.TestCase):


	def test_biparental_true_ref(self):

		dad = FamilyMember('dad', 'FAM001', 1, False)
		mum = FamilyMember('mum', 'FAM001', 2, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, dad=dad, mum=mum)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['A', 'G'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['A', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('dad', ['G', 'G'], [12, 0], 99, 20 )

		self.assertEqual(variant.is_biparental_inheritance(), True)

	def test_biparental_true_ref(self):

		dad = FamilyMember('dad', 'FAM001', 1, False)
		mum = FamilyMember('mum', 'FAM001', 2, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, dad=dad, mum=mum)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['A', 'G'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'G'], [12, 0], 99, 20 )
		variant.add_genotype('dad', ['A', 'A'], [12, 0], 99, 20 )

		self.assertEqual(variant.is_biparental_inheritance(), True)

	def test_biparental_false_ref(self):

		dad = FamilyMember('dad', 'FAM001', 1, False)
		mum = FamilyMember('mum', 'FAM001', 2, False)
		proband = FamilyMember('proband', 'FAM001', 1, True, dad=dad, mum=mum)
		my_family = Family('FAM001')
		my_family.add_family_member(dad)
		my_family.add_family_member(mum)
		my_family.add_family_member(proband)
		my_family.set_proband(proband.get_id())

		variant = Variant(chrom='2', pos=10, ref='G', alt='A')
		variant.add_family(my_family)

		variant.add_genotype('proband', ['A', 'G'], [12, 0], 99, 20 )
		variant.add_genotype('mum', ['G', 'A'], [12, 0], 99, 20 )
		variant.add_genotype('dad', ['A', 'A'], [12, 0], 99, 20 )

		self.assertEqual(variant.is_biparental_inheritance(), False)


if __name__ == '__main__':
	unittest.main()



































