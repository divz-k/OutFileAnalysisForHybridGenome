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

## Understanding the pipeline

### What do we need from the pipeline?

Post demultiplexing, we get `.out` files, that are named according to their barcodes. Each file is an array, as long as the genome it was aligned with, and at each position, it contains the total number of sequencing reads obtained. To meaningfully process this data, we must:
1. Assign appropriate sample names, and replacing the barcode name 
2. Filter unwanted genomic regions (e.g., subtelomeric regions, mitochondrial DNA, and repetitive sequences).
3. Normalise read counts to account for sequencing depth differences.
4. Summarise TF binding signals at promoter regions for meaningful comparison across samples.
5. Organise results in structured output files for downstream statistical and visualization analyses.
Performing these tasks manually for multiple experiments is time-consuming and error-prone. Therefore, we require an automated computational pipeline to efficiently process and analyze the data.


### What Does This Pipeline Do?

1. **Sample Organisation**:
    - Finds the `.out` files, and all the other required file locations from outFilesLoc.txt
    - Reads the naming file called "WellList.xlsx" that matches the barcodes to the sample names
    - Reads the `.out` files, names them appropritately and saves this in a usable yet compressed format (pickle.gz) , in an organised file.
2. **Filtering and Normalisation**:
    - Removes unwanted genomic regions (e.g., subtelomeric regions, mitochondrial DNA, CUP1 locus) 
    - Normalises read counts to total sequencing depth per sample, allowing direct comparisons.
3. **Promoter Signal Summation**:
    - Sums the normalized signals over defined promoter regions (provided in the repository) and further adjusts summed signal for promoter length.

This pipeline automates the processing of ChEC sequencing data, reducing the need for manual intervention and enabling overnight batch analysis. It ensures:
1. Efficiency and Scalability: Processes large datasets by a single code
2. Reproducibility: Standardized data handling across multiple experiments.
3. File Organisation: We can keep adding new out Files and run the code, but all the resulting samples will be neatly organised into pre-defined folders.


---

## What are the files in the repository?

### Input Files:
1. `outFilesLoc.txt`: A text file with paths to the required inputs, and location to save the outputs. Example format provided in the repository
2. **Genome Information Files**: All provided in the repository
- `cerChrLen.xlsx`: Chromosome lengths for *S. cerevisiae*.
- `parChrLen.xlsx`: Chromosome lengths for *S. paradoxus*.
- `cerProm.xlsx`: Promoter information for *S. cerevisiae*.
- `parProm.xlsx`: Promoter information for *S. paradoxus*.
3. **Raw `.out` Files**: Alignment results containing read counts across genome positions.
4. `WellList.xlsx`: A mapping of well identifiers to sample names.

### Output Files:
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
2. Set up directories.
   - `outFilesLoc.txt`
   - `genomeInfo/` containing:
     - `cerChrLen.xlsx`
     - `parChrLen.xlsx`
     - `cerProm.xlsx`
     - `parProm.xlsx`
   - `outFiles/` containing:
     - `.out` files
     - `WellList.xlsx`
    
3. Ensure input files are correctly placed:
   - Fill in outFilesLoc.txt to the appropriate file paths.
   - Copy the `.out` files to the 'outFiles' folder
   - Edit the WellList.xlsx to match the correct file names (barcode) to the sample names

4. Run the script:
   ```bash
   python3 outFilesPipeline.py

---

## Example/ Test Run 

With this repository, I have provided example files that can help you test the working of this pipeline. 
-- Setup the directories as described above (just clone the repository, you should have everything in it)
-- From the ExampleFiles folder, copy the outFiles folder. This contains the corresponding WellList.xlsx file too.
-- From the ExampleFiles folder, copy the outFilesLoc.txt. In this text document, edit the folder paths. This will change according to your home directory, and where you cloned this repository.
-- Run the script on bash/zsh
-- Go the ExampleFiles folder, where there is a script called exampleCheck.py. Write down the appropriate SumPromRepeats file paths (to the one you created new, and the ones I have attached in the ExampleFiles folder). 
-- Run this exampleCheck.py script. As the SumPromRepeats are created at the end of the analysis, if this is identical, it means the RawProfileRepeats and NormProfileRepeats are also identical. 



## Acknowledgements
Analysis used in the pipeline, such as RawProfiles refining, Normalisation, Promoter signal calculation was developed in the Barkai lab. 
This project is done as a part of the Python Course at WIS by Gabor Sabor: [link to couse repository](https://github.com/szabgab/wis-python-course-2024-11)
