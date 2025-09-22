# 3123004790
论文查重系统
==========
| 这个作业属于哪个课程 | https://edu.cnblogs.com/campus/gdgy/Class34Grade23ComputerScience |
| ----------------- |--------------- |
| 这个作业要求在哪里| https://edu.cnblogs.com/campus/gdgy/Class34Grade23ComputerScience/homework/13477 |
| 这个作业的目标 | 使用PSP表格，完成项目开发，测试改进代码 |

一、PSP表格
----------
|**PSP2.1**|**Personal Software Process Stages**|**预估耗时（分钟）**      |**实际耗时（分钟）**     |
| ---- | ---- | ---- |---- |
|Planning      |  计划    | 20     | 25    |
|Estimate      | 估计这个任务需要多少时间     | 5     | 5    |
|Development      |开发      |40      |45     |
|Analysis      |需求分析 (包括学习新技术)      |20      |20     |
|Design Spec      |生成设计文档      |5      |5     |
|Design Review      |设计复审      |10      | 15    |
|Coding Standard      |代码规范 (为目前的开发制定合适的规范)      |10      | 10    |
|Design      |具体设计      |10      |15     |
|Coding      |具体编码      | 30     |30     |
|Code Review      |代码复审      | 20     | 15    |
|Test      |测试（自我测试，修改代码，提交修改）      |20      |20     |
|Reporting      | 报告     | 30     | 35    |
|Test Repor      |测试报告      |10      |10     |
|Size Measurement      |计算工作量      |5      |5     |
|Postmortem & Process Improvement Plan      |事后总结, 并提出过程改进计划      | 5     |5   |
|      | 合计     | 240     |260     |

