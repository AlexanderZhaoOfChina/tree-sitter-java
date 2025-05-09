package com.example.demo;

import java.util.List;
import java.util.Map;
import java.util.HashMap;
import java.util.Date;

/**
 * 数据处理抽象类，定义了数据处理的基本框架
 */
public abstract class AbstractProcessor<T, R> {
    
    // 字段
    protected String processorName;
    protected Map<String, Object> configuration;
    protected boolean isActive;
    protected long startTime;
    
    // 构造函数
    public AbstractProcessor(String processorName) {
        this.processorName = processorName;
        this.configuration = new HashMap<>();
        this.isActive = false;
        this.startTime = System.currentTimeMillis();
    }
    
    // 抽象方法，由子类实现
    protected abstract R processData(T data);
    protected abstract void validate(T data) throws IllegalArgumentException;
    
    // 具体实现的方法
    public final R execute(T data) {
        // 记录开始时间
        long execStartTime = System.currentTimeMillis();
        
        try {
            // 前置校验
            validate(data);
            
            // 核心处理逻辑
            R result = processData(data);
            
            // 日志记录
            logExecution(data, result, execStartTime);
            
            return result;
        } catch (Exception e) {
            handleError(e, data);
            throw e;
        }
    }
    
    // 受保护的普通方法
    protected void logExecution(T data, R result, long startTime) {
        long executionTime = System.currentTimeMillis() - startTime;
        System.out.println("Processor: " + processorName + " executed in " + executionTime + "ms");
    }
    
    protected void handleError(Exception e, T data) {
        System.err.println("Error processing data in " + processorName + ": " + e.getMessage());
    }
    
    // 公共访问方法
    public void setConfiguration(String key, Object value) {
        this.configuration.put(key, value);
    }
    
    public Object getConfiguration(String key) {
        return this.configuration.get(key);
    }
    
    public String getProcessorName() {
        return processorName;
    }
    
    public void setActive(boolean active) {
        this.isActive = active;
    }
    
    public boolean isActive() {
        return isActive;
    }
} 