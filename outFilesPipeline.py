import numpy as np
import pandas as pd
import os
import pickle
import glob
import re


with open("outFilesLoc.txt", "r") as file:
           locs ={}
           for l in file:
                l=re.sub(r"\s+", "", l)
                l=l.strip()
                varType, pathAddress = l.replace(" ", "").split("=")
                locs[varType] = pathAddress



## get names of all the samples
fullFileNames = glob.glob(os.path.join(locs['outFilesLoc'], '*.out'))
wellList = pd.read_excel(os.path.join(locs['outFilesLoc'], 'WellList.xlsx'),engine='openpyxl')



####################    get Raw values for all  ######################

# Correct the sample name
for i,name in enumerate(fullFileNames):  
    currFileName = name.replace(locs['outFilesLoc'], '')[:8] 
    if currFileName in wellList['Well'].values:
        currSampleName = wellList.loc[wellList['Well'] == currFileName, 'Name'].values[0]
    else:
        currSampleName = currFileName
    currOut = pd.read_csv(name, header=None)
     
# Separate to Cer and Par
    totalCerPar=[]
    cer_values = currOut.loc[:12157105].reset_index(drop=True)
    par_values = currOut.loc[12157105:].reset_index(drop=True)
    currRaw= pd.concat([cer_values, par_values], axis=1)
    currRaw.columns = ["Cer", "Par"]

# Save
    folderPathRaw = locs['resultsFileLoc']+'RawProfilesRepeats/'
    os.makedirs(folderPathRaw, exist_ok=True)
    currRaw.to_pickle(folderPathRaw + currSampleName +'_raw.gz', compression='gzip')  # Save with index
    del cer_values, par_values, totalCerPar, currOut    




###############   Normalise #################

#delete cup1, subtel genes and mitochonrial
chrLenSC = pd.read_excel(os.path.join(locs['genomeInfoLoc'], 'cerChrLen.xlsx'), header=None, engine='openpyxl')
chrLenSC= np.cumsum(chrLenSC.to_numpy())
chrLenSP = pd.read_excel(os.path.join(locs['genomeInfoLoc'], 'parChrLen.xlsx'), header=None, engine='openpyxl')
chrLenSP= np.cumsum(chrLenSP.to_numpy())
delCer = chrLenSC[11] + np.arange(451599,468930);
delPar = chrLenSP[12] + np.arange(443941,461298);

for i,name in enumerate(wellList['Name'].values):

    currRaw = pd.read_pickle( folderPathRaw+ name+ '_raw.gz' , compression='gzip')
    
    currRawCopy = currRaw.copy()
    currNorm = currRaw.copy()
    currRawCopy.Cer.iloc[delCer]= pd.Series(np.full(len(delCer), np.nan))
    currRawCopy.Par.iloc[delPar]= pd.Series(np.full(len(delPar), np.nan))
    currNorm.Cer = (currRaw.Cer)*12000000/(currRawCopy.Cer.sum())
    currNorm.Par = (currRaw.Par)*12000000/(currRawCopy.Par.sum())
    
    # Save
    folderPathNorm = locs['resultsFileLoc']+'NormProfilesRepeats/'
    os.makedirs(folderPathNorm, exist_ok=True)
    currNorm.to_pickle(folderPathNorm + name +'_norm.gz', compression='gzip') 
    del currRawCopy, currRaw, currNorm



###############   Signal on Promoters- SumProm #################

#load promoter Parameters
promIdxCer = pd.read_excel(os.path.join(locs['genomeInfoLoc'], 'cerProm.xlsx'), engine='openpyxl')
promIdxCer = promIdxCer.apply(pd.to_numeric, errors='coerce')  # Convert all numeric values

promIdxPar = pd.read_excel(os.path.join(locs['genomeInfoLoc'], 'parProm.xlsx'), engine='openpyxl')
promIdxPar = promIdxPar.apply(pd.to_numeric, errors='coerce')  # Convert all numeric values

#Sumprom 
for i,name in enumerate(wellList['Name'].values):
 
    sumPromCer = np.full([6701], np.nan)
    sumPromPar = np.full([6701], np.nan)
    currNorm = pd.read_pickle(folderPathNorm + name+ '_norm.gz' , compression='gzip')

    for p in range(0,6701):
        currSumCer = currNorm.Cer.iloc[promIdxCer.loc[p, :].dropna().astype(int) - 1].sum()
        currLenCer = promIdxCer.loc[p,:].notna().sum()
        #currLen = cerProm.promLength[p]
        if currLenCer != 0:
            sumPromCer[p] = currSumCer*700/currLenCer
        
        currSumPar = currNorm.Par.iloc[promIdxPar.loc[p, :].dropna().astype(int) - 1].sum()
        currLenPar = promIdxPar.loc[p,:].notna().sum()
        if currLenPar != 0:
            sumPromPar[p] = currSumPar*700/currLenPar
            
    currSumProm= pd.concat([pd.Series(sumPromCer), pd.Series(sumPromPar)], axis=1)
    currSumProm.columns = ["Cer", "Par"] 
    
    
    # Save
    folderPathSumProm = locs['resultsFileLoc']+'SumPromRepeats/'
    os.makedirs(folderPathSumProm, exist_ok=True)
    currSumProm.to_pickle(folderPathSumProm + name +'_sumProm.gz', compression='gzip')  
    del currSumProm, currLenPar, currSumPar, currLenCer, currSumCer 






