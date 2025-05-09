package com.example.demo;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.Predicate;

/**
 * 数据管理器，包含多个内部类，用于管理数据处理器
 */
public class DataManager {
    
    // 字段
    private final Map<String, DataProcessor<?, ?>> processors;
    private final Cache cache;
    private final Logger logger;
    private final Configuration config;
    private int maxProcessors;
    private boolean initialized;
    
    /**
     * 内部缓存类
     */
    public class Cache {
        private final Map<String, Object> cacheData;
        private final long expiryTimeMs;
        private final int maxEntries;
        
        public Cache(int maxEntries, long expiryTimeMs) {
            this.cacheData = new ConcurrentHashMap<>();
            this.maxEntries = maxEntries;
            this.expiryTimeMs = expiryTimeMs;
        }
        
        public void put(String key, Object value) {
            if (cacheData.size() >= maxEntries) {
                // 简单的缓存淘汰策略，仅作演示
                cacheData.clear();
            }
            
            // 包装值与时间戳
            CacheEntry entry = new CacheEntry(value, System.currentTimeMillis());
            cacheData.put(key, entry);
        }
        
        public Object get(String key) {
            Object entry = cacheData.get(key);
            if (entry == null) {
                return null;
            }
            
            CacheEntry cacheEntry = (CacheEntry) entry;
            
            // 检查是否过期
            if (System.currentTimeMillis() - cacheEntry.timestamp > expiryTimeMs) {
                cacheData.remove(key);
                return null;
            }
            
            return cacheEntry.value;
        }
        
        /**
         * 缓存条目，包含值和时间戳
         */
        private class CacheEntry {
            private final Object value;
            private final long timestamp;
            
            public CacheEntry(Object value, long timestamp) {
                this.value = value;
                this.timestamp = timestamp;
            }
        }
        
        public int size() {
            return cacheData.size();
        }
        
        public void clear() {
            cacheData.clear();
        }
    }
    
    /**
     * 日志记录器，静态内部类
     */
    public static class Logger {
        private final String logPrefix;
        private final List<String> logEntries;
        private final AtomicInteger errorCount;
        
        public Logger(String logPrefix) {
            this.logPrefix = logPrefix;
            this.logEntries = new ArrayList<>();
            this.errorCount = new AtomicInteger(0);
        }
        
        public void info(String message) {
            String entry = logPrefix + " [INFO] " + message;
            logEntries.add(entry);
            System.out.println(entry);
        }
        
        public void error(String message, Throwable error) {
            String entry = logPrefix + " [ERROR] " + message + 
                    (error != null ? ": " + error.getMessage() : "");
            logEntries.add(entry);
            System.err.println(entry);
            errorCount.incrementAndGet();
        }
        
        public List<String> getLogEntries() {
            return new ArrayList<>(logEntries);
        }
        
        public int getErrorCount() {
            return errorCount.get();
        }
        
        public void clear() {
            logEntries.clear();
            errorCount.set(0);
        }
        
        /**
         * 日志过滤器，用于筛选日志
         */
        public static class LogFilter {
            private final Predicate<String> filter;
            
            public LogFilter(Predicate<String> filter) {
                this.filter = filter;
            }
            
            public List<String> filter(List<String> logs) {
                List<String> filtered = new ArrayList<>();
                for (String log : logs) {
                    if (filter.test(log)) {
                        filtered.add(log);
                    }
                }
                return filtered;
            }
        }
    }
    
    /**
     * 配置类，用于管理配置信息
     */
    public static class Configuration {
        private final Map<String, String> properties;
        
        public Configuration() {
            this.properties = new HashMap<>();
            // 设置默认值
            properties.put("cache.size", "1000");
            properties.put("cache.expiry", "3600000");
            properties.put("max.processors", "10");
        }
        
        public void setProperty(String key, String value) {
            properties.put(key, value);
        }
        
        public String getProperty(String key) {
            return properties.get(key);
        }
        
        public String getProperty(String key, String defaultValue) {
            return properties.getOrDefault(key, defaultValue);
        }
        
        public int getIntProperty(String key, int defaultValue) {
            String value = properties.get(key);
            if (value == null) {
                return defaultValue;
            }
            
            try {
                return Integer.parseInt(value);
            } catch (NumberFormatException e) {
                return defaultValue;
            }
        }
        
