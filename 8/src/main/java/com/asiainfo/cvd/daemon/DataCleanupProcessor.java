package com.asiainfo.cvd.daemon;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.nio.file.*;
import java.util.Comparator;
import java.util.stream.Stream;

/**
 * 数据清理工具类
 */
public class DataCleanupProcessor {
    private static final Logger logger = LoggerFactory.getLogger(DataCleanupProcessor.class);

    /**
     * 清理数据存储目录
     */
    public static void cleanupDataStore() {
        try {
            Path dataStorePath = Paths.get("data_store");
            if (Files.exists(dataStorePath)) {
                // 使用walk遍历目录下所有文件和子目录，并按照从深到浅的顺序删除
                try (Stream<Path> walk = Files.walk(dataStorePath)) {
                    walk.sorted(Comparator.reverseOrder())
                        .forEach(path -> {
                            try {
                                Files.delete(path);
                                logger.info("已删除: {}", path);
                            } catch (IOException e) {
                                logger.error("删除文件失败: {}", path, e);
                            }
                        });
                }
                logger.info("data_store目录清理完成");
            } else {
                logger.info("data_store目录不存在");
            }
        } catch (IOException e) {
            logger.error("清理data_store目录时发生错误", e);
        }
    }

    /**
     * 删除process_status.json文件
     */
    public static void deleteProcessStatus() {
        Path processStatusPath = Paths.get("process_status.json");
        try {
            if (Files.deleteIfExists(processStatusPath)) {
                logger.info("process_status.json文件已删除");
            } else {
                logger.info("process_status.json文件不存在");
            }
        } catch (IOException e) {
            logger.error("删除process_status.json文件时发生错误", e);
        }
    }

    /**
     * 移动备份文件到上级目录
     */
    public static void moveBackupFile() {
        Path sourcePath = Paths.get("cnvd", "backup", "2025-01-13_2025-01-19.xml");
        Path targetPath = Paths.get("cnvd","2025-01-13_2025-01-19.xml");
        
        try {
            if (Files.exists(sourcePath)) {
                Files.move(sourcePath, targetPath, StandardCopyOption.REPLACE_EXISTING);
                logger.info("备份文件已移动到: {}", targetPath);
            } else {
                logger.warn("源文件不存在: {}", sourcePath);
            }
        } catch (IOException e) {
            logger.error("移动备份文件时发生错误", e);
        }
    }

    public static void moveBackupExceptionFile() {
        Path sourcePath = Paths.get("cnvd", "backup_for_exception", "2025-01-13_2025-01-19.xml");
        Path targetPath = Paths.get("cnvd","2025-01-13_2025-01-19.xml");
        
        try {
            if (Files.exists(sourcePath)) {
                Files.move(sourcePath, targetPath, StandardCopyOption.REPLACE_EXISTING);
                logger.info("备份文件已移动到: {}", targetPath);
            } else {
                logger.warn("源文件不存在: {}", sourcePath);
            }
        } catch (IOException e) {
            logger.error("移动备份文件时发生错误", e);
        }
    }

    /**
     * 执行所有清理操作
     */
    public static void performFullCleanup() {
        logger.info("开始执行数据清理操作...");
        
        cleanupDataStore();
        deleteProcessStatus();
        moveBackupFile();
        moveBackupExceptionFile();

        logger.info("数据清理操作完成");
    }

    public static void main(String[] args) {
        performFullCleanup();
    }
} 