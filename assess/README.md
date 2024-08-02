# scripts

1. conda create -n imagebind_LLM python=3.9 -y
2. cd LLaMA-Adapter
3. pip install -r requirements.txt

# 评估

1. `conda create --name imagebind python=3.8 -y`
2. `conda activate imagebind`
3. `cd ImageBind`
4. `pip install .`
5. `cd ..`
6. `pip install -r requirements.txt`
7. 【语意相似性】assessment text: `python assessment_text.py --ori_text_path assets/ori_text.txt --protect_text_path assets/protect_text.txt`
8. 【语意相似性 + 数值相似性】assessment position: `python assessment_position.py --ori_position_path assets/ori_position.txt --protect_position_path assets/protect_position.txt`
9. 【语意相似性 + 数值相似性 + 位置关联性】assessment trace: `python assessment_trace.py --ori_trace_path assets/ori_trace.txt --protect_trace_path assets/protect_trace.txt`
   10.【语意相似性】assessment csv: `python assessment_csv.py --ori_csv_path assets/ori_csv.csv --protect_csv_path assets/protect_csv.csv`
   11.【语意相似性】(convert the odf to pdf first) assessment ofd and pdf: `python assessment_pdf.py --ori_pdf_path assets/ori_pdf.pdf --protect_pdf_path assets/protect_pdf.pdf`

注意：

1. .assets/ori_text.txt 与 .assets/protect_text.txt 文件中，只有保护前的文本
2. .assets/ori_position.txt 与 .assets/protect_position.txt 文件中，只有保护前后的位置数字，数字之间用空格分割
3. .assets/ori_trace.txt 与 .assets/protect_trace.txt 文件中，只有保护前后的位置轨迹数字，数字之间用空格分割
