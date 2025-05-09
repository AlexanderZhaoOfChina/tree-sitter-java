package com.asiainfo.utils;

import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.file.Paths;

/**
 * Excel模板生成工具
 */
public class ExcelTemplateGenerator {

    /**
     * 生成组件配置模板
     */
    public static void generateComponentsTemplate(String outputPath) throws IOException {
        try (Workbook workbook = new XSSFWorkbook()) {
            Sheet sheet = workbook.createSheet("Components");
            
            // 创建标题行
            Row headerRow = sheet.createRow(0);
            String[] headers = {
                "id", "component_name", "component_describe", "use_count", "use_count_exclude_bss",
                "belong_directory_name", "belong_directory_id", "official_link", "source_code_link",
                "last_version", "last_modified_date", "license_type", "vendor", "vendor_country",
                "cve_product_name", "belong_domain", "is_component_lib", "is_independ", "is_for_devolop",
                "replace_cost", "is_increase_market", "is_decrease_market", "belong_type",
                "is_open_source", "company_name", "release_date", "risk_type", "influence_type",
                "replace_solution", "component_version", "component_status"
            };
            
            // 设置标题样式
            CellStyle headerStyle = createHeaderStyle(workbook);
            
            // 写入标题
            for (int i = 0; i < headers.length; i++) {
                Cell cell = headerRow.createCell(i);
                cell.setCellValue(headers[i]);
                cell.setCellStyle(headerStyle);
                sheet.autoSizeColumn(i);
            }
            
            // 保存文件
            try (FileOutputStream fileOut = new FileOutputStream(outputPath)) {
                workbook.write(fileOut);
            }
        }
    }

    /**
     * 生成组件过滤规则模板
     */
    public static void generateComponentFiltersTemplate(String outputPath) throws IOException {
        try (Workbook workbook = new XSSFWorkbook()) {
            Sheet sheet = workbook.createSheet("Component Filters");
            
            // 创建标题行
            Row headerRow = sheet.createRow(0);
            String[] headers = {
                "id", "component_name", "component_filter_name"
            };
            
            // 设置标题样式
            CellStyle headerStyle = createHeaderStyle(workbook);
            
            // 写入标题
            for (int i = 0; i < headers.length; i++) {
                Cell cell = headerRow.createCell(i);
                cell.setCellValue(headers[i]);
                cell.setCellStyle(headerStyle);
                sheet.autoSizeColumn(i);
            }
            
            // 保存文件
            try (FileOutputStream fileOut = new FileOutputStream(outputPath)) {
                workbook.write(fileOut);
            }
        }
    }

    /**
     * 创建标题行样式
     */
    private static CellStyle createHeaderStyle(Workbook workbook) {
        CellStyle style = workbook.createCellStyle();
        
        // 设置背景色为灰色
        style.setFillForegroundColor(IndexedColors.GREY_25_PERCENT.getIndex());
        style.setFillPattern(FillPatternType.SOLID_FOREGROUND);
        
        // 设置边框
        style.setBorderTop(BorderStyle.THIN);
        style.setBorderBottom(BorderStyle.THIN);
        style.setBorderLeft(BorderStyle.THIN);
        style.setBorderRight(BorderStyle.THIN);
        
        // 设置字体为粗体
        Font font = workbook.createFont();
        font.setBold(true);
        style.setFont(font);
        
        // 设置居中对齐
        style.setAlignment(HorizontalAlignment.CENTER);
        
        return style;
    }

    public static void main(String[] args) {
        try {
            // 确保目录存在
            File configDir = new File("src/main/resources/config");
            if (!configDir.exists()) {
                configDir.mkdirs();
            }

            // 生成模板文件
            generateComponentsTemplate(Paths.get("src/main/resources/config/Components.xlsx").toString());
            generateComponentFiltersTemplate(Paths.get("src/main/resources/config/ComponentFilters.xlsx").toString());
            
            System.out.println("Excel templates generated successfully!");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
} 