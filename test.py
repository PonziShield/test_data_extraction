from feature_extraction import *
from create_dataset import *


cd = CreateDataset(300)
# cd.createTransactionDataset()
# cd.createFeatureDataset()
cd.create_numpy_array()
