'''
ONLY connect to local data files or azure blob storage.
ONLY accepts azure ml TabularDatasets when working on a remote compute.
Train,validation, and test:
>20,000: 10%
<20,000:
  <1,000: 10 folds
  1,000-20,000: 3 folds

If you are using ONNX models, or have model-explanability enabled, stacking is disabled and ONLY voting is utilized.
'''