        public long getLongProperty(String key, long defaultValue) {
            String value = properties.get(key);
            if (value == null) {
                return defaultValue;
            }
            
            try {
                return Long.parseLong(value);
            } catch (NumberFormatException e) {
                return defaultValue;
            }
        }
        
        /**
         * 配置监听器，用于监听配置变更
         */
        public interface ConfigChangeListener {
            void onConfigChanged(String key, String oldValue, String newValue);
        }
        
        // 监听器列表
        private final List<ConfigChangeListener> listeners = new ArrayList<>();
        
        public void addListener(ConfigChangeListener listener) {
            listeners.add(listener);
        }
        
        public void removeListener(ConfigChangeListener listener) {
            listeners.remove(listener);
        }
        
        private void notifyListeners(String key, String oldValue, String newValue) {
            for (ConfigChangeListener listener : listeners) {
                listener.onConfigChanged(key, oldValue, newValue);
            }
        }
    }
    
    /**
     * 异常类，用于标识DataManager异常
     */
    public static class DataManagerException extends RuntimeException {
        private final String errorCode;
        
        public DataManagerException(String message, String errorCode) {
            super(message);
            this.errorCode = errorCode;
        }
        
        public DataManagerException(String message, String errorCode, Throwable cause) {
            super(message, cause);
            this.errorCode = errorCode;
        }
        
        public String getErrorCode() {
            return errorCode;
        }
    }
    
    /**
     * 构造函数
     */
    public DataManager() {
        this.processors = new HashMap<>();
        this.config = new Configuration();
        this.logger = new Logger("DataManager");
        this.maxProcessors = config.getIntProperty("max.processors", 10);
        this.cache = new Cache(
                config.getIntProperty("cache.size", 1000),
                config.getLongProperty("cache.expiry", 3600000)
        );
        this.initialized = false;
    }
    
    /**
     * 初始化管理器
     */
    public void initialize() {
        if (initialized) {
            logger.info("DataManager already initialized");
            return;
        }
        
        try {
            logger.info("Initializing DataManager");
            // 执行初始化逻辑
            initialized = true;
            logger.info("DataManager initialized successfully");
        } catch (Exception e) {
            logger.error("Failed to initialize DataManager", e);
            throw new DataManagerException("Initialization failed", "INIT_ERROR", e);
        }
    }
    
    /**
     * 注册处理器
     */
    public <T, R> void registerProcessor(String name, DataProcessor<T, R> processor) {
        if (processors.size() >= maxProcessors) {
            throw new DataManagerException("Maximum number of processors reached", "MAX_PROCESSORS");
        }
        
        processors.put(name, processor);
        logger.info("Registered processor: " + name);
    }
    
    /**
     * 获取处理器
     */
    @SuppressWarnings("unchecked")
    public <T, R> DataProcessor<T, R> getProcessor(String name) {
        return (DataProcessor<T, R>) processors.get(name);
    }
    
    /**
     * 移除处理器
     */
    public void removeProcessor(String name) {
        processors.remove(name);
        logger.info("Removed processor: " + name);
    }
    
    /**
     * 关闭管理器
     */
    public void shutdown() {
        if (!initialized) {
            logger.info("DataManager not initialized, nothing to shutdown");
            return;
        }
        
        logger.info("Shutting down DataManager");
        
        // 关闭所有处理器
        for (Map.Entry<String, DataProcessor<?, ?>> entry : processors.entrySet()) {
            try {
                entry.getValue().cleanup();
                logger.info("Processor cleaned up: " + entry.getKey());
            } catch (Exception e) {
                logger.error("Error cleaning up processor: " + entry.getKey(), e);
            }
        }
        
        processors.clear();
        cache.clear();
        initialized = false;
        
        logger.info("DataManager shutdown complete");
    }
    
    /**
     * 获取缓存实例
     */
    public Cache getCache() {
        return cache;
    }
    
    /**
     * 获取日志记录器
     */
    public Logger getLogger() {
        return logger;
    }
    
    /**
     * 获取配置
     */
    public Configuration getConfig() {
        return config;
    }
    
    /**
     * 检查是否初始化
     */
    public boolean isInitialized() {
        return initialized;
    }
} 