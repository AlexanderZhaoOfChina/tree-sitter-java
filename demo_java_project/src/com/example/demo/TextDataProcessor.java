package com.example.demo;

import java.util.HashMap;
import java.util.Map;
import java.util.regex.Pattern;

/**
 * 文本数据处理器，继承自AbstractProcessor
 */
public class TextDataProcessor extends AbstractProcessor<String, Map<String, Integer>> {
    
    private Pattern wordPattern;
    private int minWordLength;
    private boolean caseSensitive;
    private Map<String, Integer> wordCache;
    
    /**
     * 构造函数
     */
    public TextDataProcessor() {
        super("TextDataProcessor");
        this.wordPattern = Pattern.compile("\\b\\w+\\b");
        this.minWordLength = 2;
        this.caseSensitive = false;
        this.wordCache = new HashMap<>();
    }
    
    /**
     * 设置最小单词长度
     */
    public void setMinWordLength(int minWordLength) {
        if (minWordLength < 1) {
            throw new IllegalArgumentException("Minimum word length must be at least 1");
        }
        this.minWordLength = minWordLength;
    }
    
    /**
     * 设置大小写敏感
     */
    public void setCaseSensitive(boolean caseSensitive) {
        this.caseSensitive = caseSensitive;
    }
    
    @Override
    protected Map<String, Integer> processData(String text) {
        if (text == null || text.isEmpty()) {
            return new HashMap<>();
        }
        
        // 转换大小写（如果需要）
        String processedText = caseSensitive ? text : text.toLowerCase();
        
        // 使用正则表达式匹配单词
        java.util.regex.Matcher matcher = wordPattern.matcher(processedText);
        Map<String, Integer> wordCount = new HashMap<>();
        
        // 统计单词频率
        while (matcher.find()) {
            String word = matcher.group();
            
            // 过滤短单词
            if (word.length() < minWordLength) {
                continue;
            }
            
            // 更新单词计数
            wordCount.put(word, wordCount.getOrDefault(word, 0) + 1);
        }
        
        // 缓存结果
        this.wordCache = new HashMap<>(wordCount);
        
        return wordCount;
    }
    
    @Override
    protected void validate(String data) throws IllegalArgumentException {
        if (data == null) {
            throw new IllegalArgumentException("Input text cannot be null");
        }
    }
    
    /**
     * 获取特定单词的计数
     */
    public int getWordCount(String word) {
        if (!caseSensitive) {
            word = word.toLowerCase();
        }
        return wordCache.getOrDefault(word, 0);
    }
    
    /**
     * 获取总单词数
     */
    public int getTotalWordCount() {
        int total = 0;
        for (int count : wordCache.values()) {
            total += count;
        }
        return total;
    }
    
    /**
     * 获取唯一单词数
     */
    public int getUniqueWordCount() {
        return wordCache.size();
    }
    
    /**
     * 清除缓存
     */
    public void clearCache() {
        wordCache.clear();
    }
} 