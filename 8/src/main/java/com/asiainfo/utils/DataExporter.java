package com.asiainfo.utils;

import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.sql.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * 数据导出工具类
 * 将数据库表数据导出到Excel文件
 */
public class DataExporter {
    
    private static final String EXPORT_DIR = "D:\\CNVD\\exports";
    private final String dbUrl;
    private final String dbUser;
    private final String dbPassword;

    public DataExporter(String dbUrl, String dbUser, String dbPassword) {
        this.dbUrl = dbUrl;
        this.dbUser = dbUser;
        this.dbPassword = dbPassword;
    }

    /**
     * 导出所有数据到Excel
     */
    public void exportAllToExcel() throws SQLException, IOException {
        // 确保导出目录存在
        createExportDirectory();

        // 生成带时间戳的文件名
        String timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss"));
        String excelFileName = "component_data_" + timestamp + ".xlsx";
        File excelFile = new File(EXPORT_DIR, excelFileName);

        // 创建工作簿
        try (Workbook workbook = new XSSFWorkbook()) {
            Connection conn = DriverManager.getConnection(dbUrl, dbUser, dbPassword);

            // 导出组件数据
            exportComponentsToSheet(workbook, conn);
            // 导出过滤规则数据
            exportFiltersToSheet(workbook, conn);

            // 保存Excel文件
            try (FileOutputStream fileOut = new FileOutputStream(excelFile)) {
                workbook.write(fileOut);
            }

            conn.close();
            System.out.println("Data exported successfully to: " + excelFile.getAbsolutePath());
        }
    }