二、计算模块接口的设计与实现过程
----------
###2.1 设计思路
论文查重系统需求为：设计一个论文查重算法，给出一个原文文件和一个在这份原文上经过了增删改的抄袭版论文的文件，在答案文件中输出其重复率。查询相关资料了解可以设计一个基于余弦相似度算法的文本相似度检测系统，通过jieba分词工具对中文文本进行预处理，结合词频统计与向量空间模型，计算两篇文本的余弦相似度值。
###2.2 算法流程图
![下载](https://img2024.cnblogs.com/blog/3698256/202509/3698256-20250922112124475-364465080.png)
###2.3 模块设计
####2.3.1 主控制模块 (main)
- 功能：系统入口，协调各模块工作流程。
- 验证命令行参数合法性；调用文件读取模块获取文本内容；调用相似度计算模块处理文本；调用结果输出模块保存计算结果；处理全局异常并提供用户友好提示。


####2.3.2 文件读取模块 (read_file)
功能：安全读取文本文件内容
关键设计：

支持UTF-8编码处理中文文本

完善的异常处理机制：

文件不存在异常

文件读取错误异常

错误处理策略：终止程序并输出错误信息

####2.3.3 文本处理模块
- ​​分词处理 (cut_text)​​

  - 功能：将连续文本转换为词语序列

  - 实现：基于jieba分词库的精确模式

  - 特点：保留所有词语，不做过滤

- 词频统计 (get_word_frequency)​​

  - 功能：统计词语出现频率

  - 实现：使用字典数据结构高效统计

  - 特点：时间复杂度O(n)，空间复杂度O(m)
- 模块流程图
![image](https://img2024.cnblogs.com/blog/3698256/202509/3698256-20250922122046317-1535557691.png)

####2.3.4 相似度计算模块 (calculate_similarity)
- 功能：计算两篇文本的余弦相似度

- 核心算法流程：对两篇文本分别进行分词，随后分别统计词频，构建统一的词汇表（两篇文本所有词语的并集），基于词汇表构建词频向量，最后用余弦相似度计算方法计算。
- 余弦相似度计算方法流程：
点积 = ∑(向量1[i] × 向量2[i])
模长 = √(∑(向量[i]²))
相似度 = 点积 / (模长1 × 模长2)
- 特殊处理：
  - 空文本检测：当任一文本为空时返回0
  - 数值精度：结果保留两位小数
- 模块流程图
![屏幕截图 2025-09-22 122306](https://img2024.cnblogs.com/blog/3698256/202509/3698256-20250922122529187-1628326863.png)

####2.3.5 结果输出模块
- 功能：将计算结果写入指定文件

- 设计特点：
  - 格式化输出：保留两位小数，UTF-8编码支持
  - 异常处理：可以对文件写入错误做出响应

三、计算模块接口部分的性能改进
----------
####3.1 改进思路
#####3.1.1 使用更高效的数据结构
- 原代码问题​​：手动实现词频统计，效率较低
- 优化方案​​：使用collections.Counter替代手动词频统计
- 效果​​：Counter使用哈希表实现，时间复杂度为O(n)，比手动实现的O(n²)更高效
#####3.1.2 优化分词处理
- 原代码问题​​：jieba.cut返回生成器，需要转换为列表
- 优化方案​​：直接使用jieba.lcut返回分词列表
​​- 效果​​：减少一次类型转换操作，提高效率
#####3.1.3 优化向量计算过程
- 原代码问题​​：
  - 构建了两个完整的高维向量
  - 需要三次遍历（构建向量和两次模长计算）
  - 内存占用高（存储完整向量
- 优化方案​​：
  - 不构建完整向量，直接计算点积和模长平方
  - 合并计算过程为单次遍历
  - 使用模长平方避免重复开方计算
- ​​效果​​：
  - 时间复杂度从O(3n)降低到O(n)
  - 空间复杂度从O(n)降低到O(1)（仅存储标量值）
  - 避免创建大型临时列表，减少内存占用
#####3.1.3 优化集合操作
- 原代码问题​​：set(orig_words) | set(plag_words)需要创建两个中间集合
- ​​优化方案​​：直接使用set(orig_freq.keys()) | set(plag_freq.keys())
- ​​效果​​：利用字典键集合操作，减少中间对象创建

优化后的代码在保持相同功能的前提下，显著提高了计算效率，降低了内存占用，特别适合处理大规模文本相似度计算任务。
####3.2 性能分析图
![屏幕截图 2025-09-22 152754](https://img2024.cnblogs.com/blog/3698256/202509/3698256-20250922152830669-2066097495.png)
四、计算模块部分单元测试展示
----------
####4.1 项目部分单元测试代码
测试代码中主要测试了 main.py 文件中的以下函数：
#####4.1.1 read_file - 读取文件内容
- 正常情况测试：使用 setUp 方法创建临时文件，包含预定义的文本内容，验证能否正确读取文件内容
- 异常情况测试：尝试读取不存在的文件，验证程序是否能正确处理异常并退出
```    
def test_read_file(self):
    # 测试文件读取功能`
    content = read_file(self.orig_file)
    self.assertEqual(content, self.orig_content)
```
#####4.1.2 cut_text - 对文本进行分词处理
- 构造简单的中文文本进行分词测试
- 验证返回结果是否为列表类型，且包含分词结果
```
def test_cut_text(self):
    # 测试文本分词功能
    words = cut_text("这是一个测试")
    self.assertIsInstance(words, list)
    self.assertGreater(len(words), 0)
```
#####4.1.3 get_word_frequency - 统计词频
- 构造包含重复词汇的词列表
- 验证词频统计是否准确
```
def test_get_word_frequency(self):
    # 测试词频统计功能
    words = ['这', '是', '一个', '测试', '这']
    freq = get_word_frequency(words)
    self.assertEqual(freq['这'], 2)
    self.assertEqual(freq['是'], 1)
calculate_similarity - 计算两个文本的相似度
```
#####4.1.4 测试相似度功能
- 普通情况测试：构造两个部分相似的文本，验证相似度在合理范围内（0-1之间）
- 相同文本测试：验证相同文本的相似度为1.0
- 不同文本测试：构造完全不同的文本，验证相似度仍在合理范围内
```
def test_calculate_similarity(self):
    # 测试相似度计算功能
    similarity = calculate_similarity(self.orig_content, self.plag_content)
    self.assertGreaterEqual(similarity, 0)
    self.assertLessEqual(similarity, 1)

def test_calculate_similarity_identical(self):
    # 测试相同文本的相似度（应为1）
    similarity = calculate_similarity(self.orig_content, self.orig_content)
    self.assertEqual(similarity, 1.0)

def test_calculate_similarity_different(self):
    # 测试完全不同的文本相似度
    similarity = calculate_similarity(self.orig_content, self.different_content)
    self.assertGreaterEqual(similarity, 0)
    self.assertLessEqual(similarity, 1)
```

五、计算模块部分异常处理说明
----------
####5.1 文件不存在异常 (FileNotFoundError)
- 用户输入了错误的文件路径

- 文件被移动或删除

- 文件名拼写错误
```
import unittest
from unittest.mock import patch, mock_open
import main

class TestFileNotFound(unittest.TestCase):
    @patch('builtins.open', side_effect=FileNotFoundError("文件不存在"))
    def test_read_file_not_found(self, mock_file):
        with self.assertRaises(SystemExit) as cm:
            main.read_file("non_existent.txt")
        self.assertEqual(cm.exception.code, 1)
        # 验证错误信息输出
        self.assertIn("文件不存在: non_existent.txt", self.captured_output.getvalue())

    def setUp(self):
        self.captured_output = io.StringIO()
        sys.stdout = self.captured_output

    def tearDown(self):
        sys.stdout = sys.__stdout__
```
####5.2 通用读取异常 (Exception)
- 文件权限问题（无读取权限）

- 文件编码问题

- 硬件故障导致读取失败
```
class TestGenericReadError(unittest.TestCase):
    @patch('builtins.open', side_effect=Exception("未知错误"))
    def test_read_file_generic_error(self, mock_file):
        with self.assertRaises(SystemExit) as cm:
            main.read_file("problematic.txt")
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("读取文件时出错: 未知错误", self.captured_output.getvalue())
```
####5.3 写入结果文件异常
- 目标目录无写入权限

- 文件被其他进程锁定

- 路径是目录而非文件
```
class TestWriteError(unittest.TestCase):
    @patch('builtins.open', side_effect=Exception("写入失败"))
    def test_write_result_error(self, mock_file):
        with self.assertRaises(SystemExit) as cm:
            # 模拟计算相似度后写入结果
            with patch('main.calculate_similarity', return_value=0.85):
                main.run_main()
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("写入结果文件时出错: 写入失败", self.captured_output.getvalue())
```
####5.4 参数数量错误处理
- 用户忘记提供必要的参数

- 参数顺序错误

- 脚本调用方式不正确
```
class TestArgumentHandling(unittest.TestCase):
    @patch('sys.argv', ['main.py'])  # 只有1个参数
    def test_insufficient_arguments(self):
        with self.assertRaises(SystemExit) as cm:
            main.run_main()
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("使用方法: python main.py [原文文件] [抄袭版论文的文件] [答案文件]", 
                      self.captured_output.getvalue())
```
