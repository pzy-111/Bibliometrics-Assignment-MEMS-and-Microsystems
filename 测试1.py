#缺点是共被引有问题
from pybibx.base.pbx import pbx_probe
import networkx as nx
from itertools import combinations
import matplotlib.pyplot as plt
authors=[]
probe = pbx_probe(file_bib="D:\下载\demon.bib", db="wos", del_duplicated=True)
eda_report = probe.eda_bib()
print(eda_report)

# 数据健康检查
health_report = probe.health_bib()
print(health_report)
# 显示Top 20高频关键词
probe.tree_map(entry='kwp', topn=20)

# 显示作者生产力图
probe.authors_productivity(topn=15)
# 生成合作网络图（需自定义网络分析代码）
# 示例：作者合作网络
author_network = nx.Graph()
for authors in probe.aut:
    for pair in combinations(authors, 2):
        author_network.add_edge(*pair)

nx.draw(author_network, with_labels=True)
plt.show()
probe.plot_citation_trajectory()
