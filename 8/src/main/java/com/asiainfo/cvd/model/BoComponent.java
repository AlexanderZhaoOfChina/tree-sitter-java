package com.asiainfo.cvd.model;

import lombok.Data;

import java.time.LocalDateTime;

// 第三方组件表对应实体类
@Data
public class BoComponent {
    private Long id;
    private String componentName;
    private String componentDescribe;
    private Long useCount;
    private Long useCountExcludeBss;
    private String belongDirectoryName;
    private Long belongDirectoryId;

    private String officialLink;
    private String sourceCodeLink;
    private String lastVersion;
    private LocalDateTime lastModifiedDate;

    private String licenseType;
    private String vendor;
    private String vendorCountry;
    private String cveProductName;

    // 略去废弃字段...

    private String riskType;
    private String influenceType;
    private String replaceSolution;
    private String componentVersion;
    private String componentStatus;
}
