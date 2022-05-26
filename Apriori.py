'''
Filename: d:\edu_programs\traffic_ml\homework3\Apriori.py
Path: d:\edu_programs\traffic_ml\homework3
Created Date: Thursday, May 12th 2022, 10:32:14 am
Author: Orion

实现基于计数散列表的Apriori关联类 1950097阙成恩
'''




class Apriori():
    
    # 初始化数据集为set类型，定义最小支持度和最小置信度
    def __init__(self, data: list, min_sup: float, min_conf: float):
        self.dataset = [set(x) for x in data]
        self.min_sup = min_sup
        self.min_conf = min_conf
    
    # 根据集合计算hash
    def get_key(self, lis: set) -> str: 
        lis = [ord(i) for i in lis]
        lis.sort()
        lis = [str(i) for i in lis]
        return ''.join(lis)
    
    # 从hash反算集合
    def get_set(self, key: str) -> set:
        return set([chr(int(key[2*i:2*i+2])) for i in range(len(key)//2)])
    
    # 是否符合apriori剪枝规则
    def is_apriori(self, Ck_key: str, Lk_keys: list) -> bool: 
        Ck_set = self.get_set(Ck_key)
        Lk_sets = [self.get_set(Lk_key) for Lk_key in Lk_keys]
        
        for item in Ck_set:
            sub_Ck = Ck_set - frozenset([item])
            if sub_Ck not in Lk_sets:
                return False
        
        return True
    
    # 计算C1候选散列表，索引为get_key计算得到的hash，值为遍历原数据集得到的计数结果的支持度
    def get_C1(self) -> dict:
        C1  = {}
        
        for itemset in self.dataset:
            for item in itemset:
                key = self.get_key(item)
                if key not in C1:
                    C1[key] = 1
                else:
                    C1[key] += 1    
                        
        for key in C1:
            C1[key] = C1[key] / len(self.dataset) 

        return C1
    
    # 根据Ck候选散列表计算Lk频繁散列表
    def generate_Lk(self, Ck: dict, k: int) -> dict:
        Lk = {}
        
        for key in Ck:
            if Ck[key] >= self.min_sup:
                Lk[key] = Ck[key]
        return Lk
    
    # 根据Lk候选散列表，拼接组合索引，根据apriori规则进行剪枝，并遍历原数据集计算Lk频繁散列表（支持度）    
    def generate_Ck(self, Lk, k):
        Ck = {}
        Lk_keys = list(Lk.keys())
        
        for i in range(len(Lk_keys)):
            for j in range(i+1, len(Lk_keys)):
                set0 = self.get_set(Lk_keys[i])
                set1 = self.get_set(Lk_keys[j])

                if len(set0 & set1) == k-2:
                    new_set = set0 | set1
                    Ck_key = self.get_key(new_set)
                    
                    if self.is_apriori(Ck_key,Lk_keys):
                        # print(set0, set1)
                        Ck[Ck_key] = 0
                        
                        for itemset in self.dataset:
                            if new_set.issubset(itemset):
                                Ck[Ck_key] += 1

        for Ck_key in Ck:
            Ck[Ck_key] = Ck[Ck_key] / len(self.dataset)
            
        return Ck
    
    # 计算最大频繁项集X
    def generate_X(self) -> dict:
        k = 1
        Ck = self.get_C1()
        Lk = self.generate_Lk(Ck,k=k)
        
        while True:
            k+=1
            Ck = self.generate_Ck(Lk,k)
            if len(Ck) == 0:
                return Lk
            Lk = self.generate_Lk(Ck,k)

    # 回溯算法，计算一个长为k的集合的所有可能子集，返回二进制的01表示链表
    def all_subsets(self, k: int) -> list:
        path = []
        res = []
        def backtrack():
            # 归
            if len(path) == k:
                res.append(path[:])
            else:
                for i in [0,1]:
                    path.append(i)
            # 递
                    backtrack()
                    # print(self.path)
                    path.pop()
            return res
        return backtrack()
    
    # 对所有的最大频繁项集，分别计算它们的关联规则并输出    
    def generate_rules(self):
        # 得到最大频繁项集
        X = self.generate_X()
        for freq_key in X:
            freq_set = self.get_set(freq_key)
            freq_lis = list(freq_set)
            
            # 计算所有可能的真子集
            bin_subsets = self.all_subsets(len(freq_lis))
            possible_subsets = []
            for i in bin_subsets:
                subset = []
                for j in range(len(i)):
                    if i[j] == 1:
                        subset.append(freq_lis[j])
                possible_subsets.append(set(subset))
            # 删去非真子集
            possible_subsets.pop(0)   
            possible_subsets.pop(-1)  
            
            # 计算置信度并输出符合要求的关联规则
            for sub_set in possible_subsets:                
                sub_count = 0
                count = X[freq_key] * len(self.dataset)
                for key in self.dataset:
                    if sub_set.issubset(key):
                        sub_count += 1
                if (count / sub_count) >= self.min_conf:
                    print(freq_set,':',sub_set, '--->', freq_set - sub_set,'conf:',(count / sub_count))

# test it
if __name__ == '__main__':
    
    data = [['M', 'O', 'N', 'K', 'E', 'Y'],
            ['D', 'O', 'N', 'K', 'E', 'Y'],
            ['M', 'A', 'K', 'E'],
            ['M', 'U', 'C', 'K', 'Y'],
            ['C', 'O', 'O', 'K', 'I', 'E']]

    # 添加数据
    # data.append(list('MOOKACKY'))
    # data.append(list('HOOKCOO'))
    # data.append(list('HOCKEYHOO'))
    # data.append(list('PONYONEY'))
    # data.append(list('ROCKY'))
    # data.append(list('MOCKY'))
    # data.append(list('COCKY'))
    # data.append(list('SOCKEY'))

    relator = Apriori(data=data, min_sup=0.6, min_conf=0.8)
    relator.generate_rules()
    
    