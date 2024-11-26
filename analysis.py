# 读取modified_merged_file.csv，并根据每一列的内容分布生成直方图
import pandas as pd
import matplotlib.pyplot as plt

# 读取CSV文件
data = pd.read_csv('modified_merged_file.csv')

# 获取data的所有列
columns = data.columns.tolist()
print(columns)




# 根据data中isFriendly列的内容生成饼图，isFriendly的取值有三种True、False和空值
data['isFriendly'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.title('Pie Chart of isFriendly Values')
plt.ylabel('')  # Hide the y-label for better aesthetics
plt.savefig('pie_chart_isFriendly.png')
plt.close()

# 判断data中Sentiment列数据是否全部为数值，如果是数值，则根据内容生成直方图
if pd.api.types.is_numeric_dtype(data['Sentiment']):
    data['Sentiment'].plot(kind='hist', bins=100)
    plt.title('Histogram of Sentiment Values')
    plt.xlabel('Sentiment')
    plt.ylabel('Frequency')
    plt.savefig('histogram_sentiment.png')
    plt.close()

# 读取data的每一行，根据text的长度生成一个新的指标textlen，并基于textlen的数值生成直方图
try:
    # 计算每行text的长度，处理空值情况
    data['textlen'] = data['text'].apply(lambda x: len(x) if isinstance(x, str) else 0)  
    data['textlen'].plot(kind='hist', bins=100)  # 生成textlen的直方图
    plt.title('Histogram of Text Lengths')
    plt.xlabel('Text Length')
    plt.ylabel('Frequency')
    plt.savefig('histogram_text_length.png')
    plt.close()
except Exception as e:
    print(f"An error occurred: {e}")
    print(type(data['text']))


# 获取data中textlen的各种统计量，包括最大值、最小值，均值、中位数等
textlen_stats = {
    'max': data['textlen'].max(),
    'min': data['textlen'].min(),
    'mean': data['textlen'].mean(),
    'median': data['textlen'].median(),
    '25':data['textlen'].quantile(0.25),
    '75':data['textlen'].quantile(0.75)
}
print(textlen_stats)

# 显示textlen大于1000的所有text值，并统计总共有多少条
long_texts = data[data['textlen'] > 250]['text']
count_long_texts = long_texts.count()
print(long_texts)
print(f"Total number of texts with length greater than 250: {count_long_texts}")

# 显示textlen大于1000的所有text值以及likeCount和replyCount
long_texts_details = data[data['textlen'] > 1000][['text', 'likeCount', 'replyCount']]
print(long_texts_details)

