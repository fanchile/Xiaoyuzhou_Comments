# 读取episode_comments_info文件夹中所有的csv文件，并判断是否可以根据表头的信息进行合并。如果可以进行合并则将所有文件合并为一个csv文件
import pandas as pd
import os
import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
        return result['encoding']

def merge_csv_files(folder_path):
    all_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    dataframes = []
    
    for file in all_files:
        df = pd.read_csv(os.path.join(folder_path, file), encoding=detect_encoding(os.path.join(folder_path, file)))
        dataframes.append((file, df))  # Store filename along with the dataframe
    
    # Check if all dataframes have the same columns
    base_columns = dataframes[0][1].columns
    inconsistent_files = []

    for file, df in dataframes:
        if not df.columns.equals(base_columns):
            inconsistent_files.append(file)  # Collect files with inconsistent headers

    if not inconsistent_files:
        merged_df = pd.concat([df for _, df in dataframes], ignore_index=True)
        merged_df.to_csv(os.path.join(folder_path, 'merged_file.csv'), index=False)
    else:
        print("无法合并文件，以下文件的表头信息不一致：", inconsistent_files)

if __name__ == "__main__":

    # 获取当前工作目录
    current_directory = os.getcwd()

    # 定义相对路径
    relative_path = 'episode_comments_info'  # 相对路径示例

    # 组合路径
    full_path = os.path.join(current_directory, relative_path)
    merge_csv_files(full_path)
