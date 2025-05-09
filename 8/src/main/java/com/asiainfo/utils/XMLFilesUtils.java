package com.asiainfo.utils;

import org.w3c.dom.Element;

import java.io.File;
import java.io.FilenameFilter;
import java.util.List;

public class XMLFilesUtils {

    public static void collectXMLFiles(File directory, List<File> xmlFiles) {
        File[] files = directory.listFiles(new FilenameFilter() {
            @Override
            public boolean accept(File dir, String name) {
                return name.toLowerCase().endsWith(".xml");
            }
        });

        if (files != null) {
            for (File file : files) {
                if (file.isFile()) {
                    xmlFiles.add(file);
                } else if (file.isDirectory()) {
                    collectXMLFiles(file, xmlFiles); // 递归遍历子目录
                }
            }
        }
    }

    public static String getStringFromXmlElement(Element vulnerability, String tagName) {
        String tagValue = "";
        Element numberElement = (Element) vulnerability.getElementsByTagName(tagName).item(0);
        if (numberElement != null) {
            tagValue = numberElement.getTextContent();
        }
        return tagValue;
    }

}
