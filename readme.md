# PyVariantFilter

Versatile Python package for filtering germline genetic variants based on inheritance pattern. 

 * Find Autosomal Dominant, Autosomal Reccessive, X Linked Reccessive, X Linked Dominant, De Novo and Compound Heterozygous variants in your dataset.

 * Filter variants by their annotations by applying custom python filtering functions.

 * Convert VEP annotated VCFs to Pandas DataFrames.

## Quick Start

```python
from pyvariantfilter.family import Family
from pyvariantfilter.variant_set import VariantSet

# Create a Family object describing the relationships between samples as well as their sex and affected status
my_family = Family('FAM001')
my_family.read_from_ped_file(ped_file_path='test_data/NA12878.ped', family_id='FAM001', proband_id='NA12878i')

# Associate a VariantSet object with a the Family object we just created
my_variant_set = VariantSet()
my_variant_set.add_family(my_family)

# Read variants from a standard VCF and apply initial filtering function
my_variant_set.read_variants_from_vcf('test_data/NA12878.trio.vep.vcf', proband_variants_only=True, filter_func=import_filter, args=(new_family.get_proband_id(),) )

# Get candidate compound hets
my_variant_set.get_candidate_compound_hets()

# Filter the compound hets by phasing them using parental information
my_variant_set.filter_compound_hets()

# Flatten the compound hets to a dictionary with each compound het as a key
my_variant_set.get_filtered_compound_hets_as_dict()

# Create Pandas Dataframe
df = my_variant_set.to_df()

# Filter to view variants matching any inheritiance model.
df[['variant_id', 'worst_consequence','inheritance_models', 'csq_SYMBOL' ]][df['inheritance_models'] != ''].head()


```

Where the filter\_func argument to read\_variants\_from\_vcf() is something like the function below.

```python
def import_filter(variant, proband_id):
    
    if variant.has_alt(proband_id) and variant.passes_gt_filter(proband_id) and variant.passes_filter():
        
        freq_filter = variant.filter_on_numerical_transcript_annotation_lte(annotation_key='gnomAD_AF',
                                                                                          ad_het=0.01,
                                                                                          ad_hom_alt=0.01,
                                                                                          x_male =0.01,
                                                                                          x_female_het=0.01,
                                                                                          x_female_hom=0.01,
                                                                                          compound_het=0.01,
                                                                                          y=0.01,
                                                                                          mt=0.01,
                                                                                          )

        
        csq_filter = False
    
        if variant.get_worst_consequence() in {'transcript_ablation': None,
                                               'splice_acceptor_variant': None,
                                               'splice_donor_variant': None,
                                               'stop_gained': None,
                                               'frameshift_variant': None,
                                               'stop_lost': None,
                                               'start_lost': None}:
        
            csq_filter = True
        
        
        if csq_filter and freq_filter:
            
            return True
        
    return False

```

## Input Requirements

When using the VariantSet classes read from vcf functions a decomposed (Split Multiallelic Variants) and VEP annotated VCF is required. 

Both GATK and Platypus VCFs are supported.

Use VT and VEP with the following commands to preprocess your VCF before analysing.

* https://github.com/atks/vt
* https://github.com/Ensembl/ensembl-vep

Annotation with VEP is only neccecary if you want to find compound hets.

```
# split multiallellics and normalise
cat input.vcf | vt decompose -s - | vt normalize -r reference.fasta - > input.norm.vcf

# Annotate with VEP
vep --verbose --format vcf --everything --fork 1 --species homo_sapiens --assembly GRCh37 --input_file input.norm.vcf \
--output_file input.norm.vep.vcf --force_overwrite --cache --dir vep_cache_location \
--fasta reference.fasta --offline --cache_version 94 -no_escape --shift_hgvs 1 --exclude_predicted --vcf --refseq --flag_pick \
--custom gnomad.genomes.vcf.gz,gnomADg,vcf,exact,0,AF_POPMAX  \
--custom gnomad.exomes.vcf.gz,gnomADe,vcf,exact,0,AF_POPMAX \

```

## Inheritance Models

A lot of the rules here have been adapted from the GEMINI software which is worth checking out. https://gemini.readthedocs.io/en/latest/

### Autosomal Dominant

1) Variant must be on an autosome.

2) All affected samples must be heterozygous or missing e.g. ./. See lenient option to allow homozygous alternate genotypes in affected samples other than the proband.

3) If the variant is not in a low penetrant gene then all unaffected samples must be homozygous reference or have a missing genotype.


### Autosomal Reccessive

1) Variant must be on an Autosome.

2) All affected samples must be homozygous for the alternate allele. Can be missing.

3) No unaffected samples can be homozygous for the alternate allele. Can be missing.

### X-Linked Reccessive

1) Variant must be on the X chromosome.

2) All affected female samples must be homozygous for the alternate allele or missing.

3) No unaffected female samples can be homozygous for the alternate allele.

4) All affected male samples must have the variant or be missing.

5) No unaffected male samples can have the variant.

### X-Linked Dominant

1) Variant must be on the X chromosome.

2) The daughters of affected male samples must be affected.

3) The sons of affected males must not be affected.

4) Affected male samples must have the variant or be missing.

5) Affected female samples  must be heterozygous or be missing.

6) Unaffected samples must not have the variant.

### De Novo

1) Variant must be in the proband and not in either parent.

2) Parents must have a GQ value above min\_parental\_gq.

3) Parents must have a DP value above min\_parental\_depth.

4) Parents must have a alt/ref ratio below max\_parental\_alt\_ref\_ratio.


### Compound Heterozygous

1) No unaffected samples can have the pair of variants. Can be adjusted using the allow\_hets\_in\_unaffected argument.

2) All affected samples must have the pair of variants or be missing the genotype data. Can be adjusted using the check_affected argument.

3) 

a) One of the pair must be inherited from mum and the other from dad.

b) If include_denovo is True then one of the pair can be de_novo and the other inherited from either parent or both can be de_novo. There are no minimum requirements e.g. depth on the de_novo calls.


## Install

### Requirements

* Python 3.6 or greater
* Pysam 0.15.0
* Pandas 0.23.4

### Install the Package

`pip install pyvariantfilter ` TO DO

or

`git clone https://github.com/josephhalstead/pyvariantfilter.git `

## Examples

See the notebooks folder for some examples of using the library for WES and WGS analyses.

## Documentation

See the docs directory.

## Test

`python tests.py`






