    /**
     * 导出组件数据到工作表
     */
    private void exportComponentsToSheet(Workbook workbook, Connection conn) throws SQLException {
        Sheet sheet = workbook.createSheet("Components");
        
        // 创建标题行样式
        CellStyle headerStyle = createHeaderStyle(workbook);

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
        for (int i = 0; i < headers.length; i++) {
            Cell cell = headerRow.createCell(i);
            cell.setCellValue(headers[i]);
            cell.setCellStyle(headerStyle);
        }

        // 查询数据
        String sql = "SELECT id, component_name, component_describe, use_count, use_count_exclude_bss, " +
                    "belong_directory_name, belong_directory_id, official_link, source_code_link, " +
                    "last_version, last_modified_date, license_type, vendor, vendor_country, " +
                    "cve_product_name, belong_domain, is_component_lib, is_independ, is_for_devolop, " +
                    "replace_cost, is_increase_market, is_decrease_market, belong_type, " +
                    "is_open_source, company_name, release_date, risk_type, influence_type, " +
                    "replace_solution, component_version, component_status FROM components";
        try (PreparedStatement stmt = conn.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {

            int rowNum = 1;
            while (rs.next()) {
                Row row = sheet.createRow(rowNum++);
                row.createCell(0).setCellValue(rs.getInt("id"));
                row.createCell(1).setCellValue(rs.getString("component_name"));
                row.createCell(2).setCellValue(rs.getString("component_describe"));
                row.createCell(3).setCellValue(getStringValue(rs, "use_count"));
                row.createCell(4).setCellValue(getStringValue(rs, "use_count_exclude_bss"));
                row.createCell(5).setCellValue(rs.getString("belong_directory_name"));
                row.createCell(6).setCellValue(getStringValue(rs, "belong_directory_id"));
                row.createCell(7).setCellValue(rs.getString("official_link"));
                row.createCell(8).setCellValue(rs.getString("source_code_link"));
                row.createCell(9).setCellValue(rs.getString("last_version"));
                row.createCell(10).setCellValue(getStringValue(rs, "last_modified_date"));
                row.createCell(11).setCellValue(rs.getString("license_type"));
                row.createCell(12).setCellValue(rs.getString("vendor"));
                row.createCell(13).setCellValue(rs.getString("vendor_country"));
                row.createCell(14).setCellValue(rs.getString("cve_product_name"));
                row.createCell(15).setCellValue(rs.getString("belong_domain"));
                row.createCell(16).setCellValue(rs.getString("is_component_lib"));
                row.createCell(17).setCellValue(rs.getString("is_independ"));
                row.createCell(18).setCellValue(rs.getString("is_for_devolop"));
                row.createCell(19).setCellValue(rs.getString("replace_cost"));
                row.createCell(20).setCellValue(rs.getString("is_increase_market"));
                row.createCell(21).setCellValue(rs.getString("is_decrease_market"));
                row.createCell(22).setCellValue(rs.getString("belong_type"));
                row.createCell(23).setCellValue(rs.getString("is_open_source"));
                row.createCell(24).setCellValue(rs.getString("company_name"));
                row.createCell(25).setCellValue(getStringValue(rs, "release_date"));
                row.createCell(26).setCellValue(rs.getString("risk_type"));
                row.createCell(27).setCellValue(rs.getString("influence_type"));
                row.createCell(28).setCellValue(rs.getString("replace_solution"));
                row.createCell(29).setCellValue(rs.getString("component_version"));
                row.createCell(30).setCellValue(rs.getString("component_status"));
            }

            // 自动调整列宽
            for (int i = 0; i < headers.length; i++) {
                sheet.autoSizeColumn(i);
            }
        }
    }

    /**
     * 导出过滤规则数据到工作表
     */
    private void exportFiltersToSheet(Workbook workbook, Connection conn) throws SQLException {
        Sheet sheet = workbook.createSheet("Component Filters");
        
        // 创建标题行样式
        CellStyle headerStyle = createHeaderStyle(workbook);

        // 创建标题行
        Row headerRow = sheet.createRow(0);
        String[] headers = {
            "id", "component_name", "component_filter_name"
        };
        for (int i = 0; i < headers.length; i++) {
            Cell cell = headerRow.createCell(i);
            cell.setCellValue(headers[i]);
            cell.setCellStyle(headerStyle);
        }

        // 查询数据
        String sql = "SELECT id, component_name, component_filter_name FROM component_filter_name";
        try (PreparedStatement stmt = conn.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {

            int rowNum = 1;
            while (rs.next()) {
                Row row = sheet.createRow(rowNum++);
                row.createCell(0).setCellValue(rs.getInt("id"));
                row.createCell(1).setCellValue(rs.getString("component_name"));
                row.createCell(2).setCellValue(rs.getString("component_filter_name"));
            }

            // 自动调整列宽
            for (int i = 0; i < headers.length; i++) {
                sheet.autoSizeColumn(i);
            }
        }
    }

    /**
     * 获取ResultSet中字段的字符串值，处理null值
     */
    private String getStringValue(ResultSet rs, String columnName) throws SQLException {
        Object value = rs.getObject(columnName);
        return value != null ? value.toString() : "";
    }

    /**
     * 创建标题行样式
     */
    private CellStyle createHeaderStyle(Workbook workbook) {
        CellStyle style = workbook.createCellStyle();
        
        // 设置背景色
        style.setFillForegroundColor(IndexedColors.GREY_25_PERCENT.getIndex());
        style.setFillPattern(FillPatternType.SOLID_FOREGROUND);
        
        // 设置边框
        style.setBorderTop(BorderStyle.THIN);
        style.setBorderBottom(BorderStyle.THIN);
        style.setBorderLeft(BorderStyle.THIN);
        style.setBorderRight(BorderStyle.THIN);
        
        // 设置字体
        Font font = workbook.createFont();
        font.setBold(true);
        style.setFont(font);
        
        // 设置居中对齐
        style.setAlignment(HorizontalAlignment.CENTER);
        
        return style;
    }

    /**
     * 确保导出目录存在
     */
    private void createExportDirectory() {
        File exportDir = new File(EXPORT_DIR);
        if (!exportDir.exists()) {
            exportDir.mkdirs();
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
            DataExporter exporter = new DataExporter(dbUrl, dbUser, dbPassword);
            exporter.exportAllToExcel();
        } catch (Exception e) {
            System.err.println("Error exporting data to Excel: " + e.getMessage());
            e.printStackTrace();
        }
    }
} 
