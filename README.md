# ChEC In Vitro Analysis Pipeline

This project provides a streamlined method for analyzing ChEC (Chromatin Endogenous Cleavage) data. It processes the output files generated after demultiplexing and produces normalized, structured data for further analysis. The pipeline is specifically adapted for in vitro studies of transcription factor (TF) binding sites in *Saccharomyces cerevisiae* and *Saccharomyces paradoxus* genomes.

---

## What Does This Project Do?

The pipeline:
1. Processes `.out` files (post-demultiplexing).
2. Identifies and removes unwanted genomic regions (e.g., subtelomeric regions, mitochondrial DNA, and specific genes like CUP1).
3. Normalizes read counts for each sample.
4. Calculates the sum of signal on promoters (probably will add more features)
5. Saves the processed data in well organised target folders as compressed files (`.gz`) for easy access.

This pipeline is especially useful for analyzing TF binding data across two genomes (*S. cerevisiae* and *S. paradoxus*) in parallel, enabling insights into TF binding patterns and carryover DNA.

---

## Input and Output

### Input:
1. **outFilesLoc.txt**: A text file with paths to various directories and files. Example format provided in the repository
2. **Genome Information Files**:
- `cerChrLen.xlsx`: Chromosome lengths for *S. cerevisiae*.
- `parChrLen.xlsx`: Chromosome lengths for *S. paradoxus*.
- `cerProm.xlsx`: Promoter information for *S. cerevisiae*.
- `parProm.xlsx`: Promoter information for *S. paradoxus*.
3. **Raw `.out` Files**: Alignment results containing read counts across genome positions.
4. **WellList.xlsx**: A mapping of well identifiers to sample names.

### Output:
1. **Raw Profiles**: Saved in `RawProfilesRepeats/` as compressed `.gz` files.
- Each file contains two columns: `Cer` (counts for *S. cerevisiae*) and `Par` (counts for *S. paradoxus*).
2. **Norm Profiles**: Saved in `NormProfilesRepeats/` as compressed `.gz` files.
- The reads are normalised to the total reads obtained in this sample, thus ensuring that different samples can be compared. Each file contains two columns: `Cer` (counts for *S. cerevisiae*) and `Par` (counts for *S. paradoxus*).
3. **Sum Prom**: Saved in `NormProfilesRepeats/` as compressed `.gz` files.
- As both species of yeast are very closely related, there is an equivalence of promoters. We sum over the normalised signal along the promoter lengths, and further normalise this according to promoter length. This is then stored as the signal over the promoter (SumProm) value. Each file contains two columns: `Cer` (counts for *S. cerevisiae*) and `Par` (counts for *S. paradoxus*).
---

## Setup

### Prerequisites:
1. **Python Environment**: Ensure you have Python 3.8+ installed.
2. **Dependencies**:
- `numpy`
- `pandas`
- `openpyxl`

Install them using:
```bash
pip install numpy pandas openpyxl
```
3. (Optional) Environment: Use the provided environment file: OutFileAnalysisEnv

