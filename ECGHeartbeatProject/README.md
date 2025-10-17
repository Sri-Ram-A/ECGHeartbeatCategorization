# ECG Heartbeat Classification Project
# Install PyTorch (choose based on your system)
cmd - nvidia-smi
Visit: https://pytorch.org/get-started/locally/

# Example:
# For CUDA 12.1:
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# For CPU only:
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu


ECGHeartbeatProject/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── splits/
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_preprocessing.ipynb
│   └── 03_model_experiments.ipynb
│
├── src/
│   ├── dataset.py
│   ├── model.py
│   ├── train.py
│   ├── evaluate.py
│   ├── preprocess.py
│   ├── utils.py
│   ├── config.yaml
│   └── __init__.py
│
├── experiments/
├── checkpoints/
├── requirements.txt
├── README.md
└── main.py

## Steps I followed in this project
cmd - pip install -r requirements.txt
cmd - python template.py to create directory structure
conda install -c conda-forge kaggle
kaggle --version
