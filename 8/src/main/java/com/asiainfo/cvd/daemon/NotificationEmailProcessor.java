package com.asiainfo.cvd.daemon;

import com.asiainfo.cvd.model.*;
import com.asiainfo.utils.MailParam;
import com.asiainfo.utils.MailUtil;
import org.jetbrains.annotations.NotNull;
import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.support.PropertiesLoaderUtils;

import javax.mail.MessagingException;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

/**
 * 漏洞通知邮件处理器
 * 负责处理和发送技术栈组件安全漏洞通知邮件
 * 支持HTML格式的邮件内容，包含漏洞概览和详细信息
 */
public class NotificationEmailProcessor {

    private static final Logger logger = LogManager.getLogger(NotificationEmailProcessor.class);

    /**
     * 处理并发送漏洞通知邮件
     * 根据提供的漏洞简报和漏洞警告列表，生成格式化的HTML邮件内容并发送
     *
     * @param vulnerabilityAlertBrief 漏洞简报信息
     * @param vulnerabilityAlertList 漏洞警告列表
     * @throws MessagingException 当邮件发送失败时抛出
     * @throws UnsupportedEncodingException 当编码不支持时抛出
     */
    public static void process(VulnerabilityAlertBrief vulnerabilityAlertBrief, List<VulnerabilityAlert> vulnerabilityAlertList) throws MessagingException, UnsupportedEncodingException {

        MailParam mailParam = new MailParam();

        // 设置收件人列表（专家邮箱）
        mailParam.setTos(EmailListBuilder.getExpertEmails());
        logger.info("Expert Email List: {}", mailParam.getTos());


        // 设置抄送人列表
        mailParam.setCcs(EmailListBuilder.getCcEmails());
        logger.info("Cc Email List: {}", mailParam.getCcs());

        // 设置邮件标题，格式：技术栈技术组件安全漏洞通报（日期范围）
        mailParam.setTitle("技术栈技术组件安全漏洞通报" + "（" + vulnerabilityAlertList.get(0).getSourceFileNameWithoutSuffix().replace("-","/").replace("_"," - ") + "）");

        // 创建邮件内容模板连接器
        AlertContentTemplateConnection alertContentTemplateConnection = new AlertContentTemplateConnection();
        // 设置收件人标题
        alertContentTemplateConnection.setRecipient("<h2 style=\"margin-top: 0px; text-align: center; margin-bottom: 0px; font-family: 'Arial', sans-serif;\">技术栈技术组件</h2><h2 style=\"margin-top: 0px; text-align: center; margin-bottom: 0px; font-family: 'Arial', sans-serif;\">安全漏洞通报</h2>");
        // 设置简报内容
        alertContentTemplateConnection.setBrief(vulnerabilityAlertBrief.getData());

        // 构建漏洞概览部分
        StringBuilder overview = new StringBuilder();
        overview.append("<h3 style=\"margin-left: 15px;\">• 漏洞概览：</h3>");
        overview.append("<table style=\"margin-left: 30px; color: brown; margin-bottom: 0px;\">");

        // 遍历所有漏洞警告，生成概览内容
        for (VulnerabilityAlert vulnerabilityAlert : vulnerabilityAlertList) {

            String componentDescription = "<span style=\"color: black;\">：" + vulnerabilityAlert.getDescription() + "</span>";

            // 根据漏洞等级（高/其他）使用不同的样式
            if ("高".equals(vulnerabilityAlert.getSeverity())){
                overview.append("<tr style=\"margin-bottom: 12px; margin-top: 0px;\"><td style=\"vertical-align: top; font-weight: bold;\">");
                overview.append(vulnerabilityAlert.getTitle().split("\\.")[0].trim());
                overview.append(". </td><td style=\"font-weight: bold;\">");
                overview.append(vulnerabilityAlert.getTitle().split("\\.", 2)[1].trim());
                overview.append("<span style=\"color: red;\">（漏洞等级：");
                overview.append(vulnerabilityAlert.getSeverity());
                overview.append("）");
                overview.append("<span style=\"color: black; font-weight: lighter;\">");
                overview.append(componentDescription);
                overview.append("</span></span></td></tr>");
            }else {
                overview.append("<tr style=\"margin-bottom: 12px; margin-top: 0px;\"><td style=\"vertical-align: top; font-weight: bold;\">");
                overview.append(vulnerabilityAlert.getTitle().split("\\.")[0].trim());
                overview.append(". </td><td style=\"font-weight: bold;\">");
                overview.append(vulnerabilityAlert.getTitle().split("\\.", 2)[1].trim());
                overview.append("<span>（漏洞等级：");
                overview.append(vulnerabilityAlert.getSeverity());
                overview.append("）");
                overview.append("<span style=\"color: black; font-weight: lighter;\">");
                overview.append(componentDescription);
                overview.append("</span></span></td>");
            }

            // 获取漏洞详细信息的内容部分
            List<AlertContentSection> alertContentSectionList = getAlertContentSectionList(vulnerabilityAlert);

            // 创建并添加漏洞内容模板
            AlertContentTemplate alertContentTemplate = new AlertContentTemplate();
            alertContentTemplate.setTitle(vulnerabilityAlert.getTitle());
            alertContentTemplate.setAlertContentSectionList(alertContentSectionList);

            alertContentTemplateConnection.addAlertContentTemplate(alertContentTemplate);
        }

        overview.append("</table>");

        // 设置概览内容
        alertContentTemplateConnection.setOverview(overview.toString());

        // 设置邮件内容并发送
        mailParam.setContent(alertContentTemplateConnection.getData());

        // 检查是否启用邮件发送
        if (isEmailSendEnabled()) {
            // 发送邮件
            MailUtil.sendText(mailParam);
            logger.info("Email Sent Successfully");
        } else {
            logger.info("Email sending function has been disabled, and the email has not been sent.");
            logger.debug("Email Content：{}", mailParam.getContent());
        }
    }

