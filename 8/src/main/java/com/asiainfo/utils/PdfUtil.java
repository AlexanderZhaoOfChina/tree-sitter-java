package com.asiainfo.utils;

import lombok.extern.slf4j.Slf4j;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.rendering.PDFRenderer;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * @author: guosp5
 * @date: 2022/9/20 15:50
 * @description: pdf文件处理相关工具类
 */
@Slf4j
public class PdfUtil {

    //最大图片加载大小：13MB
    public static Integer MAX_PIC_SIZE_BYTES = 1024 * 1024 * 13;

    /**
     * 转换全部的pdf便成图片存到相应位置
     *
     * @param fileAddress 文件地址
     * @param filename    PDF文件名
     * @param type        图片类型
     */
    public static void pdf2png(String fileAddress, String filename, String type) {
        // 将pdf装图片 并且自定义图片得格式大小
        File file = new File(fileAddress + "/" + filename + ".pdf");
        try {
            PDDocument doc = PDDocument.load(file);
            PDFRenderer renderer = new PDFRenderer(doc);
            int pageCount = doc.getNumberOfPages();
            for (int i = 0; i < pageCount; i++) {
                BufferedImage image = renderer.renderImageWithDPI(i, 100); // Windows native DPI
                //BufferedImage srcImage = resize(image, 240, 240);//产生缩略图
                ImageIO.write(image, type, new File(fileAddress + filename + "_" + (i + 1) + "." + "png"));
            }
        } catch (IOException e) {
            log.error("pdf文件图片转换图片失败！", e);
        }
    }

    /**
     * 转换全部的pdf
     *
     * @param pdfBytes PDF二进制文件
     */
    public static List<ByteArrayOutputStream> pdf2png(byte[] pdfBytes, String type) {
        // 将pdf装图片 并且自定义图片得格式大小
        try {
            PDDocument doc = PDDocument.load(pdfBytes);
            PDFRenderer renderer = new PDFRenderer(doc);
            int pageCount = doc.getNumberOfPages();
            List<ByteArrayOutputStream> imageList = new ArrayList<>();
            int currentSize = 0;
            for (int i = 0; i < pageCount; i++) {
                BufferedImage image = renderer.renderImageWithDPI(i, 100); // Windows native DPI
                //BufferedImage srcImage = resize(image, 240, 240);//产生缩略图
                ByteArrayOutputStream outStream = new ByteArrayOutputStream();
                ImageIO.write(image, type, outStream);
                currentSize += outStream.size();
                // 判断当前加载的图片数量是否大于额定总大小，如果大于则跳出循环
                if (currentSize < MAX_PIC_SIZE_BYTES) {
                    imageList.add(outStream);
                } else {
                    break;
                }
            }
            return imageList;
        } catch (IOException e) {
            log.error("pdf文件图片转换图片失败！", e);
            return null;
        }
    }
}
