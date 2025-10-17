from pathlib import Path

def create_project_structure(base_dir="ECGHeartbeatProject"):
    base = Path(base_dir)
    
    # Define folder structure
    folders = [
        "data/raw",
        "data/processed",
        "data/splits",
        "notebooks",
        "src",
        "experiments",
        "checkpoints",
    ]
    
    # Define base files
    files = {
        "README.md": "# ECG Heartbeat Classification Project\n",
        "requirements.txt": "torch\nnumpy\npandas\nmatplotlib\npyyaml\ntqdm\nwfdb\n",
        "main.py": "# Entry point for training/evaluation\n\nif __name__ == '__main__':\n    print('Starting project...')\n",
        "src/__init__.py": "",
        "src/dataset.py": "# Dataset and DataLoader definitions\n",
        "src/model.py": "# Model architecture definitions\n",
        "src/train.py": "# Training loop logic\n",
        "src/evaluate.py": "# Evaluation logic\n",
        "src/preprocess.py": "# Preprocessing and feature extraction\n",
        "src/utils.py": "# Utility functions (logging, metrics, etc.)\n",
        "src/config.yaml": (
            "experiment_name: 'ecg_baseline'\n"
            "data_dir: 'data/processed/'\n"
            "epochs: 20\n"
            "batch_size: 32\n"
            "learning_rate: 0.001\n"
            "num_classes: 5\n"
            "model:\n"
            "  type: 'Conv1D'\n"
            "  hidden_dim: 64\n"
            "optimizer: 'Adam'\n"
            "device: 'cuda'\n"
        ),
        "notebooks/01_data_exploration.ipynb": "",
        "notebooks/02_preprocessing.ipynb": "",
        "notebooks/03_model_experiments.ipynb": "",
    }
    
    # Create folders
    for folder in folders:
        path = base / folder
        path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created folder: {path}")
    
    # Create files
    for rel_path, content in files.items():
        file_path = base / rel_path
        if not file_path.exists():
            file_path.write_text(content)
            print(f"📝 Created file: {file_path}")
    
    print("\n🎉 Project structure created successfully!")

if __name__ == "__main__":
    create_project_structure()
