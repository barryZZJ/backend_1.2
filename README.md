1. `conda create -n toolbox_minimal python=3.9 -y`
2. `conda activate toolbox_minimal`
2. install cuda 12.4: https://developer.nvidia.com/cuda-12-4-0-download-archive
3. install pytorch: https://pytorch.org/get-started/locally/

   `pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124`
4. install ffmpeg, 加入PATH
4. `pip install -r requirements.txt`
5. flash-attn (麻烦，暂时没有安装成功，跳过)
    - 安装Microsoft Build Tools  https://visualstudio.microsoft.com/visual-cpp-build-tools/
    - 单个组件 勾选"MSVC v141 - VS 2017 C++ x64/x86 生成工具"、"Windows 10 SDK (10.0.20348.0)"
    - PATH添加"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Tools\MSVC\14.16.27023\bin\HostX64\x64"、"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Tools\MSVC\14.16.27023\include"
    - `SET DISTUTILS_USE_SDK=1 & "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvarsall.bat" x64`
    - `pip install exclude/flash-attention-main`
6. `conda install chardet`
7. download `https://github.com/facebookresearch/ImageBind/blob/main/imagebind/bpe/bpe_simple_vocab_16e6.txt.gz` and put into `exclude\ImageBind\bpe`

   then `cd exclude\ImageBind` and `pip install .`
8. download 'https://huggingface.co/microsoft/Phi-3-vision-128k-instruct' and put into `src/models/microsoft/Phi-3-vision-128k-instruct`
9. download 'https://dl.fbaipublicfiles.com/imagebind/imagebind_huge.pth' and put into `.checkpoints/`

Docker user:
1. Install WSL 2: `https://learn.microsoft.com/en-us/windows/wsl/install`
2. Install Docker Desktop:
   - Windows: https://www.docker.com/products/docker-desktop/
   - Linux: https://docs.docker.com/desktop/install/linux-install/#generic-installation-steps
3. Install NVIDIA Container Toolkit (Note you need to install cuda on host machine): https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html
4. run with docker: 