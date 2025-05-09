package com.example.demo;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * 示例程序的主类，演示所有创建的类的使用
 */
public class Main {
    
    public static void main(String[] args) {
        System.out.println("=== 数据处理演示程序 ===");
        
        // 创建数据管理器
        DataManager dataManager = new DataManager();
        dataManager.initialize();
        
        try {
            // 演示抽象类的使用
            demoAbstractProcessor();
            
            // 演示接口和实现类
            demoInterfaceImplementation();
            
            // 演示内部类
            demoInnerClasses(dataManager);
            
        } catch (Exception e) {
            System.err.println("程序执行出错: " + e.getMessage());
            e.printStackTrace();
        } finally {
            // 关闭数据管理器
            dataManager.shutdown();
        }
        
        System.out.println("\n=== 程序执行完毕 ===");
    }
    
    /**
     * 演示抽象类的使用
     */
    private static void demoAbstractProcessor() {
        System.out.println("\n--- 抽象类演示 ---");
        
        // 创建TextDataProcessor实例（继承自AbstractProcessor）
        TextDataProcessor textProcessor = new TextDataProcessor();
        textProcessor.setActive(true);
        textProcessor.setMinWordLength(3);
        textProcessor.setCaseSensitive(false);
        
        // 设置配置
        textProcessor.setConfiguration("maxWordLength", 20);
        
        // 处理文本数据
        String sampleText = "这是一个Java示例程序，用于演示抽象类、接口和内部类的使用。"
                + "Java是一种面向对象的编程语言，支持继承、多态和封装等特性。";
        
        Map<String, Integer> result = textProcessor.execute(sampleText);
        
        System.out.println("文本处理结果:");
        System.out.println("- 唯一单词数: " + textProcessor.getUniqueWordCount());
        System.out.println("- 总单词数: " + textProcessor.getTotalWordCount());
        System.out.println("- 单词频率统计:");
        
        for (Map.Entry<String, Integer> entry : result.entrySet()) {
            if (entry.getValue() > 1) {  // 只显示出现多次的单词
                System.out.println("  " + entry.getKey() + ": " + entry.getValue());
            }
        }
    }
    
    /**
     * 演示接口和实现类
     */
    private static void demoInterfaceImplementation() {
        System.out.println("\n--- 接口和实现类演示 ---");
        
        // 创建JsonDataProcessor实例（实现DataProcessor接口）
        JsonDataProcessor jsonProcessor = new JsonDataProcessor();
        
        // 初始化处理器
        jsonProcessor.initialize("validate=true,maxBatchSize=50,encoding=UTF-8");
        
        // 处理单个JSON
        String sampleJson = "{\"name\":\"张三\",\"age\":30,\"city\":\"北京\"}";
        Map<String, Object> result = jsonProcessor.process(sampleJson);
        
        System.out.println("JSON处理结果:");
        for (Map.Entry<String, Object> entry : result.entrySet()) {
            System.out.println("  " + entry.getKey() + ": " + entry.getValue());
        }
        
        // 批量处理JSON
        List<String> jsonBatch = new ArrayList<>();
        jsonBatch.add("{\"name\":\"李四\",\"age\":25,\"city\":\"上海\"}");
        jsonBatch.add("{\"name\":\"王五\",\"age\":35,\"city\":\"广州\"}");
        
        List<Map<String, Object>> batchResults = jsonProcessor.processBatch(jsonBatch);
        
        System.out.println("\n批量处理结果:");
        for (int i = 0; i < batchResults.size(); i++) {
            System.out.println("记录 " + (i + 1) + ":");
            for (Map.Entry<String, Object> entry : batchResults.get(i).entrySet()) {
                System.out.println("  " + entry.getKey() + ": " + entry.getValue());
            }
        }
        
        // 清理处理器
        jsonProcessor.cleanup();
    }
    
    /**
     * 演示内部类的使用
     */
    private static void demoInnerClasses(DataManager dataManager) {
        System.out.println("\n--- 内部类演示 ---");
        
        // 使用非静态内部类 - Cache
        DataManager.Cache cache = dataManager.getCache();
        cache.put("user1", "张三");
        cache.put("user2", "李四");
        
        System.out.println("缓存大小: " + cache.size());
        System.out.println("缓存内容:");
        System.out.println("- user1: " + cache.get("user1"));
        System.out.println("- user2: " + cache.get("user2"));
        
        // 使用静态内部类 - Logger
        DataManager.Logger logger = dataManager.getLogger();
        logger.info("这是一条信息日志");
        logger.error("这是一条错误日志", null);
        
        // 使用静态内部类的内部类 - LogFilter
        DataManager.Logger.LogFilter errorFilter = new DataManager.Logger.LogFilter(
                log -> log.contains("[ERROR]")
        );
        
        List<String> allLogs = logger.getLogEntries();
        List<String> errorLogs = errorFilter.filter(allLogs);
        
        System.out.println("\n所有日志数量: " + allLogs.size());
        System.out.println("错误日志数量: " + errorLogs.size());
        
        // 使用接口内部类 - ConfigChangeListener
        DataManager.Configuration config = dataManager.getConfig();
        
        // 创建匿名内部类实现接口
        config.addListener(new DataManager.Configuration.ConfigChangeListener() {
            @Override
            public void onConfigChanged(String key, String oldValue, String newValue) {
                System.out.println("配置变更: " + key + " 从 " + oldValue + " 变为 " + newValue);
            }
        });
        
        // 测试参数获取
        System.out.println("\n配置参数:");
        System.out.println("- cache.size: " + config.getIntProperty("cache.size", 0));
        System.out.println("- cache.expiry: " + config.getLongProperty("cache.expiry", 0));
    }
} 