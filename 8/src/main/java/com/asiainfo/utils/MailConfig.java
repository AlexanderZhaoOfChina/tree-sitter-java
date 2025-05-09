package com.asiainfo.utils;

import lombok.Data;

import javax.mail.Session;
import javax.mail.Transport;
import javax.mail.internet.MimeMessage;
import java.util.Properties;

@Data
public class MailConfig {

    private Transport transport;
    private Session session;
    private Properties properties;
    private MimeMessage mimeMessage;
}
