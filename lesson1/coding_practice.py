# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 13:10:07 2019

@author: 75253
"""

from collections import Counter
import random
import jieba

def generate(grammar_rule, target):
    """递归生成字符串拼接句子

    grammar_rule: 语法生成树的字典形式
    target: 需要查找的 key (statement / expression)
    """
    if target in grammar_rule:
        candidates = grammar_rule[target]
        candidate = random.choice(candidates)
        return ''.join(generate(grammar_rule, target=c.strip()) for c in candidate.split())
    else:
        return target

def get_generation_by_gram(grammar_str: str, target, stmt_split='=>', or_split='|'):
    """基于 grammar_str 产生句子

    grammar_str: 语法生成树
    stmt_split: 行内 statement 和  expression 的分隔符
    or_split: expression 不同取值的分隔符
    """
    rules = dict() # key is the @statement, value is @expression
    for line in grammar_str.split('\n'):
        if not line: continue  # skip the empty line

        stmt, expr = line.split(stmt_split)

        rules[stmt.strip()] = expr.split(or_split)

    # 将语法生成树转换成字典形式
    generated = generate(rules, target=target)

    return generated

def generate_n(grammar_str: str, target, n: int, stmt_split='=>', or_split='|'):
    """基于 grammar_str 产生句子

    grammar_str: 语法生成树
    stmt_split: 行内 statement 和  expression 的分隔符
    or_split: expression 不同取值的分隔符
    n: 生成句子个数
    """
    rules = dict() # key is the @statement, value is @expression
    for line in grammar_str.split('\n'):
        if not line: continue  # skip the empty line

        stmt, expr = line.split(stmt_split)

        rules[stmt.strip()] = expr.split(or_split)

    return [generate(rules, target=target) for i in range(10)]

def get_corpus(file):
    """清洗文本，提取需要信息

    file: 数据所在路径
    """
    FILE = open(file, encoding='utf-8').readlines()
    return "".join(row.split('++$++')[2].strip()[:-1] for row in FILE)

def cut(string):
    return list(jieba.cut(string))

def get_gram_count(word, wc):
    if word in wc: return wc[word]
    else:
        return wc.most_common()[-1][-1]

def two_gram_model(sentence):
    # 2-gram langauge model
    tokens = cut(sentence)

    probability = 1

    for i in range(len(tokens)-1):
        word = tokens[i]
        next_word = tokens[i+1]

        _two_gram_c = get_gram_count(word+next_word, _2_gram_word_counts)
        _one_gram_c = get_gram_count(next_word, words_count)
        pro =  _two_gram_c / _one_gram_c

        probability *= pro

    return probability

def generate_best(grammar_str: str, target, stmt_split='=>', or_split='|'):
    rules = dict() # key is the @statement, value is @expression
    for line in grammar_str.split('\n'):
        if not line: continue  # skip the empty line

        stmt, expr = line.split(stmt_split)

        rules[stmt.strip()] = expr.split(or_split)

    n = random.randint(10, 30)
    generated_list = [generate(rules, target=target) for i in range(n)]

    res = [(sentence, two_gram_model(sentence)) for sentence in generated_list]
    res.sort(key = lambda x : x[1], reverse=True)
    return res[0]


# 1. 设计你自己的句子生成器
sample_grammar1 = """
sentence => start sub respect do tail
start => 您好 | 你好 | hey | hello
sub => 我是人工智能客服 name number 号
name => 小美 | 比较美 | 大美 | 超级美
number => 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
respect => 请问您要 | 您需要
do => 点餐 | 预定 | 陪聊 | 咨询
tail => 吗？"""

sample_grammar2 = """
sentence => sub hello intro game ask do role tail
sub => 先生 | 女士 | 老板 | 金主爸爸 | 小朋友
hello => 您好 | 你好
intro => 欢迎来到
game => 地球online | 黑客帝国 | 王者荣耀 | 我的世界
ask =>  请问您要 | 您需要
do => 伪装成 | 化妆成 | 变性为
role => 孙悟空 | 富婆 | 二郎神 | 妲己 | 胡汉三
tail => 吗？"""

#sentence = get_generation_by_gram(sample_grammar1, target='sentence')
#print(sentence)

#sentence = get_generation_by_gram(sample_grammar2, target='sentence')
#print(sentence)

# 生成 n 个句子
#sentences = generate_n(sample_grammar2, target='sentence', n=10)
#print(sentences)

# 2. 使用新数据源完成语言模型的训练
corpus = get_corpus('./train.txt')
TOKENS = cut(corpus)
words_count = Counter(TOKENS)

words_with_fre = [f for w, f in words_count.most_common()]

_2_gram_words = [
    TOKENS[i] + TOKENS[i+1] for i in range(len(TOKENS)-1)
]
_2_gram_word_counts = Counter(_2_gram_words)

# 3. 获得最优质的的语言
print(generate_best(sample_grammar2, target='sentence'))

# Disadvantages
# 语料库和句子生成器生成的句子实际上并覅同一“类别”，所以生成句子的该v了都比较低
# 所得概率没有归一化处理，不够直观
# 解决办法，计算 two_gram_model 时，进行归一化处理，依照语料库文本，重新设计句子生成器
