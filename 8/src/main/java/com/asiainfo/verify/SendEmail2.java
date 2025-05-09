package com.asiainfo.verify;

import com.asiainfo.cvd.model.AlertContentSection;
import com.asiainfo.cvd.model.AlertContentTemplate;
import com.asiainfo.cvd.model.AlertContentTemplateConnection;
import com.asiainfo.utils.MailParam;
import com.asiainfo.utils.MailUtil;
import org.jetbrains.annotations.NotNull;

import javax.mail.MessagingException;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;

public class SendEmail2 {

    public static void main(String[] args) throws MessagingException, UnsupportedEncodingException {

        MailParam mailParam = new MailParam();

        ArrayList<String> emailTo = new ArrayList<>();

        emailTo.add("zhaolx5@asiainfo.com");

        mailParam.setTos(emailTo);

        mailParam.setTitle("test email");

        AlertContentTemplateConnection alertContentTemplateConnection = new AlertContentTemplateConnection();

        alertContentTemplateConnection.setRecipient("技术栈技术组件安全漏洞通报");

        List<AlertContentSection> alertContentSectionList = getAlertContentSectionList();

        AlertContentTemplate alertContentTemplate1 = new AlertContentTemplate();
        alertContentTemplate1.setTitle("【漏洞预警】Apache Struts 2 拒绝服务漏洞");
        alertContentTemplate1.setSubTitle("2023-10-01");

        alertContentTemplate1.setAlertContentSectionList(alertContentSectionList);

        alertContentTemplateConnection.addAlertContentTemplate(alertContentTemplate1);

        AlertContentTemplate alertContentTemplate2 = new AlertContentTemplate();
        alertContentTemplate2.setTitle("【漏洞预警】MySQL 2 拒绝服务漏洞");
        alertContentTemplate2.setSubTitle("2022-10-10");

        alertContentTemplate2.setAlertContentSectionList(alertContentSectionList);

        alertContentTemplateConnection.addAlertContentTemplate(alertContentTemplate2);

        System.out.println(alertContentTemplateConnection.getData());
        mailParam.setContent(alertContentTemplateConnection.getData());

        MailUtil.sendText(mailParam);

    }

    @NotNull
    private static List<AlertContentSection> getAlertContentSectionList() {
        List<AlertContentSection> alertContentSectionList = new ArrayList<>();

        AlertContentSection alertContentSection1 = new AlertContentSection();
        alertContentSection1.setSectionName("一、漏洞描述");
        alertContentSection1.setSectionDescription("近日，安全厂商监测到Apache Struts 2修复了一个拒绝服务漏洞 (CVE-2023-41835) 。该漏洞允许远程攻击者执行拒绝服务(DoS)攻击。该漏洞的存在是由于应用程序无法正确处理多部分请求。远程攻击者可以发送特制的多部分请求，其中的字段超过 maxStringLength 限制，并强制应用程序过度使用磁盘，即使请求被拒绝也是如此。");
        alertContentSectionList.add(alertContentSection1);

        AlertContentSection alertContentSection2 = new AlertContentSection();
        alertContentSection2.setSectionName("二、修复建议");
        alertContentSection2.setSectionDescription("目前官网已发布安全更新，受影响用户可以升级到 Struts2.5.32 或6.1.2.2 或Struts 6.3.0.1 或更高版本。");
        alertContentSectionList.add(alertContentSection2);
        return alertContentSectionList;
    }

}