    /**
     * 检查是否启用邮件发送
     * 从配置文件中读取email.send.enabled属性，默认为true
     *
     * @return 如果启用邮件发送返回true，否则返回false
     */
    private static boolean isEmailSendEnabled() {
        try {
            Properties properties = PropertiesLoaderUtils.loadProperties(new ClassPathResource("application.properties"));
            return Boolean.parseBoolean(properties.getProperty("email.send.enabled", "true"));
        } catch (IOException e) {
            logger.error("读取邮件发送配置失败，默认启用邮件发送", e);
            return true;
        }
    }

    /**
     * 构建漏洞警告的内容部分列表
     * 包含组件信息、CNVD编号、漏洞描述、严重程度、受影响版本和修复建议等信息
     *
     * @param vulnerabilityAlert 漏洞警告对象
     * @return 警告内容部分列表
     */
    @NotNull
    private static List<AlertContentSection> getAlertContentSectionList(VulnerabilityAlert vulnerabilityAlert) {

        List<AlertContentSection> alertContentSectionList = new ArrayList<>();

        // 添加组件信息
        AlertContentSection alertContentSection0 = new AlertContentSection();
        alertContentSection0.setSectionName(VulnerabilityDefinitions.COMPONENT);
        alertContentSection0.setSectionDescription(vulnerabilityAlert.getComponent());
        alertContentSectionList.add(alertContentSection0);

        // 添加CNVD编号（如果有CVE编号则一并添加）
        AlertContentSection alertContentSection1 = new AlertContentSection();
        alertContentSection1.setSectionName(VulnerabilityDefinitions.CNVD_NUMBER);
        alertContentSection1.setSectionDescription(vulnerabilityAlert.getCnvdNumber() + (vulnerabilityAlert.getCveNumber() != null && !vulnerabilityAlert.getCveNumber().isEmpty() ? "（" + vulnerabilityAlert.getCveNumber() + "）" : ""));
        alertContentSectionList.add(alertContentSection1);

        // 添加漏洞描述
        AlertContentSection alertContentSection2 = new AlertContentSection();
        alertContentSection2.setSectionName(VulnerabilityDefinitions.VULNERABILITY_DESC);
        alertContentSection2.setSectionDescription(vulnerabilityAlert.getDescription());
        alertContentSectionList.add(alertContentSection2);

        // 添加漏洞严重程度
        AlertContentSection alertContentSection3 = new AlertContentSection();
        alertContentSection3.setSectionName(VulnerabilityDefinitions.VULNERABILITY_SEVERITY);
        alertContentSection3.setSectionDescription(vulnerabilityAlert.getSeverity());
        alertContentSectionList.add(alertContentSection3);

        // 添加受影响版本
        AlertContentSection alertContentSection4 = new AlertContentSection();
        alertContentSection4.setSectionName(VulnerabilityDefinitions.AFFECTED_VERSION);
        alertContentSection4.setSectionDescription(vulnerabilityAlert.getAffectedVersion());
        alertContentSectionList.add(alertContentSection4);

        // 添加修复建议
        AlertContentSection alertContentSection5 = new AlertContentSection();
        alertContentSection5.setSectionName(VulnerabilityDefinitions.REMEDIATION_ADVICE);
        alertContentSection5.setSectionDescription(vulnerabilityAlert.getRemediationAdvice());
        alertContentSectionList.add(alertContentSection5);

        return alertContentSectionList;
    }
}
