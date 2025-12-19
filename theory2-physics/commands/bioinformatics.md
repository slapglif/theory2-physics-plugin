---
name: bioinformatics
description: Bioinformatics analysis (Biopython) - sequence, protein, and structure analysis
argument-hint: <operation> [options]
allowed-tools:
  - Bash
  - Read
---

# Theory2 Bioinformatics

Analyze DNA, RNA, protein sequences, and 3D protein structures using Biopython.

## Sequence Analysis

### Analyze Sequence

Analyze DNA, RNA, or protein sequences for basic properties:

```bash
# DNA sequence analysis
/home/mikeb/theory2/.venv/bin/theory --json bioinformatics analyze-sequence \
  --sequence="ATGCGATCGATCG"

# Protein sequence analysis (auto-detected)
/home/mikeb/theory2/.venv/bin/theory --json bioinformatics analyze-sequence \
  --sequence="MVLSPADKTNVK" --seq-type=protein --explain

# RNA sequence
/home/mikeb/theory2/.venv/bin/theory --json bioinformatics analyze-sequence \
  --sequence="AUGCGAUCGAUCG" --seq-type=rna
```

**Parameters:**
- `--sequence`: DNA/RNA/Protein sequence string (required)
- `--seq-type`: `auto`, `dna`, `rna`, or `protein` (default: auto)
- `--explain`: Include detailed explanation
- `--json`: Output as JSON

**Returns:**
- Sequence type (DNA, RNA, or protein)
- Length in residues/nucleotides
- Composition (base/amino acid counts)
- Molecular weight (Da)
- GC content (for DNA/RNA only)

### Translate DNA

Translate DNA sequences to protein using genetic code tables:

```bash
# Standard genetic code (table 1)
/home/mikeb/theory2/.venv/bin/theory --json bioinformatics translate-dna \
  --sequence="ATGGCTAGCTAG"

# Mitochondrial genetic code (table 2)
/home/mikeb/theory2/.venv/bin/theory --json bioinformatics translate-dna \
  --sequence="ATGGCTAGCTAG" --table=2
```

**Parameters:**
- `--sequence`: DNA sequence to translate (required)
- `--table`: Codon table (1=Standard, 2=Mitochondrial, default: 1)
- `--json`: Output as JSON

**Returns:**
- Original DNA sequence
- Translated protein sequence
- Amino acid count
- Codon table used

### Find ORFs

Find Open Reading Frames (ORFs) in DNA sequences:

```bash
# Find ORFs with default 100bp minimum
/home/mikeb/theory2/.venv/bin/theory --json bioinformatics find-orfs \
  --sequence="ATGAAATAG..." --min-length=100

# Find shorter ORFs (50bp minimum)
/home/mikeb/theory2/.venv/bin/theory --json bioinformatics find-orfs \
  --sequence="ATGAAATAG..." --min-length=50
```

**Parameters:**
- `--sequence`: DNA sequence to search (required)
- `--min-length`: Minimum ORF length in nucleotides (default: 100)
- `--json`: Output as JSON

**Returns:**
- Number of ORFs found
- ORF list (up to 20) with:
  - Start position
  - End position
  - Length
  - Frame
  - Sequence

## Protein Analysis

### Analyze Protein

Compute detailed protein properties:

```bash
# Full protein analysis with explanation
/home/mikeb/theory2/.venv/bin/theory --json bioinformatics analyze-protein \
  --sequence="MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSH" \
  --explain
```

**Parameters:**
- `--sequence`: Protein sequence (one-letter amino acid codes, required)
- `--explain`: Include detailed explanation
- `--json`: Output as JSON

**Returns:**
- Length (amino acids)
- Molecular weight (Da)
- Isoelectric point (pI)
- Instability index (<40 = stable)
- GRAVY score (hydropathicity)
- Aromaticity
- Amino acid composition (%)

**Interpretation:**
- **Instability index < 40**: Protein is stable in test tube
- **GRAVY > 0**: Hydrophobic protein
- **GRAVY < 0**: Hydrophilic protein

### Find Domains

Search for protein domains/motifs using PROSITE-like patterns:

```bash
# Search for common domains
/home/mikeb/theory2/.venv/bin/theory --json bioinformatics find-domains \
  --sequence="MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSH"
```

**Parameters:**
- `--sequence`: Protein sequence to search (required)
- `--json`: Output as JSON

**Returns:**
- Number of domains found
- Domain list with:
  - Domain ID
  - Domain name (e.g., N-glycosylation site, PKC phosphorylation)
  - Start position
  - End position
  - Sequence
  - Score/confidence

**Searches for:**
- N-glycosylation sites
- PKC phosphorylation sites
- Casein kinase II phosphorylation
- Myristoylation sites
- And other PROSITE patterns

### Align Sequences

Perform pairwise sequence alignment:

```bash
# Global alignment (Needleman-Wunsch)
/home/mikeb/theory2/.venv/bin/theory --json bioinformatics align-sequences \
  --seq1="ACGT" --seq2="AGCT" --alignment-type=global

# Local alignment (Smith-Waterman)
/home/mikeb/theory2/.venv/bin/theory --json bioinformatics align-sequences \
  --seq1="ACGTACGTACGT" --seq2="CGTACGTA" --alignment-type=local
```

**Parameters:**
- `--seq1`: First sequence (required)
- `--seq2`: Second sequence (required)
- `--alignment-type`: `global` or `local` (default: global)
- `--json`: Output as JSON

