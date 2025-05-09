package com.asiainfo.verify;

import com.asiainfo.utils.MailParam;
import com.asiainfo.utils.MailUtil;

import javax.mail.MessagingException;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;

public class SendEmail {

    public static void main(String[] args) throws MessagingException, UnsupportedEncodingException {

        MailParam mailParam = new MailParam();

        ArrayList<String> emailTo = new ArrayList<>();

        emailTo.add("zhaolx5@asiainfo.com");

        mailParam.setTos(emailTo);

        mailParam.setTitle("test email");

//        String content = "<h1 style=\"text-align: center;\">【漏洞预警】Apache Struts 2 拒绝服务漏洞</h1>\n" +
//                "  <h2>一、漏洞描述</h2>\n" +
//                "  <p>近日，安全厂商监测到Apache Struts 2修复了一个拒绝服务漏洞 (CVE-2023-41835) 。该漏洞允许远程攻击者执行拒绝服务(DoS)攻击。该漏洞的存在是由于应用程序无法正确处理多部分请求。远程攻击者可以发送特制的多部分请求，其中的字段超过 maxStringLength 限制，并强制应用程序过度使用磁盘，即使请求被拒绝也是如此。</p>\n" +
//                "  <h2>二、修复建议</h2>\n" +
//                "  <p>目前官网已发布安全更新，受影响用户可以升级到 Struts2.5.32 或6.1.2.2 或Struts 6.3.0.1 或更高版本。</p>\n" +
//                "  <p>补丁链接:<a href=\"https://struts.apache.org/download.cgi#struts6301\">https://struts.apache.org/download.cgi#struts6301</a></p>";

        String content1 = "<h1 style=\"text-align: center;\">【漏洞预警】Apache Struts 2 拒绝服务漏洞</h1>\n" +
                "  <h2>一、漏洞描述</h2>\n" +
                "  <p>近日，安全厂商监测到Apache Struts 2修复了一个拒绝服务漏洞 (CVE-2023-41835) 。该漏洞允许远程攻击者执行拒绝服务(DoS)攻击。该漏洞的存在是由于应用程序无法正确处理多部分请求。远程攻击者可以发送特制的多部分请求，其中的字段超过 maxStringLength 限制，并强制应用程序过度使用磁盘，即使请求被拒绝也是如此。</p>\n" +
                "  <h2>二、修复建议</h2>\n" +
                "  <p>目前官网已发布安全更新，受影响用户可以升级到 Struts2.5.32 或6.1.2.2 或Struts 6.3.0.1 或更高版本。</p>\n";

        String content2 = "<h1 style=\"text-align: center;\"【漏洞预警】Apache Struts 9 拒绝服务漏洞</h1>\n" +
                "  <h2>一、漏洞描述</h2>\n" +
                "  <p>近日，安全厂商监测到Apache Struts 2修复了一个拒绝服务漏洞 (CVE-2023-41835) 。该漏洞允许远程攻击者执行拒绝服务(DoS)攻击。该漏洞的存在是由于应用程序无法正确处理多部分请求。远程攻击者可以发送特制的多部分请求，其中的字段超过 maxStringLength 限制，并强制应用程序过度使用磁盘，即使请求被拒绝也是如此。</p>\n" +
                "  <h2>二、修复建议</h2>\n" +
                "  <p>目前官网已发布安全更新，受影响用户可以升级到 Struts2.5.32 或6.1.2.2 或Struts 6.3.0.1 或更高版本。</p>\n";

        System.out.println(content1);
        mailParam.setContent(content1);
        MailUtil.sendText(mailParam);

        System.out.println(content2);
        mailParam.setContent(content2);
        MailUtil.sendText(mailParam);

    }


}
