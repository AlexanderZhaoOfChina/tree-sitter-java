package com.asiainfo.verify;

import java.util.regex.*;

public class ExtractCharacters {
    public static void main(String[] args) {
        // 定义包含版本和操作符的字符串
        String input = "V5 Release 1.20.1";
        //String input = "Redis 2.8.x < 2.8.24;2.8.x < 2.8.24";
        //String input = "Redis Redis 5.*;<5.0 RC2";
        //String input = "Redis Redis 5.*;<5.0 RC2";
        //String input = "< 3.0.2";
        Pattern pattern = Pattern.compile("[0-9.x<>*\\s]+");
        // 使用正则表达式提取所需字符
        //Pattern pattern = Pattern.compile("[0-9.x<>*]+");
        //Pattern pattern = Pattern.compile("[0-9.x<>*\\s]+");

        //Pattern pattern = Pattern.compile("[0-9.x<>*\\s;]+");
        //Pattern pattern = Pattern.compile("[0-9.x<>*\\s]+");
        //Pattern pattern = Pattern.compile("\\b(\\d+(?:\\.\\d+)?[<>x\\s]*)\\b");

        Matcher matcher = pattern.matcher(input);

        while (matcher.find()) {
            String extractedCharacters = matcher.group();

            System.out.println("从字符串1中提取的字符为: " + extractedCharacters);
        }
    }
}
