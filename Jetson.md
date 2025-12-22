# List of commands followed
```bash
// 1. We need python3.8 for tensorflow (Insp from : https://github.com/NVIDIA-AI-IOT/jetbot/wiki/Create-SD-Card-Image-From-Scratch)
sudo usermod -aG i2c $USER
sudo apt-get update
sudo apt install python3.8 python3.8-venv python3.8-dev -y
python3.8 --version

// 2. We need nodejs for jupyter support 
sudo apt install curl
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash - 
// Download whatever setup version is lesser than the link written as "(recommended)"
sudo apt install -y nodejs

// 3. Create venv and install notebook
python3.8 -m venv venv38
source venv38/bin/activate
pip3 install --upgrade numpy 
pip3 install notebook
// Check installation
jupyter notebook

// 4. Find your Jetpack version 
dpkg-query --show nvidia-l4t-core
// Mine is Mine is 4.6.5
``` 

## 5 . Find your tensorflow version at : 
- https://developer.download.nvidia.com/compute/redist/jp/
- Now follow the below documentation 
- https://docs.nvidia.com/deeplearning/frameworks/install-tf-jetson-platform/index.html

```bash
sudo apt-get update
sudo apt-get install libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran
source venv38/bin/activate
pip3 install -U testresources setuptools numpy future mock keras_preprocessing keras_applications gast protobuf pybind11 cython pkgconfig packaging h5py
pip3 install --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v46 tensorflow==2.6.2+nv21.12
```