#!/usr/bin/env python
# coding:utf-8
# author:Z time:2018/7/30

import sys
from pathlib import Path
import importlib
importlib.reload(sys)

from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

'''
 解析pdf 文本，保存到txt文件中
'''
def pdf_parse(source_path, result_path):
    fp = open(source_path, 'rb') # 以二进制读模式打开
    #用文件对象来创建一个pdf文档分析器
    praser = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器 与文档对象
    praser.set_document(doc)
    doc.set_parser(praser)

    # 提供初始化密码
    # 如果没有密码 就创建一个空的字符串
    doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDf 资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 文件已存在则清空内容，否则新建文件
        res_path = Path(result_path)
        if res_path.exists():
            open(result_path, "r+").truncate()

        # 循环遍历列表，每次处理一个page的内容
        for page in doc.get_pages(): # doc.get_pages() 获取page列表
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    with open(result_path,'a', encoding='utf-8') as f:
                        results = x.get_text()
                        # print(results)
                        f.write(results + '\n')
    return 1


'''
 解析txt文本
'''
import jieba
def analy_words(text_path):
    txt = open(text_path, 'r',encoding='utf-8').read()
    # 加载停用词表
    stopwords = [line.strip() for line in open("../data_set/stopwords.txt", 'r',encoding='utf-8').readlines()]
    words = jieba.lcut(txt)
    counts = {}
    for word in words:
        # 不在停用词表中
        if word not in stopwords:
            # 不统计字数为一的词
            if len(word) == 1:
                continue
            else:
                counts[word] = counts.get(word, 0) + 1
    items = list(counts.items())
    items.sort(key=lambda x: x[1], reverse=True)
    return items


'''
 绘制词云图
'''
from pyecharts.charts import WordCloud, Line, Bar, Page,Kline, Grid
from pyecharts import options as opts
from pyecharts.globals import SymbolType
from snapshot_selenium import snapshot
from pyecharts.render import make_snapshot
def analy_wordcloud(data):
    words = data
    c = (
        WordCloud()
        .add("", words, word_size_range=[20, 100], shape="diamond")
        .set_global_opts(title_opts=opts.TitleOpts(title="2019中国政府工作报告词云分析图"))
    )
    return c


if __name__ == "__main__":
    pdf_parse(r'../data_set/2019e-book.pdf', r'../result_set/2019e-book.txt')
    items = analy_words(r'../result_set/2019e-book.txt')
    for i in range(30):
        word, count = items[i]
        print("{:<10}{:>7}".format(word, count))
    picture = analy_wordcloud(items)
    picture.render('../result_set/analy_pdf.html')