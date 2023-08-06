import pandas as pd
import sys

header_cols = ['Feature', 
               'Feature True Percent', 
               'Feature True Count', 
               'Feature True Fraud Count', 
               'Feature True Fraud Precent', 
               'Feature False Count', 
               'Feature False Fraud Count', 
               'Feature False Fraud Precent']

class BivariateException(Exception):
  def __init__(self, message):
      self.message = message
      super().__init__(self.message)

def base_rate(data, target_col):
  base = ['Base Count | Base Fraud Count | Base Fraud Percent', 
          data.shape[0], 
          data[target_col].sum(), 
          data[target_col].sum() / data.shape[0] * 100, 
          0, 
          0, 
          0, 
          0]

  return base

def bivariate(data, bivariate_col, target_col):
  try:
    assert(data[bivariate_col].dtype == bool)
  except:
    raise BivariateException('Exception: Bivariate data column type is not boolean')

  try:
    assert(data[target_col].dtype == bool)
  except:
    raise BivariateException('Exception: Bivariate target column type is not boolean')

  bivar = pd.DataFrame()

  temp = [bivariate_col, 
          data[bivariate_col].sum() / data.shape[0] * 100, 
          data[bivariate_col].sum(), 
          data[data[target_col]][bivariate_col].sum(), 
          data[data[target_col]][bivariate_col].sum() / data[bivariate_col].sum() * 100,
          data.shape[0] - data[bivariate_col].sum(), 
          data[target_col].sum() - data[data[target_col]][bivariate_col].sum(), 
          (data[target_col].sum() - data[data[target_col]][bivariate_col].sum()) / (data.shape[0] - data[bivariate_col].sum()) * 100]
  
  bivar = pd.concat([bivar, pd.DataFrame(temp).transpose()])
    
  temp = base_rate(data, target_col)
  
  bivar = pd.concat([bivar, pd.DataFrame(temp).transpose()])

  bivar.columns = header_cols

  bivar['Feature'] = bivar['Feature'].astype(str)
  bivar[header_cols[-1:]] = bivar[header_cols[-1:]].astype(float)

  return bivar

def fraud_bivariates(data, bivariate_cols, target_col):
  try:
    assert(data[bivariate_cols].dtypes.nunique() == 1)
  except:
    raise BivariateException('Exception: Bivariate data columns are not all boolean')

  try:
    assert(data[bivariate_cols].dtypes.unique()[0] == bool)
  except:
    raise BivariateException('Exception: Bivariate data columns type is not boolean')

  try:
    assert(data[target_col].dtype == bool)
  except:
    raise BivariateException('Exception: Bivariate target column type is not boolean')

  bivar = pd.DataFrame()

  for col in bivariate_cols:
    try:
      temp = [col, 
              data[col].sum() / data.shape[0] * 100, 
              data[col].sum(), 
              data[data[target_col]][col].sum(), 
              data[data[target_col]][col].sum() / data[col].sum() * 100,
              data.shape[0] - data[col].sum(), 
              data[target_col].sum() - data[data[target_col]][col].sum(), 
              (data[target_col].sum() - data[data[target_col]][col].sum()) / (data.shape[0] - data[col].sum()) * 100]
      
      bivar = pd.concat([bivar, pd.DataFrame(temp).transpose()])
    except:
      pass
    
  temp = base_rate(data, target_col)
  
  bivar = pd.concat([bivar, pd.DataFrame(temp).transpose()])

  bivar.columns = header_cols

  bivar['Feature'] = bivar['Feature'].astype(str)
  bivar[header_cols[-1:]] = bivar[header_cols[-1:]].astype(float)

  return bivar