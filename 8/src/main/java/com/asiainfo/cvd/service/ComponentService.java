package com.asiainfo.cvd.service;

import com.asiainfo.cvd.model.BoComponent;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

import java.io.*;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;

public class ComponentService {
    private static final Logger logger = LoggerFactory.getLogger(ComponentService.class);
    
    // 基础目录（程序运行目录）
    private static final String BASE_DIR = System.getProperty("user.dir");
    
    // 组件配置文件路径
    private static final String COMPONENTS_CONFIG_PATH = Paths.get(BASE_DIR, "config", "Components.xlsx").toString();
    
    // 组件过滤规则配置文件路径
    private static final String COMPONENT_FILTERS_PATH = Paths.get(BASE_DIR, "config", "ComponentFilters.xlsx").toString();

    /**
     * 从Excel文件读取组件配置
     */
    public List<BoComponent> readComponentsFromExcel() throws IOException {
        List<BoComponent> components = new ArrayList<>();
        
        File configFile = new File(COMPONENTS_CONFIG_PATH);
        if (!configFile.exists()) {
            logger.error("配置文件不存在: {}", COMPONENTS_CONFIG_PATH);
            throw new IOException("配置文件不存在: " + COMPONENTS_CONFIG_PATH);
        }
        
        try (InputStream is = new FileInputStream(configFile);
             Workbook workbook = new XSSFWorkbook(is)) {
            Sheet sheet = workbook.getSheetAt(0);
            // 跳过标题行
            Iterator<Row> rowIterator = sheet.iterator();
            if (rowIterator.hasNext()) {
                rowIterator.next(); // 跳过标题行
            }
            
            while (rowIterator.hasNext()) {
                Row row = rowIterator.next();
                BoComponent component = new BoComponent();
                
                // 读取每个字段
                component.setId(Long.valueOf(getIntValue(row.getCell(0))));
                component.setComponentName(getStringValue(row.getCell(1)));
                component.setComponentDescribe(getStringValue(row.getCell(2)));
                component.setUseCount(Long.valueOf(getIntValue(row.getCell(3))));
                component.setUseCountExcludeBss(Long.valueOf(getIntValue(row.getCell(4))));
                component.setBelongDirectoryName(getStringValue(row.getCell(5)));
                component.setBelongDirectoryId(Long.valueOf(getIntValue(row.getCell(6))));
                component.setOfficialLink(getStringValue(row.getCell(7)));
                component.setSourceCodeLink(getStringValue(row.getCell(8)));
                component.setLastVersion(getStringValue(row.getCell(9)));
                
                // 修改日期时间解析逻辑
                String dateStr = getStringValue(row.getCell(10));
                LocalDateTime dateTime;
                try {
                    // 尝试解析带T的格式
                    dateTime = LocalDateTime.parse(dateStr);
                    component.setLastModifiedDate(dateTime);
                } catch (Exception e) {
                    try {
                        // 如果失败，尝试解析标准格式
                        dateTime = LocalDateTime.parse(dateStr, DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
                        component.setLastModifiedDate(dateTime);
                    } catch (Exception e2) {
                        // 如果还是失败，无需设置为当前时间
                        //dateTime = LocalDateTime.now();
                        //logger.warn("Warning: Could not parse date '{}', using current time instead", dateStr);
                    }
                }

                component.setLicenseType(getStringValue(row.getCell(11)));
                component.setVendor(getStringValue(row.getCell(12)));
                component.setVendorCountry(getStringValue(row.getCell(13)));
                component.setCveProductName(getStringValue(row.getCell(14)));
                /**
                component.setBelongDomain(getStringValue(row.getCell(15)));
                component.setIsComponentLib(getStringValue(row.getCell(16)));
                component.setIsIndepend(getStringValue(row.getCell(17)));
                component.setIsForDevolop(getStringValue(row.getCell(18)));
                component.setReplaceCost(getStringValue(row.getCell(19)));
                component.setIsIncreaseMarket(getStringValue(row.getCell(20)));
                component.setIsDecreaseMarket(getStringValue(row.getCell(21)));
                component.setBelongType(getStringValue(row.getCell(22)));
                component.setIsOpenSource(getStringValue(row.getCell(23)));
                component.setCompanyName(getStringValue(row.getCell(24)));
                component.setReleaseDate(getStringValue(row.getCell(25)));
                */
                component.setRiskType(getStringValue(row.getCell(26)));
                component.setInfluenceType(getStringValue(row.getCell(27)));
                component.setReplaceSolution(getStringValue(row.getCell(28)));
                component.setComponentVersion(getStringValue(row.getCell(29)));
                component.setComponentStatus(getStringValue(row.getCell(30)));
                
                components.add(component);
            }
        }
        
        return components;
    }

    /**
     * 获取单元格字符串值
     */
    private String getStringValue(Cell cell) {
        if (cell == null) {
            return "";
        }
        switch (cell.getCellType()) {
            case STRING:
                return cell.getStringCellValue();
            case NUMERIC:
                return String.valueOf(cell.getNumericCellValue());
            case BOOLEAN:
                return String.valueOf(cell.getBooleanCellValue());
            default:
                return "";
        }
    }

    /**
     * 获取单元格整数值
     */
    private int getIntValue(Cell cell) {
        if (cell == null) {
            return 0;
        }
        switch (cell.getCellType()) {
            case NUMERIC:
                return (int) cell.getNumericCellValue();
            case STRING:
                try {
                    return Integer.parseInt(cell.getStringCellValue());
                } catch (NumberFormatException e) {
                    return 0;
                }
            default:
                return 0;
        }
    }

    /**
     * 读取组件过滤名称列表
     */
    public List<String> readComponentFilterNameList(String componentName) throws IOException {
        List<String> filterNames = new ArrayList<>();
        filterNames.add(componentName); // 默认添加组件名称本身
        
        File configFile = new File(COMPONENT_FILTERS_PATH);
        if (!configFile.exists()) {
            logger.error("配置文件不存在: {}", COMPONENT_FILTERS_PATH);
            throw new IOException("配置文件不存在: " + COMPONENT_FILTERS_PATH);
        }

        try (InputStream is = new FileInputStream(configFile);
             Workbook workbook = new XSSFWorkbook(is)) {
            
            Sheet sheet = workbook.getSheetAt(0);
            // 跳过标题行
            Iterator<Row> rowIterator = sheet.iterator();
            if (rowIterator.hasNext()) {
                rowIterator.next(); // 跳过标题行
            }
            
            while (rowIterator.hasNext()) {
                Row row = rowIterator.next();
                String currentComponentName = getStringValue(row.getCell(1)); // component_name列
                String filterName = getStringValue(row.getCell(2)); // component_filter_name列
                
                if (currentComponentName.equals(componentName) && !filterName.isEmpty()) {
                    filterNames.add(filterName);
                }
            }
        }
        
        return filterNames;
    }
}
