package com.example.demo;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * JSON数据处理器，实现了DataProcessor接口
 */
public class JsonDataProcessor implements DataProcessor<String, Map<String, Object>> {
    
    private boolean initialized;
    private String configString;
    private int processedCount;
    private long lastProcessTime;
    
    // 内部使用的配置类
    private static class ProcessorConfig {
        private boolean validateInput;
        private int maxBatchSize;
        private String encoding;
        
        public ProcessorConfig(String config) {
            // 简单解析配置字符串
            this.validateInput = config.contains("validate=true");
            this.maxBatchSize = 100; // 默认值
            this.encoding = "UTF-8"; // 默认值
            
            // 提取maxBatchSize配置
            if (config.contains("maxBatchSize=")) {
                String[] parts = config.split("maxBatchSize=");
                if (parts.length > 1) {
                    String sizeStr = parts[1].split(",")[0];
                    try {
                        this.maxBatchSize = Integer.parseInt(sizeStr);
                    } catch (NumberFormatException e) {
                        // 使用默认值
                    }
                }
            }
            
            // 提取encoding配置
            if (config.contains("encoding=")) {
                String[] parts = config.split("encoding=");
                if (parts.length > 1) {
                    this.encoding = parts[1].split(",")[0];
                }
            }
        }
        
        public boolean isValidateInput() {
            return validateInput;
        }
        
        public int getMaxBatchSize() {
            return maxBatchSize;
        }
        
        public String getEncoding() {
            return encoding;
        }
    }
    
    private ProcessorConfig config;
    
    public JsonDataProcessor() {
        this.initialized = false;
        this.processedCount = 0;
        this.lastProcessTime = 0;
    }
    
    @Override
    public Map<String, Object> process(String input) {
        if (!initialized) {
            throw new IllegalStateException("Processor not initialized");
        }
        
        // 记录处理时间
        this.lastProcessTime = System.currentTimeMillis();
        
        // 验证输入
        if (config.isValidateInput() && (input == null || input.trim().isEmpty())) {
            throw new IllegalArgumentException("Input cannot be null or empty");
        }
        
        // 模拟JSON解析
        Map<String, Object> result = parseJson(input);
        
        // 更新计数器
        this.processedCount++;
        
        return result;
    }
    
    @Override
    public List<Map<String, Object>> processBatch(List<String> inputs) {
        if (!initialized) {
            throw new IllegalStateException("Processor not initialized");
        }
        
        if (inputs == null) {
            throw new IllegalArgumentException("Input list cannot be null");
        }
        
        // 检查批量大小
        if (inputs.size() > config.getMaxBatchSize()) {
            throw new IllegalArgumentException("Batch size exceeds maximum allowed: " + config.getMaxBatchSize());
        }
        
        List<Map<String, Object>> results = new ArrayList<>();
        
        // 处理每个输入
        for (String input : inputs) {
            results.add(process(input));
        }
        
        return results;
    }
    
    @Override
    public void initialize(String config) {
        this.configString = config;
        this.config = new ProcessorConfig(config);
        this.initialized = true;
        this.processedCount = 0;
        this.lastProcessTime = System.currentTimeMillis();
        
        System.out.println("JsonDataProcessor initialized with config: " + config);
    }
    
    @Override
    public void cleanup() {
        System.out.println("JsonDataProcessor cleaned up. Processed " + processedCount + " items.");
        this.initialized = false;
    }
    
    @Override
    public boolean isReady() {
        return initialized;
    }
    
    // 辅助方法：模拟JSON解析
    private Map<String, Object> parseJson(String jsonString) {
        Map<String, Object> result = new HashMap<>();
        
        // 这里是一个非常简化的JSON解析模拟
        // 实际应用中会使用Jackson、Gson等库
        if (jsonString.contains(":")) {
            String[] entries = jsonString.replace("{", "").replace("}", "").split(",");
            for (String entry : entries) {
                if (entry.contains(":")) {
                    String[] keyValue = entry.split(":");
                    if (keyValue.length == 2) {
                        String key = keyValue[0].trim().replace("\"", "");
                        String value = keyValue[1].trim().replace("\"", "");
                        result.put(key, value);
                    }
                }
            }
        }
        
        return result;
    }
    
    // 额外的非接口方法
    public int getProcessedCount() {
        return processedCount;
    }
    
    public long getLastProcessTime() {
        return lastProcessTime;
    }
    
    public String getConfigString() {
        return configString;
    }
} 