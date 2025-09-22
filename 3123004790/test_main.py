import unittest
import os
import tempfile
from main import read_file, cut_text, get_word_frequency, calculate_similarity
from io import StringIO
import sys

class TestMain(unittest.TestCase):
    
    def setUp(self):
        # 创建临时文件用于测试
        self.orig_content = "这是一个原始文本，用于测试相似度计算功能。"
        self.plag_content = "这是一个抄袭文本，用于测试相似度计算功能。"
        self.different_content = "完全不同的文本内容，与原始文本没有相似性。"
        
        # 创建临时目录和文件
        self.temp_dir = tempfile.mkdtemp()
        self.orig_file = os.path.join(self.temp_dir, 'orig.txt')
        self.plag_file = os.path.join(self.temp_dir, 'plag.txt')
        self.different_file = os.path.join(self.temp_dir, 'different.txt')
        
        with open(self.orig_file, 'w', encoding='utf-8') as f:
            f.write(self.orig_content)
        
        with open(self.plag_file, 'w', encoding='utf-8') as f:
            f.write(self.plag_content)
            
        with open(self.different_file, 'w', encoding='utf-8') as f:
            f.write(self.different_content)
    
    def tearDown(self):
        # 清理临时文件
        os.remove(self.orig_file)
        os.remove(self.plag_file)
        os.remove(self.different_file)
        os.rmdir(self.temp_dir)
    
    def test_read_file(self):
        # 测试文件读取功能
        content = read_file(self.orig_file)
        self.assertEqual(content, self.orig_content)
    
    def test_read_file_not_found(self):
        # 测试读取不存在的文件
        # 重定向stderr以避免在测试输出中显示错误信息
        old_stderr = sys.stderr
        sys.stderr = StringIO()
        
        with self.assertRaises(SystemExit):
            read_file(os.path.join(self.temp_dir, 'nonexistent.txt'))
            
        # 恢复stderr
        sys.stderr = old_stderr
    
    def test_cut_text(self):
        # 测试文本分词功能
        words = cut_text("这是一个测试")
        self.assertIsInstance(words, list)
        self.assertGreater(len(words), 0)
    
    def test_get_word_frequency(self):
        # 测试词频统计功能
        words = ['这', '是', '一个', '测试', '这']
        freq = get_word_frequency(words)
        self.assertEqual(freq['这'], 2)
        self.assertEqual(freq['是'], 1)
    
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
        
if __name__ == '__main__':
    unittest.main()