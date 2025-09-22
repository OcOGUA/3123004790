import jieba
import sys
import math
from collections import Counter
import cProfile
import pstats
import io


# 读取文件
def read_file(file_path) :
    try :
        with open(file_path , 'r' , encoding = 'utf-8') as f :
            return f.read()
    except FileNotFoundError :
        print(f"文件不存在: {file_path}")
        sys.exit(1)
    except Exception as e :
        print(f"读取文件时出错: {e}")
        sys.exit(1)


# 对文本进行分词处理（使用jieba的精确模式）
def cut_text(text) :
    return jieba.lcut(text)  # 直接返回列表，避免生成器转换


# 统计词频（使用Counter优化）
def get_word_frequency(words) :
    return Counter(words)  # 使用Counter代替手动计数


# 计算两个文本的相似度（优化版）
def calculate_similarity(orig_text , plag_text) :
    # 对文本进行分词
    orig_words = cut_text(orig_text)
    plag_words = cut_text(plag_text)

    # 统计词频
    orig_freq = get_word_frequency(orig_words)
    plag_freq = get_word_frequency(plag_words)

    # 获取所有词汇（使用集合操作）
    all_words = set(orig_freq.keys()) | set(plag_freq.keys())

    # 计算点积和模长平方（避免重复计算）
    dot_product = 0.0
    orig_magnitude_sq = 0.0
    plag_magnitude_sq = 0.0

    # 一次性计算所有必要值
    for word in all_words :
        orig_count = orig_freq.get(word , 0)
        plag_count = plag_freq.get(word , 0)

        dot_product += orig_count * plag_count
        orig_magnitude_sq += orig_count * orig_count
        plag_magnitude_sq += plag_count * plag_count

    # 计算模长
    magnitude_orig = math.sqrt(orig_magnitude_sq)
    magnitude_plag = math.sqrt(plag_magnitude_sq)

    if magnitude_orig == 0 or magnitude_plag == 0 :
        return 0.0

    similarity = dot_product / (magnitude_orig * magnitude_plag)
    return round(similarity , 2)


def run_main() :
    if len(sys.argv) != 4 :
        print("使用方法: python main.py [原文文件] [抄袭版论文的文件] [答案文件]")
        sys.exit(1)

    orig_path , plag_path , ans_path = sys.argv [1] , sys.argv [2] , sys.argv [3]

    # 读取文件内容
    orig_text = read_file(orig_path)
    plag_text = read_file(plag_path)

    # 计算相似度
    similarity = calculate_similarity(orig_text , plag_text)

    # 将结果写入答案文件
    try :
        with open(ans_path , 'w' , encoding = 'utf-8') as f :
            f.write(f"{similarity:.2f}")
        print(f"相似度计算完成，结果已保存至 {ans_path}")
    except Exception as e :
        print(f"写入结果文件时出错: {e}")
        sys.exit(1)


if __name__ == '__main__' :
    # 创建性能分析器
    profiler = cProfile.Profile()
    profiler.enable()  # 开始收集性能数据

    # 运行主程序
    run_main()

    profiler.disable()  # 停止收集性能数据

    # 保存.prof文件
    profiler.dump_stats('performance_analysis.prof')
    print("性能分析结果已保存至 performance_analysis.prof")

    # 创建统计对象并排序
    # 创建StringIO流对象并将其传递给Stats构造函数
    stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.sort_stats(pstats.SortKey.CUMULATIVE)  # 按累计时间排序

    # 将分析结果输出到文件
    stats.print_stats()
    
    with open('performance_analysis.txt' , 'w' , encoding = 'utf-8') as f :
        f.write(stream.getvalue())

    print("性能分析报告已保存至 performance_analysis.txt")