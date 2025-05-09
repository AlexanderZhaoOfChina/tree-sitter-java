package com.asiainfo.utils;

import lombok.extern.slf4j.Slf4j;
import org.springframework.util.StringUtils;

import javax.activation.DataHandler;
import javax.mail.*;
import javax.mail.internet.*;
import javax.mail.util.ByteArrayDataSource;
import java.io.ByteArrayOutputStream;
import java.io.UnsupportedEncodingException;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * 邮件工具类，基于javax.mail封装
 *
 * @author looly
 * @since 3.1.2
 */
@Slf4j
public class MailUtil {

    public static final Pattern MACRO_PATTERN = Pattern.compile("\\$\\{\\w+\\}");

    /**
     * 使用配置文件中设置的账户发送文本邮件，发送给单个或多个收件人<br>
     * 多个收件人可以使用逗号“,”分隔，也可以通过分号“;”分隔
     *
     * @param mailParam 邮件信息
     * @return message-id
     * @since 3.2.0
     */
    public static String sendPdfToPicture(MailParam mailParam)
            throws MessagingException, UnsupportedEncodingException {
        if (mailParam.getAttachment() != null && mailParam.getAttachment().length > 0){
            return send(mailParam, true);
        }
        throw new RuntimeException("附件为空，不能转换");
    }

    /**
     * 使用配置文件中设置的账户发送文本邮件，发送给单个或多个收件人<br>
     * 多个收件人可以使用逗号“,”分隔，也可以通过分号“;”分隔
     *
     * @param mailParam 邮件信息
     * @return message-id
     * @since 3.2.0
     */
    public static String sendText(MailParam mailParam) throws MessagingException, UnsupportedEncodingException {
        return send(mailParam, false);
    }

    private static String send(MailParam mailParam, boolean isPdfToPicture)
            throws UnsupportedEncodingException, MessagingException {

        //这里需要增加配置信息判断哪个系统 ???
        MailConfig mailConfig = getEmailBean(EmailSource.TSMM.getName());
        MimeMessage message = mailConfig.getMimeMessage();
        Transport ts = mailConfig.getTransport();

        //指明邮件的发件人
        //这里的发件人信息后期需要改为从配置文件获取 ???
        String nick = MimeUtility.encodeText(EmailSource.TSMM.getSource());
        //message.setFrom(new InternetAddress(nick + " <" + "5G@asiainfo.com" + ">"));
        message.setFrom(new InternetAddress(nick + " <" + "AITech-PRD-techstack@asiainfo.com" + ">"));

        //配置邮件的接受人以及抄送人，多个接受人或抄送人用英文逗号隔开
        if (mailParam.getTos() != null && !mailParam.getTos().isEmpty()) {
            List<String> toList = new ArrayList<>();
            for (String address : mailParam.getTos()) {
                if (address.contains(";")) {
                    toList.add(address.replaceAll(";", ","));
                    continue;
                }
                toList.add(address);
            }
            message.setRecipients(
                    Message.RecipientType.TO,
                    InternetAddress.parse(StringUtils.collectionToDelimitedString(toList, ",")));
        }
        if (mailParam.getCcs() != null && !mailParam.getCcs().isEmpty()) {
            List<String> ccList = new ArrayList<>();
            for (String address : mailParam.getCcs()) {
                if (address.contains(";")) {
                    ccList.add(address.replaceAll(";", ","));
                    continue;
                }
                ccList.add(address);
            }
            message.setRecipients(
                    Message.RecipientType.CC,
                    InternetAddress.parse(StringUtils.collectionToDelimitedString(ccList, ",")));
        }

        //配置邮件标题
        message.setSubject(mailParam.getTitle());
        HashMap<String, Object> formDataJsonObject = new HashMap<>();
        //获取邮件正文
        String emailContent = mailParam.getContent();
        //邮件附件名称错误问题解决配置，此配置需要放在需要使用的MimeMultipart和MimeBodyPart之前才能生效
        System.getProperties().setProperty("mail.mime.splitlongparameters", "false");
        MimeMultipart mp = new MimeMultipart("related");
        MimeBodyPart text = new MimeBodyPart();

        if (isPdfToPicture) {
            //为邮件添加附件节点
            MimeBodyPart attach = getAttach(mailParam);

            //为邮件正文添加图片
            //将pdf二进制数组转换为图片输出流数组
            List<ByteArrayOutputStream> imageOutputStreamList = PdfUtil.pdf2png(mailParam.getAttachment(), "png");
            //创建图片节点数组
            List<MimeBodyPart> imageList = new ArrayList<>();
            //邮件正文中需要增加的图片链接StringBuilder
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < Objects.requireNonNull(imageOutputStreamList).size(); i++) {
                //创建图片节点
                MimeBodyPart image = new MimeBodyPart();
                ByteArrayDataSource imageDataSource =
                        new ByteArrayDataSource(imageOutputStreamList.get(i).toByteArray(), "image/png");
                //读取图片数据源
                DataHandler imageDh = new DataHandler(imageDataSource);
                //将图片添加到节点
                image.setDataHandler(imageDh);
                // 为"节点"设置一个唯一编号（在文本"节点"将引用该ID）
                image.setContentID("mailPic_" + i);
                sb.append("<br/><img src='cid:mailPic_").append(i).append("'/>");
                imageList.add(image);
            }

            //图片链接标签添加到formData当中
            formDataJsonObject.put("mailPic", sb + "<br/>");
            emailContent = MailUtil.replace(emailContent, formDataJsonObject);
            // 将$符号反编码回来，这里主要是用于如果邮件正文中包含$符号并且将其进行了转译的情况，如果没有则忽略
            emailContent = emailContent.replaceAll("RDS_CHAR_DOLLAR", "\\$");
            //这里添加图片的方式是将整个图片包含到邮件内容中, 实际上也可以以 http 链接的形式添加网络图片
            text.setContent(emailContent, "text/html;charset=UTF-8");
            //（文本+图片）设置文本和图片"节点"的关系（将文本和图片"节点"合成一个混合"节点"）
            MimeMultipart mmTextImage = new MimeMultipart();
            mmTextImage.addBodyPart(text);
            for (MimeBodyPart image : imageList) {
                mmTextImage.addBodyPart(image);
            }
            mmTextImage.setSubType("related"); // 关联关系
            // 将 文本+图片 的混合"节点"封装成一个普通"节点"
            // 最终添加到邮件的 Content 是由多个 BodyPart 组成的 Multipart, 所以我们需要的是 BodyPart,
            // 上面的 mailTestPic 并非 BodyPart, 所有要把 mmTextImage 封装成一个 BodyPart
            MimeBodyPart textImage = new MimeBodyPart();
            textImage.setContent(mmTextImage);
            // 添加带图片的正文
            mp.addBodyPart(textImage);
            mp.addBodyPart(attach);
        } else {
            if (mailParam.getAttachment() != null && mailParam.getAttachment().length > 0){
                //为邮件添加附件节点
                MimeBodyPart attach = getAttach(mailParam);
                mp.addBodyPart(attach);
            }
            emailContent = MailUtil.replace(emailContent, formDataJsonObject);
            emailContent = emailContent.replaceAll("RDS_CHAR_DOLLAR", "\\$");// 将$符号反编码回来
            text.setContent(emailContent, "text/html;charset=UTF-8");
            mp.addBodyPart(text);

        }

