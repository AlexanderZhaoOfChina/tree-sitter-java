package com.asiainfo.utils;

import com.asiainfo.cvd.model.BoComponent;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;

import java.io.File;
import java.io.IOException;
import java.sql.*;
import java.util.*;

/**
 * 配置数据导出工具
 * 从数据库中提取配置数据并生成JSON配置文件
 */
public class ConfigurationExporter {
    
    private static final String CONFIG_DIR = "D:\\CNVD\\config";
    private static final ObjectMapper objectMapper = new ObjectMapper()
            .enable(SerializationFeature.INDENT_OUTPUT);

    private final String dbUrl;
    private final String dbUser;
    private final String dbPassword;

    public ConfigurationExporter(String dbUrl, String dbUser, String dbPassword) {
        this.dbUrl = dbUrl;
        this.dbUser = dbUser;
        this.dbPassword = dbPassword;
    }

    /**
     * 导出所有配置
     */
    public void exportAllConfigurations() throws SQLException, IOException {
        // 确保配置目录存在
        createConfigDirectory();

        try (Connection conn = DriverManager.getConnection(dbUrl, dbUser, dbPassword)) {
            // 导出组件配置
            exportComponents(conn);
            // 导出组件过滤规则
            exportComponentFilters(conn);
        }
    }

    /**
     * 导出组件配置
     */
    private void exportComponents(Connection conn) throws SQLException, IOException {
        List<BoComponent> components = new ArrayList<>();
        
        String sql = "SELECT component_name, component_version, description FROM component";
        try (PreparedStatement stmt = conn.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {
            
            while (rs.next()) {
                BoComponent component = new BoComponent();
                component.setComponentName(rs.getString("component_name"));
                component.setComponentVersion(rs.getString("component_version"));
                component.setComponentDescribe(rs.getString("description"));
                components.add(component);
            }
        }

        // 保存到components.json
        File componentsFile = new File(CONFIG_DIR, "components.json");
        objectMapper.writeValue(componentsFile, components);
        System.out.println("Components configuration exported to: " + componentsFile.getAbsolutePath());
    }

    /**
     * 导出组件过滤规则
     */
    private void exportComponentFilters(Connection conn) throws SQLException, IOException {
        String sql = "SELECT component_name, filter_name FROM component_filter";
        Map<String, List<String>> filterMap = new HashMap<>();

        try (PreparedStatement stmt = conn.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {
            
            while (rs.next()) {
                String componentName = rs.getString("component_name");
                String filterName = rs.getString("filter_name");
                
                filterMap.computeIfAbsent(componentName, k -> new ArrayList<>())
                        .add(filterName);
            }
        }

        // 为每个组件生成过滤规则文件
        for (Map.Entry<String, List<String>> entry : filterMap.entrySet()) {
            String componentName = entry.getKey();
            List<String> filters = entry.getValue();
            
            File filterFile = new File(CONFIG_DIR, componentName + "_filters.json");
            objectMapper.writeValue(filterFile, filters);
            System.out.println("Filter configuration for " + componentName + " exported to: " + filterFile.getAbsolutePath());
        }
    }

    /**
     * 确保配置目录存在
     */
    private void createConfigDirectory() {
        File configDir = new File(CONFIG_DIR);
        if (!configDir.exists()) {
            configDir.mkdirs();
        }
    }

    /**
     * 使用示例
     */
    public static void main(String[] args) {
        String dbUrl = "jdbc:mysql://localhost:3306/cve";
        String dbUser = "root";
        String dbPassword = "1qaz2wsx";

        try {
            ConfigurationExporter exporter = new ConfigurationExporter(dbUrl, dbUser, dbPassword);
            exporter.exportAllConfigurations();
            System.out.println("Configuration export completed successfully.");
        } catch (Exception e) {
            System.err.println("Error exporting configurations: " + e.getMessage());
            e.printStackTrace();
        }
    }
} 