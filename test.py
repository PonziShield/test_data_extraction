from feature_extraction import *
from create_dataset import *
from extract_data_realtime import *


# cd = CreateDataset(300)
# # cd.createTransactionDataset()
# # cd.createFeatureDataset()
# cd.create_numpy_array()


de= RealtimeDataExtractor("0x06012c8cf97bead5deae237070f9587f8e7a266d")
data=de.createTransactionDataset()
print(data.shape)
