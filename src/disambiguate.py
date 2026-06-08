import re
from collections import defaultdict


class AuthorDisambiguator:
    def __init__(self):
        # 使用字典加速查找
        self.name_to_id = {}
        # 辅助索引：用于机构辅助匹配（如果有机构信息可以加进来）
        self.name_variants = defaultdict(set)

    def disambiguate(self, name, affiliation=None):
        """
        作者消歧（高性能版）
        规则：DR001 (精确), DR002 (标准化), DR003 (机构辅助)
        """
        if not name:
            return None

        # 1. DR001 & DR002: 标准化姓名
        # 移除标点、空格，转小写
        norm_name = self._normalize(name)

        # 精确匹配（最快）
        if norm_name in self.name_to_id:
            return self.name_to_id[norm_name]

        # 如果没有匹配，创建新ID
        author_id = f"A{len(self.name_to_id) + 1:06d}"
        self.name_to_id[norm_name] = author_id
        self.name_variants[norm_name].add(name)

        return author_id

    def _normalize(self, name):
        """姓名标准化：去标点、去空格、转小写"""
        # 移除所有非字母数字的字符
        s = re.sub(r'[^\w]', '', name)
        return s.lower()


class PaperDeduplicator:
    def __init__(self):
        self.doi_to_id = {}
        self.title_to_id = {}

    def deduplicate(self, paper):
        """
        论文去重（高性能版）
        规则：DR006 (DOI), DR007 (标题+作者)
        """
        # DR006: DOI匹配
        doi = paper.get("doi")
        if doi and doi in self.doi_to_id:
            return self.doi_to_id[doi]

        # DR007: 标题匹配（简化版，使用标准化标题）
        title = paper.get("title", "")
        norm_title = self._normalize_title(title)

        if norm_title in self.title_to_id:
            return self.title_to_id[norm_title]

        # 创建新论文
        paper_id = f"P{len(self.doi_to_id) + 1:06d}"

        if doi:
            self.doi_to_id[doi] = paper_id
        if norm_title:
            self.title_to_id[norm_title] = paper_id

        return paper_id

    def _normalize_title(self, title):
        if not title:
            return ""
        # 转小写，去标点，去多余空格
        s = re.sub(r'[^\w\s]', '', title.lower())
        return re.sub(r'\s+', ' ', s).strip()


class KeywordDisambiguator:
    def __init__(self):
        self.kw_to_id = {}

    def disambiguate(self, keyword):
        """
        关键词消歧（高性能版）
        规则：DR010 (完全匹配)
        """
        if not keyword:
            return None

        norm_kw = keyword.lower().strip()

        if norm_kw not in self.kw_to_id:
            self.kw_to_id[norm_kw] = f"K{len(self.kw_to_id) + 1:06d}"

        return self.kw_to_id[norm_kw]