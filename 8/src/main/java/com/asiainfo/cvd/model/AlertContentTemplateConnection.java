package com.asiainfo.cvd.model;

import lombok.Data;

import java.util.ArrayList;
import java.util.List;

@Data
public class AlertContentTemplateConnection {

    private String recipient;

    private String brief;

    private String overview;

    private List<AlertContentTemplate> alertContentTemplateList = new ArrayList<>();

    private String endingFragment = "<p style=\"font-weight: bold;\"> 如有问题烦请联系亚信科技技术栈管理员（AITech-PRD-techstack@asiainfo.com） </p>";

    public  void addAlertContentTemplate(AlertContentTemplate alertContentTemplate) {
        this.alertContentTemplateList.add(alertContentTemplate);
    }

    public String getData() {

        //String newline = System.getProperty("line.separator");
        StringBuilder content = new StringBuilder();

        content.append(this.recipient).append(brief).append(this.overview).append("<h3 style=\"margin-left: 15px;\">• 漏洞明细：</h3>");

        for (AlertContentTemplate alertContentTemplate : alertContentTemplateList) {
            content.append(alertContentTemplate.getData());
        }

        content.append("<br>~~~~~~~~~~~~~~~~~~~~~~~~<br>").append(endingFragment);

        return content.toString();
    }
}
