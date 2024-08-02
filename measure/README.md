# 度量

利用大模型Agent来识别输入数据的隐私分量。

## 脚本

### 系统安装

ffmpeg：sudo apt update && sudo apt install ffmpeg 
audio: sudo apt-get install portaudio19-dev

### python环境安装

1. `conda create --name measurement python=3.8 -y`
2. `conda activate measurement`
3. `cd measurement`
4. install pytorch: https://pytorch.org/get-started/locally/
5. `pip install -r requirements.txt`
6. `conda install chardet`

# 评估脚本

1. 图像类型 `python image_measure.py`
2. 视频类型 `python video_measure.py`
3. 文字类型 `python text_measure.py`
4. 数值类型 `python number_measure.py`
5. 位置类型 `python position_measure.py`
6. 轨迹类型 `python trace_measure.py`
7. ofd/pdf类型 `python ofd_pdf_measure.py` # 在评估ofd之前，请把ofd转存成为pdf
8. csv类型 `python csv_measure.py` 
9. audio类型 `python audio_measure.py` # 
9. audio类型 `python real_time_audio_measure.py` 


## 注意

1. 输入数据在`./data/data_to_measure`中

