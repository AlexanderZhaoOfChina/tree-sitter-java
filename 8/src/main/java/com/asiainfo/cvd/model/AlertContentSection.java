package com.asiainfo.cvd.model;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class AlertContentSection {

    private String sectionName;

    private String sectionDescription;

    public AlertContentSection(){

    }

    public String getData(){
        //String newline = System.getProperty("line.separator");

        switch (sectionName) {
            case VulnerabilityDefinitions.VULNERABILITY_SEVERITY:
                if ("高".equals(sectionDescription)) {
                    return "<tr><td style=\"vertical-align: top;\">- </td><td>" + sectionName + "<span style=\"margin-top: 8px; margin-bottom:8px; font-weight:lighter; color: red;\">" + sectionDescription + "</span></td></tr>";
                }
                return "<tr><td style=\"vertical-align: top;\">- </td><td>" + sectionName + "<span style=\"margin-top: 8px; margin-bottom:8px; font-weight:lighter;\">" + sectionDescription + "</span></td></tr>";
            default:
                return "<tr><td style=\"vertical-align: top;\">- </td><td>" + sectionName + "<span style=\"margin-top: 8px; margin-bottom:8px; font-weight:lighter;\">" + sectionDescription + "</span></td></tr>";
        }

    }

    public String getData2(){
       //String newline = System.getProperty("line.separator");

        switch (sectionName) {
            case VulnerabilityDefinitions.VULNERABILITY_SEVERITY:
                if ("高".equals(sectionDescription)) {
                    return "<p style=\"margin-left: 48px; font-weight: bold; margin-top: 8px; margin-bottom: 8px;\">" + sectionName + "<span style=\"margin-top: 8px; margin-bottom:8px; font-weight:lighter; color: red;\">" + sectionDescription + "</span></p>";
                }
                return "<p style=\"margin-left: 48px; font-weight: bold; margin-top: 8px; margin-bottom: 8px;\">" + sectionName + "<span style=\"margin-top: 8px; margin-bottom:8px; font-weight:lighter;\">" + sectionDescription + "</span></p>";
            default:
                return "<p style=\"margin-left: 48px; font-weight: bold; margin-top: 8px; margin-bottom: 8px;\">" + sectionName + "<span style=\"margin-top: 8px; margin-bottom:8px; font-weight:lighter;\">" + sectionDescription + "</span></p>";
        }

    }

    public String getData1(){
        String newline = System.getProperty("line.separator");

        switch (sectionName) {
            case VulnerabilityDefinitions.VULNERABILITY_SEVERITY:
                if ("高".equals(sectionDescription)) {
                    return "<h3 style=\"margin-left: 40px; margin-bottom: 0px;\">" + sectionName + "</h3>" + newline + "<p style=\"text-indent: 74px; color: red; margin-top: 0px; margin-bottom: 0px;\">" + sectionDescription + "</p>";
                }
                return "<h3 style=\"margin-left: 40px; margin-bottom: 0px;\">" + sectionName + "</h3>" + newline + "<p style=\"text-indent: 74px; margin-top: 0px; margin-bottom: 0px;\">" + sectionDescription + "</p>";
            default:
                return "<h3 style=\"margin-left: 40px; margin-bottom: 0px;\">" + sectionName + "</h3>" + newline + "<span style=\"display:inline-block; margin-left:50px; margin-bottom: 0px;\"><p style=\"text-indent: 24px; margin-top: 0px; margin-bottom: 0px;\">" + sectionDescription + "</p></span>";
        }

    }
}
