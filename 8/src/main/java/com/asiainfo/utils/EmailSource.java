package com.asiainfo.utils;

public enum EmailSource {
    GTM("GTM(Go to Market)", "gtm邮件"),

    TSMM("Tech Stack Management Meeting", "漏洞预警通知邮件"),

    MEETING("meeting", "会议纪要邮件");

    private final String source;
    private final String name;

    EmailSource(String source, String name) {
        this.source = source;
        this.name = name;
    }

    public String getSource() {
        return source;
    }

    public String getName() {
        return name;
    }
}
