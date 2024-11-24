# 读取名为merged_file.csv文件
import pandas as pd
import re

from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

# sentiment classification
semantic_cls_bi = pipeline(Tasks.text_classification, 'damo/nlp_structbert_sentiment-classification_chinese-base',device='gpu:0')
semantic_cls_seven = pipeline(Tasks.text_classification, 'damo/nlp_structbert_emotion-classification_chinese-base', model_revision='v1.0.0',device='gpu')


def remove_timestamp(s):
    # 正则表达式匹配时间戳
    timestamp_pattern = r'\b\d{1,2}:\d{2}(?::\d{2})?(?:\s|$|[\u4e00-\u9fa5])'
    # 替换掉时间戳
    return re.sub(timestamp_pattern, '', s)

def remove_emoji_shortcodes(text):
    # 正则表达式匹配以冒号开头和结尾的文本
    emoji_shortcode_pattern = r':\w+:'
    # 替换掉这些文本
    return re.sub(emoji_shortcode_pattern, '', text)

if __name__ == "__main__":

    merged_file = pd.read_csv('merged_file.csv')

    # 读取merged_file所有列
    all_columns = merged_file.columns.tolist()

    print(all_columns)

    for col in ['惊讶', '高兴', '悲伤', '喜好', '厌恶', '愤怒', '恐惧','SentimentPos','SentimentNeg']:
        if col not in merged_file.columns:
            merged_file[col] = None

    # 遍历merged_file中列为text的所有内容
    for index, row in merged_file.iterrows():
        new_text = remove_emoji_shortcodes(remove_timestamp(row['text']))
        # 在遍历merged_file中，添加新的一列并赋值
        seven_sentiment = semantic_cls_seven(input=new_text)['scores']


        merged_file.loc[index, 'text'] = new_text
        merged_file.loc[index, 'SentimentPos'] = semantic_cls_bi(input=new_text)['scores'][0]
        merged_file.loc[index, 'SentimentNeg'] = semantic_cls_bi(input=new_text)['scores'][1]
        merged_file.loc[index, '惊讶'] = seven_sentiment[0]
        merged_file.loc[index, '高兴'] = seven_sentiment[1]
        merged_file.loc[index, '悲伤'] = seven_sentiment[2]
        merged_file.loc[index, '喜好'] = seven_sentiment[3]
        merged_file.loc[index, '厌恶'] = seven_sentiment[4]
        merged_file.loc[index, '愤怒'] = seven_sentiment[5]
        merged_file.loc[index, '恐惧'] = seven_sentiment[6]
        # print(new_text)
        print(index)
        # print(semantic_cls_bi(input=new_text)['scores'],row['Sentiment'],semantic_cls_seven(input=new_text))
        
        # merged_file.to_csv('modified_merged_file.csv', index=False)


    # 修改后的文件形成新的文件
    merged_file.to_csv('modified_merged_file.csv', index=False)
