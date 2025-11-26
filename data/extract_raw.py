import os
import kagglehub

os.environ["KAGGLEHUB_CACHE"] = "."
path = kagglehub.dataset_download("shayanfazeli/heartbeat")
print("Dataset path:", path)
