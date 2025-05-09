package com.example.demo;

import java.util.List;

/**
 * 数据处理器接口，定义了数据处理的基本契约
 */
public interface DataProcessor<T, R> {
    
    /**
     * 处理数据方法
     * @param input 输入数据
     * @return 处理结果
     */
    R process(T input);
    
    /**
     * 批量处理数据
     * @param inputs 多个输入数据
     * @return 处理结果列表
     */
    List<R> processBatch(List<T> inputs);
    
    /**
     * 初始化处理器
     * @param config 配置信息
     */
    void initialize(String config);
    
    /**
     * 清理资源
     */
    void cleanup();
    
    /**
     * 检查处理器状态
     * @return 是否可用
     */
    boolean isReady();
} 