        mp.setSubType("mixed");
        message.setContent(mp);
        message.saveChanges();
        //5、发送邮件
        try {
            ts.sendMessage(message, message.getAllRecipients());
        } catch (SendFailedException e) {
            Address[] invalidAddresses = e.getInvalidAddresses(); //获取到不合法的地址
            // 后期决定不合法的地址该如何处理 ???
            log.error("邮件发送问题------不合法的地址：" + Arrays.toString(invalidAddresses));
            Address[] validUnsentAddresses = e.getValidUnsentAddresses(); //获取到合法但未发出的地址
            ts.sendMessage(message, validUnsentAddresses);
        }
        ts.close();
        //邮件记录
//        SendMailParam sendMailParam = new SendMailParam();
//        Address[] addresses = message.getAllRecipients();
//        StringBuilder sAddresses = new StringBuilder();
//        for (Address address : addresses) {
//            sAddresses.append(address.toString());
//        }
//        sendMailParam.setTo(sAddresses.toString());
//        sendMailParam.setTitle(message.getSubject());
//        sendMailParam.setContent(emailContent);
//        MessageHelperService messageHelperService = SpringUtil.getBean(MessageHelperService.class);
//        messageHelperService.saveEmailLog(sendMailParam);
        log.info("Email Sent Successfully");
        return "发送成功！";
    }

    private static MimeBodyPart getAttach(MailParam mailParam) throws UnsupportedEncodingException, MessagingException {
        MimeBodyPart attach = new MimeBodyPart();
        ByteArrayDataSource rawData = new ByteArrayDataSource(mailParam.getAttachment(), "application/pdf");
        DataHandler dh = new DataHandler(rawData);// 文件流
        attach.setDataHandler(dh);
        attach.setFileName(MimeUtility.encodeText(mailParam.getAttachmentName(), "utf-8", null)); // 附件名
        return attach;
    }

   private static MailConfig getEmailBean(String source) throws javax.mail.MessagingException {

       Properties prop = new Properties();
       prop.put("mail.transport.protocol", "smtp");
       // 后期需要改成通过配置信息获取 ???
       prop.put("mail.smtp.host", getEmailConfig("OPD_EMAIL_HOST"));
       prop.put("mail.smtp.port", getEmailConfig("OPD_EMAIL_PORT"));
       Session session = Session.getInstance(prop);
       Transport ts = session.getTransport();
       // 发送邮件的服务器地址
       // 后期需要改成通过配置信息获取 ???
       String host = getEmailConfig("OPD_EMAIL_HOST");
       // 邮箱的用户名
       String username;
       // 邮箱授权码
       String password;
       // 后期需要改成通过配置信息获取 ???
       if (source.equals(EmailSource.TSMM.getName())) {
           // gtm邮箱的用户名和授权码
           username = getEmailConfig("OPD_EMAIL_USERNAME");
           password = getEmailConfig("OPD_EMAIL_PASSWORD");
       } else if (source.equals(EmailSource.MEETING.getName())) {
           // meeting邮箱的用户名和授权码
           username = getEmailConfig("MEETING_EMAIL_USERNAME");
           password = getEmailConfig("MEETING_EMAIL_PASSWORD");
       }else {
           throw new RuntimeException("邮箱源信息配置错误，请检查！");
       }

       //使用邮箱的用户名和密码连上邮件服务器，发送邮件时，发件人需要提交邮箱的用户名和密码给smtp服务器，
       //用户名和密码都通过验证之后才能够正常发送邮件给收件人。
       ts.connect(host, username, password);

       //创建邮件配置对象
       MailConfig mailConfig = new MailConfig();
       mailConfig.setProperties(prop);
       mailConfig.setSession(session);
       mailConfig.setMimeMessage(new MimeMessage(session)); //创建邮件对象
       mailConfig.setTransport(ts);
       return mailConfig;
   }

   private static String getEmailConfig(String key){
       Map<String,String> map = new HashMap<>();
//       map.put("OPD_EMAIL_HOST", "mail.asiainfo.com");
//       map.put("OPD_EMAIL_USERNAME", "5G@asiainfo.com");
//       map.put("OPD_EMAIL_PASSWORD", "Gtm@20230213!");
//       map.put("OPD_EMAIL_PORT", "25");
//       map.put("OPD_EMAIL_SSL", "false");
//       map.put("OPD_EMAIL_FROM", "5G@asiainfo.com");
//       map.put("MEETING_EMAIL_USERNAME", "meeting");
//       map.put("MEETING_EMAIL_PASSWORD", "gtm.1234");
//       map.put("MEETING_EMAIL_ADDRESS", "meeting@asiainfo.com");
//       map.put("MEETING_EMAIL_NAME", "Meeting");

       map.put("OPD_EMAIL_HOST", "mail.asiainfo.com");
       map.put("OPD_EMAIL_USERNAME", "AITech-PRD-techstack@asiainfo.com");
       map.put("OPD_EMAIL_PASSWORD", "1qaz@@4wsx");
       map.put("OPD_EMAIL_PORT", "25");
       map.put("OPD_EMAIL_SSL", "false");
       map.put("OPD_EMAIL_FROM", "AITech-PRD-techstack@asiainfo.com");
       map.put("MEETING_EMAIL_USERNAME", "meeting");
       map.put("MEETING_EMAIL_PASSWORD", "gtm.1234");
       map.put("MEETING_EMAIL_ADDRESS", "meeting@asiainfo.com");
       map.put("MEETING_EMAIL_NAME", "Meeting");
       return map.get(key);
   }

    /**
     * 将多个联系人转为列表，分隔符为逗号或者分号
     *
     * @param addresses 多个联系人，如果为空返回null
     * @return 联系人列表
     */
    // private static List<String> splitAddress(String addresses) {
    //     if (StringUtils.isEmpty(addresses)) {
    //         return null;
    //     }
    //     List<String> result;
    //     if (addresses.contains(",")) {
    //         result = Arrays.asList(addresses.trim().split(";"));
    //     } else {
    //         result = Collections.singletonList(addresses);
    //     }
    //     return result;
    // }

    /**
     * 对一个字符串中的宏进行替换(宏格式: ${<宏名称>}, 其中宏名称中的值用paramMap中的值替换)
     *
     * @param templateStr 模板字符串
     * @param paramMap    参数Map
     * @return 替换后的字符串
     */
    public static String replace(String templateStr, Map<String, Object> paramMap) {
        StringBuffer sb = new StringBuffer();
        // 定位带有${<宏名称>}符号的字符串，然后替换掉。
        Matcher m = MACRO_PATTERN.matcher(templateStr);
        while (m.find()) {
            String param = m.group();
            Object value = paramMap.get(param.substring(2, param.length() - 1));
            m.appendReplacement(sb, value == null ? "" : value.toString());
        }
        m.appendTail(sb);
        return sb.toString();
    }
}