**Returns:**
- Alignment type
- Alignment score
- Sequence identity (%)
- Aligned sequence 1 (with gaps)
- Aligned sequence 2 (with gaps)
- Number of gaps

**Alignment Types:**
- **Global**: Needleman-Wunsch - aligns entire sequences
- **Local**: Smith-Waterman - finds best local match

## Structure Analysis

### Load Structure

Load and analyze PDB structure files:

```bash
# Load PDB structure
/home/mikeb/theory2/.venv/bin/theory --json bioinformatics load-structure \
  --pdb-file="/path/to/1abc.pdb"
```

**Parameters:**
- `--pdb-file`: Path to PDB structure file (required)
- `--json`: Output as JSON

**Returns:**
- PDB ID
- Number of models
- Number of chains
- Number of residues
- Number of atoms
- Chain IDs
- Resolution (if available)

### Find Contacts

Find atomic contacts within a structure:

```bash
# Find contacts within 4.0 Å
/home/mikeb/theory2/.venv/bin/theory --json bioinformatics find-contacts \
  --pdb-file="/path/to/1abc.pdb" --cutoff=4.0

# Find contacts in specific chain
/home/mikeb/theory2/.venv/bin/theory --json bioinformatics find-contacts \
  --pdb-file="/path/to/1abc.pdb" --cutoff=5.0 --chain=A
```

**Parameters:**
- `--pdb-file`: Path to PDB structure file (required)
- `--cutoff`: Distance cutoff in Angstroms (default: 4.0)
- `--chain`: Filter by chain ID (optional)
- `--json`: Output as JSON

**Returns:**
- Number of contacts
- Cutoff distance used
- Contact list (up to 50) with:
  - Residue 1 details (name, number, chain)
  - Residue 2 details
  - Atom 1 name
  - Atom 2 name
  - Distance (Å)

### Analyze Binding Site

Analyze residues around a potential binding site:

```bash
# Analyze 8Å radius around residue 100 in chain A
/home/mikeb/theory2/.venv/bin/theory --json bioinformatics analyze-binding-site \
  --pdb-file="/path/to/1abc.pdb" --center-residue=100 --chain=A --radius=8.0

# Larger binding site (10Å)
/home/mikeb/theory2/.venv/bin/theory --json bioinformatics analyze-binding-site \
  --pdb-file="/path/to/1abc.pdb" --center-residue=150 --chain=B --radius=10.0
```

**Parameters:**
- `--pdb-file`: Path to PDB structure file (required)
- `--center-residue`: Central residue number (required)
- `--chain`: Chain ID (default: A)
- `--radius`: Search radius in Angstroms (default: 8.0)
- `--json`: Output as JSON

**Returns:**
- Center residue details
- Number of nearby residues
- Nearby residue list with:
  - Residue name
  - Residue number
  - Chain ID
  - Distance from center (Å)
  - Residue type classification

## Expected Output Format

All commands return structured JSON:

```json
{
  "status": "success",
  "result": {
    // Command-specific results
  },
  "metadata": {
    "tool": "Biopython",
    "method": "Analysis method",
    "timestamp": "ISO-8601",
    "duration_ms": 123,
    "gpu_used": false
  },
  "provenance": {
    "method": "Description",
    "inputs": {...},
    "library": "Bio.X.Y"
  },
  "next_actions": [
    "Suggested next steps"
  ]
}
```

## Dependencies

All bioinformatics commands require Biopython:

```bash
# Install Biopython
uv pip install biopython
```

## Common Workflows

### Gene Discovery Pipeline

```bash
# 1. Find ORFs in genomic DNA
theory --json bioinformatics find-orfs \
  --sequence="..." --min-length=300

# 2. Translate ORF to protein
theory --json bioinformatics translate-dna \
  --sequence="ORF_SEQUENCE"

# 3. Analyze protein properties
theory --json bioinformatics analyze-protein \
  --sequence="TRANSLATED_PROTEIN" --explain

# 4. Find functional domains
theory --json bioinformatics find-domains \
  --sequence="TRANSLATED_PROTEIN"
```

### Sequence Comparison

```bash
# 1. Analyze both sequences
theory --json bioinformatics analyze-sequence --sequence="SEQ1"
theory --json bioinformatics analyze-sequence --sequence="SEQ2"

# 2. Align sequences
theory --json bioinformatics align-sequences \
  --seq1="SEQ1" --seq2="SEQ2" --alignment-type=global
```

### Structure-Function Analysis

```bash
# 1. Load structure
theory --json bioinformatics load-structure --pdb-file="protein.pdb"

# 2. Identify binding site
theory --json bioinformatics analyze-binding-site \
  --pdb-file="protein.pdb" --center-residue=100 --radius=10

# 3. Find contacts within binding site
theory --json bioinformatics find-contacts \
  --pdb-file="protein.pdb" --cutoff=5.0 --chain=A
```

## Python API

```python
from bioinformatics.sequence_analysis import (
    analyze_sequence,
    translate_dna,
    find_orfs,
    align_sequences
)
from bioinformatics.protein_analysis import (
    analyze_protein,
    find_domains
)
from bioinformatics.structure_analysis import (
    load_pdb_structure,
    find_contacts,
    analyze_binding_site
)

# Sequence analysis
seq_result = analyze_sequence("ATGCGATCG", seq_type="dna")

# Protein analysis
protein_result = analyze_protein("MVLSPADK")

# Structure analysis
structure = load_pdb_structure("protein.pdb")
contacts = find_contacts("protein.pdb", cutoff=4.0)
```
