package com.asiainfo.verify;

public class RemoveSpecialCharacters {
    public static String removeCharacters(String input) {
        // 使用正则表达式替换 "-" 和英文字符
        return input.replaceAll("[.-]|[a-zA-Z]+", "");
    }

    public static void main(String[] args) {
        String input = "RELEASE.2023-05-18T00-05-36Z";
        String result = removeCharacters(input);

        System.out.println("原始字符串: " + input);
        System.out.println("去除字符后的字符串: " + result);
    }
}
