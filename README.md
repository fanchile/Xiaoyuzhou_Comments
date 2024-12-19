# 小宇宙网页端播客评论数据爬取

本项目简单爬取了2023年小宇宙播客大赏中所列播客的评论信息（2023大赏.xlsx）。所有爬取的播客评论数据都存储在`episode_comments_info`文件夹中。合并后的所有评论数据存储在`merged_file.csv`文件中。

- `pod_name`：对应的播客名称
- `epi_name`：对应的播客中单集的名称
- `id`：评论的唯一id
- `level`：评论的优先级
- `text`：评论的文本内容
- `isFriendly`：小宇宙自己提供的是否友好评论标识。只有部分评论拥有
- `Sentiment`：根据StructBERT情感分类模型判断评论为正向的概率
- `likeCount`：点赞数
- `replyCount`：回复数

`datapreparation.py`文件中包含了数据清洗和预处理的部分，包括删除emoji表情、时间标签、添加情感七分类模型的结果，最终输出文件`modified_merged_file.csv`。

`analysis.py`文件中包含了数据分析的部分，包括简单的描述性统计以及画图

针对评论区的分析报告可在[我的博客](https://fanchile.github.io/2024/11/24/xiaoyuzhou_comment_analysis/)查看

# 免责声明

本文所提供的数据抓取程序代码及思路仅供学习、交流使用，不得用于其他用途；如因使用者恶意使用所产生的任何法律后果本作者均不负相应责任
