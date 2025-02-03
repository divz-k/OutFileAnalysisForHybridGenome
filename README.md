# Pipeline for processing *in vitro* ChEC seq data

This manual provides step-by-step instructions for setting up and running the ChEC *In Vitro* Analysis Pipeline. The pipeline automates the processing of sequencing data to analyze transcription factor (TF) binding in a hybrid genome system.


### Scientific Background

ChEC (Chromatin Endogenous Cleavage) sequencing is a powerful method for mapping protein-DNA interactions *in vivo*. Our protein of interest is tagged with an MNase (Micrococcal nuclease), which is a nuclease that can cut the DNA in the presence of calcium. At the required conditions, we add calcium to the system, thus enabling the MNase to cut around the protein binding sites, thus producing short DNA fragments. These fragments are then sequenced to determine the binding sites.
ChEC seq has high reproducibility and base specific resolution. 
At the Barkai lab, we want to test TF (transcription factor) binding in *in vitro*, to truly isolate TF effects from its cellular environment. We have adapted this experimental ChEC seq protocol *in vitro*. Our protocol involves isolating the TF from *Saccharomyces cerevisiae*, and testing the binding to *Saccharomyces paradoxus* genome in a cell free system. 


### Why is this pipeline useful?
This pipeline provides a streamlined method for analyzing *in vitro* ChEC (Chromatin Endogenous Cleavage) data. It processes the output files generated after demultiplexing and produces normalized, structured data for further analysis. 
As we typically do many experiments in a high throughput fashion, and rarely change experimental methods, this pipeline will be highly benificial for me in my PhD, and for further students performing this experiment and analysis. This automates multiple steps into a single run line, therefore, we can let the analysis of many large samples run overnight, and come back the next morning to clearly organised files, ready for deeper analysis. 
This pipeline is also unique, as:
1. Unlike other pipelines, this analysis also allows analysis on carry-over DNA from the *Saccharomyces cerevisiae*, thus enabling us to understand protein binding strength to native DNA, and also quality check experimental conditions.
2. We perform high-throuput experiments, and now we have to analyse with two genomes, this has increased the load and the time required to do individual steps. Such a pipeline that can automate the basic repeatable processes, that must happen every time we do this experiment, can save a lot of time and effort.


---

### Problem Statement

In our high-throughput experimental setup, we generate large sequencing datasets that require extensive preprocessing. This includes:

1. Filtering unwanted genomic regions (e.g., subtelomeric regions, mitochondrial DNA, and repetitive sequences).
2. Normalizing read counts to account for sequencing depth differences.
3. Summarizing TF binding signals at promoter regions for meaningful comparison across samples.
4. Organizing results in structured output files for downstream statistical and visualization analyses.

Performing these tasks manually for multiple experiments is time-consuming and error-prone. Therefore, we require an automated computational pipeline to efficiently process and analyze the data.

---
### What Does This Pipeline Do?

1. Processes `.out` files (post-demultiplexing).
2. Identifies and removes unwanted genomic regions (e.g., subtelomeric regions, mitochondrial DNA, and specific genes like CUP1).
3. Normalizes read counts for each sample.
4. Calculates the sum of signal on promoters (probably will add more features)
5. Saves the processed data in well organised target folders as compressed files (`.gz`) for easy access.

This pipeline automates the processing of ChEC sequencing data, reducing the need for manual intervention and enabling overnight batch analysis. It ensures:
1. Efficiency: Processes large datasets by a single code
2. Reproducibility: Standardized data handling across multiple experiments.
3. Scalability: Adapts to growing datasets.

---

## Computationl workflow

### Outline
1. **Input Handling**: Reads required input files from outFilesLoc.txt, which specifies paths for input and output data.
2. **Filtering**: Unwanted genomic regions (e.g., subtelomeric regions, mitochondrial DNA, CUP1 locus) are removed based on predefined lists.
3. **Normalization**: Read counts are normalized to total sequencing depth per sample, allowing direct comparisons.
4. **Promoter Summation**: Normalized signals are summed over promoter regions and further adjusted for promoter length.
5. **File Organization**: Processed results are stored in structured folders for easy access and future analysis.

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
- Here, we refine the The reads are normalised to the total reads obtained in this sample, thus ensuring that different samples can be compared. Each file contains two columns: `Cer` (counts for *S. cerevisiae*) and `Par` (counts for *S. paradoxus*).
3. **Sum Prom**: Saved in `SumPromRepeats/` as compressed `.gz` files.
- As both species of yeast are very closely related, there is an equivalence of promoters. We sum over the normalised signal along the promoter lengths, and further normalise this according to promoter length. This is then stored as the signal over the promoter (SumProm) value. Each file contains two columns: `Cer` (counts for *S. cerevisiae*) and `Par` (counts for *S. paradoxus*).
---


## Instruction Manual:

### Setup
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


### How to run:

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
