# ChEC In Vitro Analysis Pipeline for Hybrid Genome

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
1. **outFilesLoc.txt**: A text file with paths to the required inputs, and location to save the outputs. Example format provided in the repository
2. **Genome Information Files**: All provided in the repository
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
3. **Sum Prom**: Saved in `SumPromRepeats/` as compressed `.gz` files.
- As both species of yeast are very closely related, there is an equivalence of promoters. We sum over the normalised signal along the promoter lengths, and further normalise this according to promoter length. This is then stored as the signal over the promoter (SumProm) value. Each file contains two columns: `Cer` (counts for *S. cerevisiae*) and `Par` (counts for *S. paradoxus*).
---


## Setup:
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
---


## How to run:
1. **Clone the repository**:
```bash
git clone https://github.com/divz-k/OutFileAnalysisForHybridGenome.git
cd OutFileAnalysisForHybridGenome
```
2. Set up directories and ensure all required input files are correctly placed. Fill in outFilesLoc.txt to the appropriate file paths.
   - `outFilesLoc.txt`
   - `genomeInfo/` containing:
     - `cerChrLen.xlsx`
     - `parChrLen.xlsx`
     - `cerProm.xlsx`
     - `parProm.xlsx`
   - `outFiles/` containing:
     - `.out` files
     - `WellList.xlsx`

3. Run the script:
   ```bash
   python3 outFilesPipeline.py

## Acknowledgements
Analysis used in the pipeline, such as RawProfiles refining, Normalisation, Promoter signal calculation was developed in the Barkai lab. 
This project is done as a part of the Python Course at WIS by Gabor Sabor: [link to couse repository](https://github.com/szabgab/wis-python-course-2024-11)
