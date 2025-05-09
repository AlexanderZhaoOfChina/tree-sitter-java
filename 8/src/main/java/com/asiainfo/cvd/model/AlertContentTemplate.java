package com.asiainfo.cvd.model;

import lombok.Data;

import java.util.ArrayList;
import java.util.List;

@Data
public class AlertContentTemplate {

    private String title;

    //漏洞发现时间
    private String subTitle;

    private List<AlertContentSection> alertContentSectionList = new ArrayList<>();

    public String getData() {

        //String newline = System.getProperty("line.separator");
        StringBuilder content = new StringBuilder();

        content.append("<h3 style=\"margin-left: 30px; color: brown;\">").append(title).append("</h3>");  // 漏洞名称

        content.append("<table style=\"margin-left: 48px; font-weight: bold; margin-top: 8px; margin-bottom: 0px;\">");

        for (AlertContentSection alertContentSection : alertContentSectionList) {
            content.append(alertContentSection.getData());
        }

        content.append("</table>");

        return content.toString();
    }

    public void addVulnerabilityDesc(String description) {
        this.alertContentSectionList.add(new AlertContentSection(VulnerabilityDefinitions.VULNERABILITY_DESC, description));
    }

    public void addVulnerabilityNumber(String number) {
        this.alertContentSectionList.add(new AlertContentSection(VulnerabilityDefinitions.CNVD_NUMBER, number));
    }

    public void addVulnerabilitySeverity(String severity) {
        this.alertContentSectionList.add(new AlertContentSection(VulnerabilityDefinitions.VULNERABILITY_SEVERITY, severity));
    }

    public void addVulnerabilityaffectedVersion(String affectedVersion) {
        this.alertContentSectionList.add(new AlertContentSection(VulnerabilityDefinitions.AFFECTED_VERSION, affectedVersion));
    }

    public void addVulnerabilityRemediationAdvice(String remediationAdvice) {
        this.alertContentSectionList.add(new AlertContentSection(VulnerabilityDefinitions.REMEDIATION_ADVICE, remediationAdvice));
    }

}
