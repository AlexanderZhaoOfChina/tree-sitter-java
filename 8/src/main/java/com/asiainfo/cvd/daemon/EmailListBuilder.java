package com.asiainfo.cvd.daemon;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.support.PropertiesLoaderUtils;

import javax.validation.constraints.NotEmpty;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Properties;

/**
 * 邮件列表构建器
 * 负责从配置文件中读取并构建邮件收件人和抄送人列表
 * 支持测试模式和正式模式的邮件发送
 */
public class EmailListBuilder {
    private static final Logger logger = LoggerFactory.getLogger(EmailListBuilder.class);
    private static final Properties properties = new Properties();
    private static boolean initialized = false;

    /**
     * 初始化配置文件
     * 如果配置未初始化，则加载application.properties配置文件
     * 配置文件应位于classpath的根目录下
     * 
     * @throws RuntimeException 当配置文件不存在或无法加载时抛出
     */
    private static void initializeIfNeeded() {
        if (!initialized) {
            try {
                properties.putAll(PropertiesLoaderUtils.loadProperties(new ClassPathResource("application.properties")));
                initialized = true;
            } catch (IOException e) {
                logger.error("加载application.properties配置文件失败", e);
                throw new RuntimeException("加载application.properties配置文件失败", e);
            }
        }
    }

    /**
     * 判断当前是否为测试模式
     * 从配置文件中读取email.test.mode属性，默认为false
     *
     * @return 如果是测试模式返回true，否则返回false
     */
    private static boolean isTestMode() {
        initializeIfNeeded();
        return Boolean.parseBoolean(properties.getProperty("email.test.mode", "false"));
    }

    /**
     * 解析邮件列表字符串
     * 将逗号分隔的邮件地址字符串转换为List
     *
     * @param propertyValue 包含邮件地址的字符串，多个地址用逗号分隔
     * @return 邮件地址列表
     */
    private static List<String> parseEmailList(String propertyValue) {
        if (propertyValue == null || propertyValue.trim().isEmpty()) {
            return new ArrayList<>();
        }
        return Arrays.asList(propertyValue.split(","));
    }

    /**
     * 获取专家邮件列表
     * 如果是测试模式，则返回测试邮箱地址
     * 如果是正式模式，则返回配置文件中定义的专家邮箱列表
     *
     * @return 专家邮箱地址列表
     * @throws RuntimeException 当邮件列表为空时可能抛出（由@NotEmpty注解控制）
     */
    public static @NotEmpty(message = "邮件收件人不能为空") List<String> getExpertEmails() {
        initializeIfNeeded();
        
        if (isTestMode()) {
            List<String> testEmails = new ArrayList<>();
            testEmails.add(properties.getProperty("email.test.address", "zhaolx5@asiainfo.com"));
            return testEmails;
        }

        String expertList = properties.getProperty("email.expert.list");
        List<String> expertEmails = parseEmailList(expertList);
        
        if (expertEmails.isEmpty()) {
            logger.warn("专家邮箱列表为空");
        }
        
        return expertEmails;
    }

    /**
     * 获取抄送邮件列表
     * 如果是测试模式，则返回空列表
     * 如果是正式模式，则返回配置文件中定义的抄送邮箱列表
     *
     * @return 抄送邮箱地址列表
     */
    public static @NotEmpty(message = "邮件抄送人不能为空") List<String> getCcEmails() {
        initializeIfNeeded();
        
        if (isTestMode()) {
            return new ArrayList<>();
        }

        String ccList = properties.getProperty("email.cc.list");
        List<String> ccEmails = parseEmailList(ccList);
        
        if (ccEmails.isEmpty()) {
            logger.warn("抄送邮箱列表为空");
        }
        
        return ccEmails;
    }
}
