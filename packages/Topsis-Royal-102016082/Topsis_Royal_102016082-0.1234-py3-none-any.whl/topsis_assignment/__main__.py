import pandas as pd
import math
import numpy as np
from pathlib import Path
import os
import sys
import logging

#data_folder = Path(os.getcwd())
#file_to_open = data_folder / sys.argv[1]
#f = open(file_to_open)

def main():  
  if (len(sys.argv) != 5):
    logging.warning("Usages: python <program.py> <InputDataFile> <Weights> <Impacts> <ResultFileName>")
    exit()
  try:
      data = pd.DataFrame(pd.read_csv(str(sys.argv[1])))
  except FileNotFoundError:
      logging.warning("Wrong input data file or file path")
      exit()
  data1 = data.copy()
  if (len(data.columns)) < 3:
    logging.warning("Input data file must contain 3 or more columns")
    exit()
  weightstr = str(sys.argv[2])
  weights = [int(i) for i in weightstr.split(',')]
  variables = len(data.columns) - 1
  instances = len(data)
  impactsstr = str(sys.argv[3]) 
  impactssplit = impactsstr.split(",")
  impacts = [0] * variables
  i = 0
  for imp in impactssplit:
    if (imp == '+'):
      impacts[i] = 1
    else:
      impacts[i] = 0
    i = i + 1
  if (((len(data.columns) - 1) != len(weights)) | ((len(data.columns) - 1) != len(impacts))):
    logging.warning("Number of weights, number of impacts and number of columns (from 2nd to last columns) must be same.")
    exit() 
  # Calculate sqrt of sum of squares
  ssp = [0] * variables
  for i in range(0, variables):
    ssp[i] = math.sqrt(data.iloc[:, i + 1].pow(2).sum())
  # Divide each column by sqrt of sum of squares
  for i in range(0, variables):
    data.iloc[:, i + 1] = data.iloc[:, i + 1] / ssp[i]
  # Assign weights
  #weights = [1, 1, 1, 1, 1]
  # Multiply each column by their respective weights
  data.iloc[:, 1:(variables + 1)].mul(weights, axis=1)  
  #Find impacts (ideal best and ideal worst values)
  #max = 1
  #min = 0
  idealbest = [0] * variables
  idealworst = [0] *  variables
  #impacts = [1, 1, 0, 0, 1]
  num = [0, 1, 2, 3, 4]
  for i in range(0, variables):
      if (impacts[i] == 1):
        idealbest[i] = max(data.iloc[:, i + 1])
        idealworst[i] = min(data.iloc[:, i + 1])
      else:
        idealbest[i] = min(data.iloc[:, i + 1])
        idealworst[i] = max(data.iloc[:, i + 1])
  #Find euclidean distance of each row from the impacts
  distidealbest = [0] * instances
  distidealworst = [0] * instances
  for i in range(0, instances):
    distidealbest[i] = np.linalg.norm(data.iloc[i,1:(variables + 1)] - idealbest)
    distidealworst[i] = np.linalg.norm(data.iloc[i, 1:(variables + 1)] - idealworst)   
  #Find topsis score for each instance
  distsum = [i + j for i, j in zip(distidealworst, distidealbest)]
  topsis = [round(i / j, 2) for i, j in zip(distidealworst, distsum)]
  # Add topsis and rank columns
  data1['Topsis Score'] = topsis
  data1['Rank'] = data1['Topsis Score'].rank()
  #write to output file
  with open(str(sys.argv[4]), 'w') as csv_file:
      data1.to_csv(path_or_buf=csv_file)

if  __name__ == "__main__":
  main()