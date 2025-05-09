package com.asiainfo.verify;

import java.util.regex.*;

public class ExtractContent {
    public static void main(String[] args) {
        // 定义包含版本和操作符的字符串
        String input1 = "Redis Redis 5.*;<5.0 RC2";
        String input2 = "Redis 2.8.x < 2.8.24";

        // 使用正则表达式提取所需字符
        Pattern pattern = Pattern.compile("[0-9.x<>\\s]+");
        Matcher matcher1 = pattern.matcher(input1);
        Matcher matcher2 = pattern.matcher(input2);

        while (matcher1.find()) {
            String extractedCharacters = matcher1.group();

            System.out.println("从字符串1中提取的字符为: " + extractedCharacters);
        }

        while (matcher2.find()) {
            String extractedCharacters = matcher2.group();

            System.out.println("从字符串2中提取的字符为: " + extractedCharacters);
        }
    }
}
