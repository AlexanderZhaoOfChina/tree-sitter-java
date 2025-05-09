# Java项目结构分析

| 类 | 方法 | 变量名 | 变量类型 | 变量位置 | 源文件位置 |
|---|------|-------|--------|--------|----------|
| com.asiainfo.cvd.daemon.CNVDDirectoryWatcherDaemon | main | | | | D:\8\src\main\java\com\asiainfo\cvd\daemon\CNVDDirectoryWatcherDaemon.java:33 / 方法:62 |
| | | task | com.asiainfo.cvd.daemon.TimerTask | 局部变量 | 行:73 |
| | | startTime |  | 局部变量 | 行:78 |
| | | timer | com.asiainfo.cvd.daemon.Timer | 局部变量 | 行:87 |
| | isFileProcessed | | | | D:\8\src\main\java\com\asiainfo\cvd\daemon\CNVDDirectoryWatcherDaemon.java:方法:102 |
| | | statusFile | com.asiainfo.cvd.daemon.File | 局部变量 | 行:104 |
| | | processStatus |  | 局部变量 | 行:108 |
| | markFileStatus | | | | D:\8\src\main\java\com\asiainfo\cvd\daemon\CNVDDirectoryWatcherDaemon.java:方法:119 |
| | | statusFile | com.asiainfo.cvd.daemon.File | 局部变量 | 行:120 |
| | | processStatus |  | 局部变量 | 行:121 |
| | scanDirectory | | | | D:\8\src\main\java\com\asiainfo\cvd\daemon\CNVDDirectoryWatcherDaemon.java:方法:135 |
| | | directory | com.asiainfo.cvd.daemon.File | 局部变量 | 行:136 |
| | | xmlFiles |  | 局部变量 | 行:137 |
| | | startTime |  | 局部变量 | 行:143 |
| | processXmlFile | | | | D:\8\src\main\java\com\asiainfo\cvd\daemon\CNVDDirectoryWatcherDaemon.java:方法:153 |
| | | sourceFileNameWithoutSuffix | com.asiainfo.cvd.daemon.String | 局部变量 | 行:154 |
| | | dbf | javax.xml.parsers.DocumentBuilderFactory | 局部变量 | 行:164 |
| | | db | javax.xml.parsers.DocumentBuilder | 局部变量 | 行:165 |
| | | doc | org.w3c.dom.Document | 局部变量 | 行:166 |
| | | vulnerabilities |  | 局部变量 | 行:168 |
| | | cves |  | 局部变量 | 行:169 |
| | | products |  | 局部变量 | 行:170 |
| | | vulnerabilitiesNodeList | org.w3c.dom.NodeList | 局部变量 | 行:173 |
| | | i |  | 局部变量 | 行:175 |
| | | vulnerability | org.w3c.dom.Element | 局部变量 | 行:176 |
| | | number | com.asiainfo.cvd.daemon.String | 局部变量 | 行:179 |
| | | title | com.asiainfo.cvd.daemon.String | 局部变量 | 行:180 |
| | | serverity | com.asiainfo.cvd.daemon.String | 局部变量 | 行:181 |
| | | isEvent | com.asiainfo.cvd.daemon.String | 局部变量 | 行:182 |
| | | submitTime | com.asiainfo.cvd.daemon.String | 局部变量 | 行:183 |
| | | openTime | com.asiainfo.cvd.daemon.String | 局部变量 | 行:184 |
| | | referenceLink | com.asiainfo.cvd.daemon.String | 局部变量 | 行:185 |
| | | formalWay | com.asiainfo.cvd.daemon.String | 局部变量 | 行:186 |
| | | description | com.asiainfo.cvd.daemon.String | 局部变量 | 行:187 |
| | | patchName | com.asiainfo.cvd.daemon.String | 局部变量 | 行:188 |
| | | patchDescription | com.asiainfo.cvd.daemon.String | 局部变量 | 行:189 |
| | | boVulnerability | com.asiainfo.cvd.daemon.BoVulnerability | 局部变量 | 行:192 |
| | | cvesNodeList | org.w3c.dom.NodeList | 局部变量 | 行:209 |
| | | j |  | 局部变量 | 行:210 |
| | | cve | org.w3c.dom.Element | 局部变量 | 行:211 |
| | | cveNumber | com.asiainfo.cvd.daemon.String | 局部变量 | 行:212 |
| | | cveUrl | com.asiainfo.cvd.daemon.String | 局部变量 | 行:213 |
| | | boVulnerabilityCve | com.asiainfo.cvd.daemon.BoVulnerabilityCve | 局部变量 | 行:215 |
| | | productsNodeList | org.w3c.dom.NodeList | 局部变量 | 行:224 |
| | | k |  | 局部变量 | 行:225 |
| | | product | org.w3c.dom.Element | 局部变量 | 行:226 |
| | | name | com.asiainfo.cvd.daemon.String | 局部变量 | 行:227 |
| | | boVulnerabilityProduct | com.asiainfo.cvd.daemon.BoVulnerabilityProduct | 局部变量 | 行:229 |
| | | alertBrief | com.asiainfo.cvd.daemon.VulnerabilityAlertBrief | 局部变量 | 行:247 |
| | | alertList |  | 局部变量 | 行:250 |
| | | components |  | 局部变量 | 行:251 |
| | | filterNames |  | 局部变量 | 行:254 |
| | | boVulnerabilityProductList2 |  | 局部变量 | 行:257 |
| | | boVulnerability | com.asiainfo.cvd.daemon.BoVulnerability | 局部变量 | 行:262 |
| | | vulnerabilityAlert | com.asiainfo.cvd.daemon.VulnerabilityAlert | 局部变量 | 行:265 |
| | | startTime |  | 局部变量 | 行:287 |
| | backupXMLFileForException | | | | D:\8\src\main\java\com\asiainfo\cvd\daemon\CNVDDirectoryWatcherDaemon.java:方法:310 |
| | | sourceDirectory | com.asiainfo.cvd.daemon.String | 局部变量 | 行:311 |
| | | sourceFileName | com.asiainfo.cvd.daemon.String | 局部变量 | 行:312 |
| | | sourcePath | com.asiainfo.cvd.daemon.String | 局部变量 | 行:313 |
| | | backupDirectory | com.asiainfo.cvd.daemon.String | 局部变量 | 行:314 |
| | | backupPath | com.asiainfo.cvd.daemon.String | 局部变量 | 行:316 |
| | backupXMLFile | | | | D:\8\src\main\java\com\asiainfo\cvd\daemon\CNVDDirectoryWatcherDaemon.java:方法:330 |
| | | backupStartTime |  | 局部变量 | 行:332 |
| | | sourceDirectory | com.asiainfo.cvd.daemon.String | 局部变量 | 行:334 |
| | | sourceFileName | com.asiainfo.cvd.daemon.String | 局部变量 | 行:335 |
| | | sourcePath | com.asiainfo.cvd.daemon.String | 局部变量 | 行:336 |
| | | backupDirectory | com.asiainfo.cvd.daemon.String | 局部变量 | 行:337 |
| | | backupPath | com.asiainfo.cvd.daemon.String | 局部变量 | 行:339 |
| | | backupEndTime |  | 局部变量 | 行:351 |
| | createDirectory | | | | D:\8\src\main\java\com\asiainfo\cvd\daemon\CNVDDirectoryWatcherDaemon.java:方法:360 |
| | | file | com.asiainfo.cvd.daemon.File | 局部变量 | 行:361 |
| | | logger | org.slf4j.Logger | 类字段 | 行:35 |
| | | BASE_DIR | com.asiainfo.cvd.daemon.String | 类字段 | 行:38 |
| | | DIRECTORY_PATH | com.asiainfo.cvd.daemon.String | 类字段 | 行:41 |
| | | DATA_STORE_PATH | com.asiainfo.cvd.daemon.String | 类字段 | 行:44 |
| | | PROCESS_STATUS_FILE | com.asiainfo.cvd.daemon.String | 类字段 | 行:47 |
| | | objectMapper | com.fasterxml.jackson.databind.ObjectMapper | 类字段 | 行:50 |
| | | SCAN_INTERVAL |  | 类字段 | 行:53 |
| | | componentService | com.asiainfo.cvd.service.ComponentService | 类字段 | 行:56 |
| | | vulnerabilityService | com.asiainfo.cvd.service.VulnerabilityService | 类字段 | 行:57 |
| com.asiainfo.cvd.daemon.DataCleanupProcessor | cleanupDataStore | | | | D:\8\src\main\java\com\asiainfo\cvd\daemon\DataCleanupProcessor.java:14 / 方法:20 |
| | | dataStorePath | com.asiainfo.cvd.daemon.Path | 局部变量 | 行:22 |
| | deleteProcessStatus | | | | D:\8\src\main\java\com\asiainfo\cvd\daemon\DataCleanupProcessor.java:方法:48 |
| | | processStatusPath | com.asiainfo.cvd.daemon.Path | 局部变量 | 行:49 |
| | moveBackupFile | | | | D:\8\src\main\java\com\asiainfo\cvd\daemon\DataCleanupProcessor.java:方法:64 |
| | | sourcePath | com.asiainfo.cvd.daemon.Path | 局部变量 | 行:65 |
| | | targetPath | com.asiainfo.cvd.daemon.Path | 局部变量 | 行:66 |
| | moveBackupExceptionFile | | | | D:\8\src\main\java\com\asiainfo\cvd\daemon\DataCleanupProcessor.java:方法:80 |
| | | sourcePath | com.asiainfo.cvd.daemon.Path | 局部变量 | 行:81 |
| | | targetPath | com.asiainfo.cvd.daemon.Path | 局部变量 | 行:82 |
| | performFullCleanup | | | | D:\8\src\main\java\com\asiainfo\cvd\daemon\DataCleanupProcessor.java:方法:99 |
| | main | | | | D:\8\src\main\java\com\asiainfo\cvd\daemon\DataCleanupProcessor.java:方法:110 |
| | | logger | org.slf4j.Logger | 类字段 | 行:15 |
| com.asiainfo.cvd.daemon.EmailListBuilder | initializeIfNeeded | | | | D:\8\src\main\java\com\asiainfo\cvd\daemon\EmailListBuilder.java:20 / 方法:32 |
| | isTestMode | | | | D:\8\src\main\java\com\asiainfo\cvd\daemon\EmailListBuilder.java:方法:50 |
| | parseEmailList | | | | D:\8\src\main\java\com\asiainfo\cvd\daemon\EmailListBuilder.java:方法:62 |
| | getExpertEmails | | | | D:\8\src\main\java\com\asiainfo\cvd\daemon\EmailListBuilder.java:方法:77 |
| | | testEmails |  | 局部变量 | 行:81 |
| | | expertList | com.asiainfo.cvd.daemon.String | 局部变量 | 行:86 |
| | | expertEmails |  | 局部变量 | 行:87 |
| | getCcEmails | | | | D:\8\src\main\java\com\asiainfo\cvd\daemon\EmailListBuilder.java:方法:103 |
| | | ccList | com.asiainfo.cvd.daemon.String | 局部变量 | 行:110 |
| | | ccEmails |  | 局部变量 | 行:111 |
| | | logger | org.slf4j.Logger | 类字段 | 行:21 |
| | | properties | java.util.Properties | 类字段 | 行:22 |
| | | initialized |  | 类字段 | 行:23 |
| com.asiainfo.cvd.daemon.NotificationEmailProcessor | process | | | | D:\8\src\main\java\com\asiainfo\cvd\daemon\NotificationEmailProcessor.java:24 / 方法:37 |
| | | mailParam | com.asiainfo.utils.MailParam | 局部变量 | 行:39 |
| | | alertContentTemplateConnection | com.asiainfo.cvd.daemon.AlertContentTemplateConnection | 局部变量 | 行:54 |
| | | overview | com.asiainfo.cvd.daemon.StringBuilder | 局部变量 | 行:61 |
| | | componentDescription | com.asiainfo.cvd.daemon.String | 局部变量 | 行:68 |
| | | alertContentSectionList |  | 局部变量 | 行:96 |
| | | alertContentTemplate | com.asiainfo.cvd.daemon.AlertContentTemplate | 局部变量 | 行:99 |
| | isEmailSendEnabled | | | | D:\8\src\main\java\com\asiainfo\cvd\daemon\NotificationEmailProcessor.java:方法:131 |
| | | properties | java.util.Properties | 局部变量 | 行:133 |
| | getAlertContentSectionList | | | | D:\8\src\main\java\com\asiainfo\cvd\daemon\NotificationEmailProcessor.java:方法:148 |
| | | alertContentSectionList |  | 局部变量 | 行:151 |
| | | alertContentSection0 | com.asiainfo.cvd.daemon.AlertContentSection | 局部变量 | 行:154 |
| | | alertContentSection1 | com.asiainfo.cvd.daemon.AlertContentSection | 局部变量 | 行:160 |
| | | alertContentSection2 | com.asiainfo.cvd.daemon.AlertContentSection | 局部变量 | 行:166 |
| | | alertContentSection3 | com.asiainfo.cvd.daemon.AlertContentSection | 局部变量 | 行:172 |
| | | alertContentSection4 | com.asiainfo.cvd.daemon.AlertContentSection | 局部变量 | 行:178 |
| | | alertContentSection5 | com.asiainfo.cvd.daemon.AlertContentSection | 局部变量 | 行:184 |
| | | logger | org.apache.logging.log4j.Logger | 类字段 | 行:26 |
| com.asiainfo.cvd.model.AlertContentSection | getData | | | | D:\8\src\main\java\com\asiainfo\cvd\model\AlertContentSection.java:6 / 方法:18 |
| | getData2 | | | | D:\8\src\main\java\com\asiainfo\cvd\model\AlertContentSection.java:方法:33 |
| | getData1 | | | | D:\8\src\main\java\com\asiainfo\cvd\model\AlertContentSection.java:方法:48 |
| | | newline | com.asiainfo.cvd.model.String | 局部变量 | 行:49 |
| | | sectionName | com.asiainfo.cvd.model.String | 类字段 | 行:10 |
| | | sectionDescription | com.asiainfo.cvd.model.String | 类字段 | 行:12 |
| com.asiainfo.cvd.model.AlertContentTemplate | getData | | | | D:\8\src\main\java\com\asiainfo\cvd\model\AlertContentTemplate.java:8 / 方法:18 |
| | | content | com.asiainfo.cvd.model.StringBuilder | 局部变量 | 行:21 |
| | addVulnerabilityDesc | | | | D:\8\src\main\java\com\asiainfo\cvd\model\AlertContentTemplate.java:方法:36 |
| | addVulnerabilityNumber | | | | D:\8\src\main\java\com\asiainfo\cvd\model\AlertContentTemplate.java:方法:40 |
| | addVulnerabilitySeverity | | | | D:\8\src\main\java\com\asiainfo\cvd\model\AlertContentTemplate.java:方法:44 |
| | addVulnerabilityaffectedVersion | | | | D:\8\src\main\java\com\asiainfo\cvd\model\AlertContentTemplate.java:方法:48 |
| | addVulnerabilityRemediationAdvice | | | | D:\8\src\main\java\com\asiainfo\cvd\model\AlertContentTemplate.java:方法:52 |
| | | title | com.asiainfo.cvd.model.String | 类字段 | 行:11 |
| | | subTitle | com.asiainfo.cvd.model.String | 类字段 | 行:14 |
| | | alertContentSectionList |  | 类字段 | 行:16 |
| com.asiainfo.cvd.model.AlertContentTemplateConnection | addAlertContentTemplate | | | | D:\8\src\main\java\com\asiainfo\cvd\model\AlertContentTemplateConnection.java:8 / 方法:21 |
| | getData | | | | D:\8\src\main\java\com\asiainfo\cvd\model\AlertContentTemplateConnection.java:方法:25 |
| | | content | com.asiainfo.cvd.model.StringBuilder | 局部变量 | 行:28 |
| | | recipient | com.asiainfo.cvd.model.String | 类字段 | 行:11 |
| | | brief | com.asiainfo.cvd.model.String | 类字段 | 行:13 |
| | | overview | com.asiainfo.cvd.model.String | 类字段 | 行:15 |
| | | alertContentTemplateList |  | 类字段 | 行:17 |
| | | endingFragment | com.asiainfo.cvd.model.String | 类字段 | 行:19 |
| com.asiainfo.cvd.model.BoComponent | | id | com.asiainfo.cvd.model.Long | 类字段 | D:\8\src\main\java\com\asiainfo\cvd\model\BoComponent.java:8 / 字段:10 |
| | | componentName | com.asiainfo.cvd.model.String | 类字段 | 行:11 |
| | | componentDescribe | com.asiainfo.cvd.model.String | 类字段 | 行:12 |
| | | useCount | com.asiainfo.cvd.model.Long | 类字段 | 行:13 |
| | | useCountExcludeBss | com.asiainfo.cvd.model.Long | 类字段 | 行:14 |
| | | belongDirectoryName | com.asiainfo.cvd.model.String | 类字段 | 行:15 |
| | | belongDirectoryId | com.asiainfo.cvd.model.Long | 类字段 | 行:16 |
| | | officialLink | com.asiainfo.cvd.model.String | 类字段 | 行:18 |
| | | sourceCodeLink | com.asiainfo.cvd.model.String | 类字段 | 行:19 |
| | | lastVersion | com.asiainfo.cvd.model.String | 类字段 | 行:20 |
| | | lastModifiedDate | java.time.LocalDateTime | 类字段 | 行:21 |
| | | licenseType | com.asiainfo.cvd.model.String | 类字段 | 行:23 |
| | | vendor | com.asiainfo.cvd.model.String | 类字段 | 行:24 |
| | | vendorCountry | com.asiainfo.cvd.model.String | 类字段 | 行:25 |
| | | cveProductName | com.asiainfo.cvd.model.String | 类字段 | 行:26 |
| | | riskType | com.asiainfo.cvd.model.String | 类字段 | 行:30 |
| | | influenceType | com.asiainfo.cvd.model.String | 类字段 | 行:31 |
| | | replaceSolution | com.asiainfo.cvd.model.String | 类字段 | 行:32 |
| | | componentVersion | com.asiainfo.cvd.model.String | 类字段 | 行:33 |
| | | componentStatus | com.asiainfo.cvd.model.String | 类字段 | 行:34 |
| com.asiainfo.cvd.model.BoVulnerability | | id | com.asiainfo.cvd.model.Long | 类字段 | D:\8\src\main\java\com\asiainfo\cvd\model\BoVulnerability.java:5 / 字段:8 |
| | | fileName | com.asiainfo.cvd.model.String | 类字段 | 行:9 |
| | | number | com.asiainfo.cvd.model.String | 类字段 | 行:10 |
| | | title | com.asiainfo.cvd.model.String | 类字段 | 行:11 |
| | | serverity | com.asiainfo.cvd.model.String | 类字段 | 行:12 |
| | | isEvent | com.asiainfo.cvd.model.String | 类字段 | 行:13 |
| | | submitTime | com.asiainfo.cvd.model.String | 类字段 | 行:14 |
| | | openTime | com.asiainfo.cvd.model.String | 类字段 | 行:15 |
| | | referenceLink | com.asiainfo.cvd.model.String | 类字段 | 行:16 |
| | | formalWay | com.asiainfo.cvd.model.String | 类字段 | 行:17 |
| | | description | com.asiainfo.cvd.model.String | 类字段 | 行:18 |
| | | patchName | com.asiainfo.cvd.model.String | 类字段 | 行:19 |
| | | patchDescription | com.asiainfo.cvd.model.String | 类字段 | 行:20 |
| com.asiainfo.cvd.model.BoVulnerabilityCve | | id | com.asiainfo.cvd.model.Long | 类字段 | D:\8\src\main\java\com\asiainfo\cvd\model\BoVulnerabilityCve.java:5 / 字段:8 |
| | | fileName | com.asiainfo.cvd.model.String | 类字段 | 行:9 |
| | | cnvdNumber | com.asiainfo.cvd.model.String | 类字段 | 行:10 |
| | | cveNumber | com.asiainfo.cvd.model.String | 类字段 | 行:11 |
| | | cveUrl | com.asiainfo.cvd.model.String | 类字段 | 行:12 |
| com.asiainfo.cvd.model.BoVulnerabilityProduct | | id | com.asiainfo.cvd.model.Long | 类字段 | D:\8\src\main\java\com\asiainfo\cvd\model\BoVulnerabilityProduct.java:5 / 字段:8 |
| | | fileName | com.asiainfo.cvd.model.String | 类字段 | 行:9 |
| | | cnvdNumber | com.asiainfo.cvd.model.String | 类字段 | 行:10 |
| | | product | com.asiainfo.cvd.model.String | 类字段 | 行:11 |
| com.asiainfo.cvd.model.Counter | increment | | | | D:\8\src\main\java\com\asiainfo\cvd\model\Counter.java:3 / 方法:10 |
| | getCount | | | | D:\8\src\main\java\com\asiainfo\cvd\model\Counter.java:方法:15 |
| | getRawCount | | | | D:\8\src\main\java\com\asiainfo\cvd\model\Counter.java:方法:20 |
| | addZero | | | | D:\8\src\main\java\com\asiainfo\cvd\model\Counter.java:方法:25 |
| | | numberString | com.asiainfo.cvd.model.String | 局部变量 | 行:26 |
| | | count |  | 类字段 | 行:5 |
| com.asiainfo.cvd.model.VulnerabilityAlert | | sourceFileNameWithoutSuffix | com.asiainfo.cvd.model.String | 类字段 | D:\8\src\main\java\com\asiainfo\cvd\model\VulnerabilityAlert.java:6 / 字段:10 |
| | | component | com.asiainfo.cvd.model.String | 类字段 | 行:11 |
| | | cnvdNumber | com.asiainfo.cvd.model.String | 类字段 | 行:12 |
| | | cveNumber | com.asiainfo.cvd.model.String | 类字段 | 行:13 |
| | | title | com.asiainfo.cvd.model.String | 类字段 | 行:14 |
| | | description | com.asiainfo.cvd.model.String | 类字段 | 行:15 |
| | | Severity | com.asiainfo.cvd.model.String | 类字段 | 行:16 |
| | | openTime | com.asiainfo.cvd.model.String | 类字段 | 行:17 |
| | | affectedVersion | com.asiainfo.cvd.model.String | 类字段 | 行:18 |
| | | remediationAdvice | com.asiainfo.cvd.model.String | 类字段 | 行:19 |
| com.asiainfo.cvd.model.VulnerabilityAlertBrief | appendComponent | | | | D:\8\src\main\java\com\asiainfo\cvd\model\VulnerabilityAlertBrief.java:8 / 方法:21 |
| | getData | | | | D:\8\src\main\java\com\asiainfo\cvd\model\VulnerabilityAlertBrief.java:方法:25 |
| | | brief | com.asiainfo.cvd.model.StringBuilder | 局部变量 | 行:27 |
| | | issuingOrganization | com.asiainfo.cvd.model.String | 类字段 | 行:11 |
| | | reportingCycle | com.asiainfo.cvd.model.String | 类字段 | 行:13 |
| | | componentScope |  | 类字段 | 行:15 |
| | | dataSources | com.asiainfo.cvd.model.String | 类字段 | 行:17 |
| | | CNVD_AND_CVE | com.asiainfo.cvd.model.String | 类字段 | 行:19 |
| com.asiainfo.cvd.model.VulnerabilityDefinitions | | CVE_NUMBER | com.asiainfo.cvd.model.String | 类字段 | D:\8\src\main\java\com\asiainfo\cvd\model\VulnerabilityDefinitions.java:3 / 字段:5 |
| | | VULNERABILITY_TITLE | com.asiainfo.cvd.model.String | 类字段 | 行:6 |
| | | COMPONENT | com.asiainfo.cvd.model.String | 类字段 | 行:7 |
| | | CNVD_NUMBER | com.asiainfo.cvd.model.String | 类字段 | 行:8 |
| | | VULNERABILITY_DESC | com.asiainfo.cvd.model.String | 类字段 | 行:9 |
| | | VULNERABILITY_SEVERITY | com.asiainfo.cvd.model.String | 类字段 | 行:10 |
| | | AFFECTED_VERSION | com.asiainfo.cvd.model.String | 类字段 | 行:11 |
| | | REMEDIATION_ADVICE | com.asiainfo.cvd.model.String | 类字段 | 行:12 |
| com.asiainfo.cvd.service.ComponentService | readComponentsFromExcel | | | | D:\8\src\main\java\com\asiainfo\cvd\service\ComponentService.java:15 / 方法:30 |
| | | components |  | 局部变量 | 行:31 |
| | | configFile | com.asiainfo.cvd.service.File | 局部变量 | 行:33 |
| | | sheet | com.asiainfo.cvd.service.Sheet | 局部变量 | 行:41 |
| | | rowIterator |  | 局部变量 | 行:43 |
| | | row | com.asiainfo.cvd.service.Row | 局部变量 | 行:49 |
| | | component | com.asiainfo.cvd.model.BoComponent | 局部变量 | 行:50 |
| | | dateStr | com.asiainfo.cvd.service.String | 局部变量 | 行:65 |
| | | dateTime | java.time.LocalDateTime | 局部变量 | 行:66 |
| | getStringValue | | | | D:\8\src\main\java\com\asiainfo\cvd\service\ComponentService.java:方法:116 |
| | getIntValue | | | | D:\8\src\main\java\com\asiainfo\cvd\service\ComponentService.java:方法:135 |
| | readComponentFilterNameList | | | | D:\8\src\main\java\com\asiainfo\cvd\service\ComponentService.java:方法:156 |
| | | filterNames |  | 局部变量 | 行:157 |
| | | configFile | com.asiainfo.cvd.service.File | 局部变量 | 行:160 |
| | | sheet | com.asiainfo.cvd.service.Sheet | 局部变量 | 行:169 |
| | | rowIterator |  | 局部变量 | 行:171 |
| | | row | com.asiainfo.cvd.service.Row | 局部变量 | 行:177 |
| | | currentComponentName | com.asiainfo.cvd.service.String | 局部变量 | 行:178 |
| | | filterName | com.asiainfo.cvd.service.String | 局部变量 | 行:179 |
| | | logger | org.slf4j.Logger | 类字段 | 行:16 |
| | | BASE_DIR | com.asiainfo.cvd.service.String | 类字段 | 行:19 |
| | | COMPONENTS_CONFIG_PATH | com.asiainfo.cvd.service.String | 类字段 | 行:22 |
| | | COMPONENT_FILTERS_PATH | com.asiainfo.cvd.service.String | 类字段 | 行:25 |
| com.asiainfo.cvd.service.VulnerabilityService | saveVulnerabilityData | | | | D:\8\src\main\java\com\asiainfo\cvd\service\VulnerabilityService.java:19 / 方法:31 |
| | | datePath | com.asiainfo.cvd.service.String | 局部变量 | 行:34 |
| | | storePath | com.asiainfo.cvd.service.String | 局部变量 | 行:35 |
| | | vulnFile | java.io.File | 局部变量 | 行:39 |
| | | cveFile | java.io.File | 局部变量 | 行:43 |
| | | productFile | java.io.File | 局部变量 | 行:47 |
| | readVulnerability | | | | D:\8\src\main\java\com\asiainfo\cvd\service\VulnerabilityService.java:方法:56 |
| | | dateDirs |  | 局部变量 | 行:57 |
| | | vulnFiles |  | 局部变量 | 行:60 |
| | | vulnerabilities |  | 局部变量 | 行:63 |
| | | found |  | 局部变量 | 行:65 |
| | readVulnerabilityProducts | | | | D:\8\src\main\java\com\asiainfo\cvd\service\VulnerabilityService.java:方法:81 |
| | | datePath | com.asiainfo.cvd.service.String | 局部变量 | 行:82 |
| | | storePath | com.asiainfo.cvd.service.String | 局部变量 | 行:83 |
| | | productFile | java.io.File | 局部变量 | 行:84 |
| | | allProducts |  | 局部变量 | 行:90 |
| | eliminateDuplicate | | | | D:\8\src\main\java\com\asiainfo\cvd\service\VulnerabilityService.java:方法:102 |
| | | counter | com.asiainfo.cvd.service.Counter | 局部变量 | 行:103 |
| | | sourceFileNameWithoutSuffix | com.asiainfo.cvd.service.String | 局部变量 | 行:109 |
| | | component | com.asiainfo.cvd.service.String | 局部变量 | 行:110 |
| | | cnvdNumber | com.asiainfo.cvd.service.String | 局部变量 | 行:111 |
| | | cveNumber | com.asiainfo.cvd.service.String | 局部变量 | 行:112 |
| | | title | com.asiainfo.cvd.service.String | 局部变量 | 行:113 |
| | | description | com.asiainfo.cvd.service.String | 局部变量 | 行:114 |
| | | severity | com.asiainfo.cvd.service.String | 局部变量 | 行:115 |
| | | openTime | com.asiainfo.cvd.service.String | 局部变量 | 行:116 |
| | | affectedVersions | com.asiainfo.cvd.service.String | 局部变量 | 行:117 |
| | | remediationAdvice | com.asiainfo.cvd.service.String | 局部变量 | 行:120 |
| | vulnerabilityCveJoin | | | | D:\8\src\main\java\com\asiainfo\cvd\service\VulnerabilityService.java:方法:130 |
| | printBoVulnerabilityProductList | | | | D:\8\src\main\java\com\asiainfo\cvd\service\VulnerabilityService.java:方法:140 |
| | | counter | com.asiainfo.cvd.service.Counter | 局部变量 | 行:141 |
| | createDirectoryIfNotExists | | | | D:\8\src\main\java\com\asiainfo\cvd\service\VulnerabilityService.java:方法:148 |
| | | file | java.io.File | 局部变量 | 行:149 |
| | | logger | org.slf4j.Logger | 类字段 | 行:20 |
| | | objectMapper | com.fasterxml.jackson.databind.ObjectMapper | 类字段 | 行:21 |
| | | dataStorePath | com.asiainfo.cvd.service.String | 类字段 | 行:22 |
| com.asiainfo.utils.ConfigurationExporter | exportAllConfigurations | | | | D:\8\src\main\java\com\asiainfo\utils\ConfigurationExporter.java:16 / 方法:35 |
| | exportComponents | | | | D:\8\src\main\java\com\asiainfo\utils\ConfigurationExporter.java:方法:50 |
| | | components |  | 局部变量 | 行:51 |
| | | sql | com.asiainfo.utils.String | 局部变量 | 行:53 |
| | | component | com.asiainfo.cvd.model.BoComponent | 局部变量 | 行:58 |
| | | componentsFile | java.io.File | 局部变量 | 行:67 |
| | exportComponentFilters | | | | D:\8\src\main\java\com\asiainfo\utils\ConfigurationExporter.java:方法:75 |
| | | sql | com.asiainfo.utils.String | 局部变量 | 行:76 |
| | | filterMap |  | 局部变量 | 行:77 |
| | | componentName | com.asiainfo.utils.String | 局部变量 | 行:83 |
| | | filterName | com.asiainfo.utils.String | 局部变量 | 行:84 |
| | | componentName | com.asiainfo.utils.String | 局部变量 | 行:93 |
| | | filters |  | 局部变量 | 行:94 |
| | | filterFile | java.io.File | 局部变量 | 行:96 |
| | createConfigDirectory | | | | D:\8\src\main\java\com\asiainfo\utils\ConfigurationExporter.java:方法:105 |
| | | configDir | java.io.File | 局部变量 | 行:106 |
| | main | | | | D:\8\src\main\java\com\asiainfo\utils\ConfigurationExporter.java:方法:115 |
| | | dbUrl | com.asiainfo.utils.String | 局部变量 | 行:116 |
| | | dbUser | com.asiainfo.utils.String | 局部变量 | 行:117 |
| | | dbPassword | com.asiainfo.utils.String | 局部变量 | 行:118 |
| | | exporter | com.asiainfo.utils.ConfigurationExporter | 局部变量 | 行:121 |
| | | CONFIG_DIR | com.asiainfo.utils.String | 类字段 | 行:18 |
| | | objectMapper | com.fasterxml.jackson.databind.ObjectMapper | 类字段 | 行:19 |
| | | dbUrl | com.asiainfo.utils.String | 类字段 | 行:22 |
| | | dbUser | com.asiainfo.utils.String | 类字段 | 行:23 |
| | | dbPassword | com.asiainfo.utils.String | 类字段 | 行:24 |
| com.asiainfo.utils.DataExporter | exportAllToExcel | | | | D:\8\src\main\java\com\asiainfo\utils\DataExporter.java:17 / 方法:33 |
| | | timestamp | com.asiainfo.utils.String | 局部变量 | 行:38 |
| | | excelFileName | com.asiainfo.utils.String | 局部变量 | 行:39 |
| | | excelFile | java.io.File | 局部变量 | 行:40 |
| | | conn | com.asiainfo.utils.Connection | 局部变量 | 行:44 |
| | exportComponentsToSheet | | | | D:\8\src\main\java\com\asiainfo\utils\DataExporter.java:方法:64 |
| | | sheet | com.asiainfo.utils.Sheet | 局部变量 | 行:65 |
| | | headerStyle | com.asiainfo.utils.CellStyle | 局部变量 | 行:68 |
| | | headerRow | com.asiainfo.utils.Row | 局部变量 | 行:71 |
| | | headers |  | 局部变量 | 行:72 |
| | | i |  | 局部变量 | 行:81 |
| | | cell | com.asiainfo.utils.Cell | 局部变量 | 行:82 |
| | | sql | com.asiainfo.utils.String | 局部变量 | 行:88 |
| | | rowNum |  | 局部变量 | 行:98 |
| | | row | com.asiainfo.utils.Row | 局部变量 | 行:100 |
| | | i |  | 局部变量 | 行:135 |
| | exportFiltersToSheet | | | | D:\8\src\main\java\com\asiainfo\utils\DataExporter.java:方法:144 |
| | | sheet | com.asiainfo.utils.Sheet | 局部变量 | 行:145 |
| | | headerStyle | com.asiainfo.utils.CellStyle | 局部变量 | 行:148 |
| | | headerRow | com.asiainfo.utils.Row | 局部变量 | 行:151 |
| | | headers |  | 局部变量 | 行:152 |
| | | i |  | 局部变量 | 行:155 |
| | | cell | com.asiainfo.utils.Cell | 局部变量 | 行:156 |
| | | sql | com.asiainfo.utils.String | 局部变量 | 行:162 |
| | | rowNum |  | 局部变量 | 行:166 |
| | | row | com.asiainfo.utils.Row | 局部变量 | 行:168 |
| | | i |  | 局部变量 | 行:175 |
| | getStringValue | | | | D:\8\src\main\java\com\asiainfo\utils\DataExporter.java:方法:184 |
| | | value | com.asiainfo.utils.Object | 局部变量 | 行:185 |
| | createHeaderStyle | | | | D:\8\src\main\java\com\asiainfo\utils\DataExporter.java:方法:192 |
| | | style | com.asiainfo.utils.CellStyle | 局部变量 | 行:193 |
| | | font | com.asiainfo.utils.Font | 局部变量 | 行:206 |
| | createExportDirectory | | | | D:\8\src\main\java\com\asiainfo\utils\DataExporter.java:方法:219 |
| | | exportDir | java.io.File | 局部变量 | 行:220 |
| | main | | | | D:\8\src\main\java\com\asiainfo\utils\DataExporter.java:方法:229 |
| | | dbUrl | com.asiainfo.utils.String | 局部变量 | 行:230 |
| | | dbUser | com.asiainfo.utils.String | 局部变量 | 行:231 |
| | | dbPassword | com.asiainfo.utils.String | 局部变量 | 行:232 |
| | | exporter | com.asiainfo.utils.DataExporter | 局部变量 | 行:235 |
| | | EXPORT_DIR | com.asiainfo.utils.String | 类字段 | 行:19 |
| | | dbUrl | com.asiainfo.utils.String | 类字段 | 行:20 |
| | | dbUser | com.asiainfo.utils.String | 类字段 | 行:21 |
| | | dbPassword | com.asiainfo.utils.String | 类字段 | 行:22 |
| com.asiainfo.utils.ExcelTemplateGenerator | generateComponentsTemplate | | | | D:\8\src\main\java\com\asiainfo\utils\ExcelTemplateGenerator.java:14 / 方法:19 |
| | | sheet | com.asiainfo.utils.Sheet | 局部变量 | 行:21 |
| | | headerRow | com.asiainfo.utils.Row | 局部变量 | 行:24 |
| | | headers |  | 局部变量 | 行:25 |
| | | headerStyle | com.asiainfo.utils.CellStyle | 局部变量 | 行:36 |
| | | i |  | 局部变量 | 行:39 |
| | | cell | com.asiainfo.utils.Cell | 局部变量 | 行:40 |
| | generateComponentFiltersTemplate | | | | D:\8\src\main\java\com\asiainfo\utils\ExcelTemplateGenerator.java:方法:56 |
| | | sheet | com.asiainfo.utils.Sheet | 局部变量 | 行:58 |
| | | headerRow | com.asiainfo.utils.Row | 局部变量 | 行:61 |
| | | headers |  | 局部变量 | 行:62 |
| | | headerStyle | com.asiainfo.utils.CellStyle | 局部变量 | 行:67 |
| | | i |  | 局部变量 | 行:70 |
| | | cell | com.asiainfo.utils.Cell | 局部变量 | 行:71 |
| | createHeaderStyle | | | | D:\8\src\main\java\com\asiainfo\utils\ExcelTemplateGenerator.java:方法:87 |
| | | style | com.asiainfo.utils.CellStyle | 局部变量 | 行:88 |
| | | font | com.asiainfo.utils.Font | 局部变量 | 行:101 |
| | main | | | | D:\8\src\main\java\com\asiainfo\utils\ExcelTemplateGenerator.java:方法:111 |
| | | configDir | java.io.File | 局部变量 | 行:114 |
| com.asiainfo.utils.MailConfig | | transport | javax.mail.Transport | 类字段 | D:\8\src\main\java\com\asiainfo\utils\MailConfig.java:10 / 字段:13 |
| | | session | javax.mail.Session | 类字段 | 行:14 |
| | | properties | java.util.Properties | 类字段 | 行:15 |
| | | mimeMessage | javax.mail.internet.MimeMessage | 类字段 | 行:16 |
| com.asiainfo.utils.MailParam | | tos |  | 类字段 | D:\8\src\main\java\com\asiainfo\utils\MailParam.java:9 / 字段:16 |
| | | ccs |  | 类字段 | 行:21 |
| | | title | com.asiainfo.utils.String | 类字段 | 行:26 |
| | | content | com.asiainfo.utils.String | 类字段 | 行:32 |
| | | attachmentName | com.asiainfo.utils.String | 类字段 | 行:37 |
| | | attachment |  | 类字段 | 行:42 |
| com.asiainfo.utils.MailUtil | sendPdfToPicture | | | | D:\8\src\main\java\com\asiainfo\utils\MailUtil.java:22 / 方法:35 |
| | sendText | | | | D:\8\src\main\java\com\asiainfo\utils\MailUtil.java:方法:51 |
| | send | | | | D:\8\src\main\java\com\asiainfo\utils\MailUtil.java:方法:55 |
| | | mailConfig | com.asiainfo.utils.MailConfig | 局部变量 | 行:59 |
| | | message | com.asiainfo.utils.MimeMessage | 局部变量 | 行:60 |
| | | ts | com.asiainfo.utils.Transport | 局部变量 | 行:61 |
| | | nick | com.asiainfo.utils.String | 局部变量 | 行:65 |
| | | toList |  | 局部变量 | 行:71 |
| | | ccList |  | 局部变量 | 行:84 |
| | | formDataJsonObject |  | 局部变量 | 行:99 |
| | | emailContent | com.asiainfo.utils.String | 局部变量 | 行:101 |
| | | mp | com.asiainfo.utils.MimeMultipart | 局部变量 | 行:104 |
| | | text | com.asiainfo.utils.MimeBodyPart | 局部变量 | 行:105 |
| | | attach | com.asiainfo.utils.MimeBodyPart | 局部变量 | 行:109 |
| | | imageOutputStreamList |  | 局部变量 | 行:113 |
| | | imageList |  | 局部变量 | 行:115 |
| | | sb | com.asiainfo.utils.StringBuilder | 局部变量 | 行:117 |
| | | i |  | 局部变量 | 行:118 |
| | | image | com.asiainfo.utils.MimeBodyPart | 局部变量 | 行:120 |
| | | imageDataSource | javax.mail.util.ByteArrayDataSource | 局部变量 | 行:121 |
| | | imageDh | javax.activation.DataHandler | 局部变量 | 行:124 |
| | | mmTextImage | com.asiainfo.utils.MimeMultipart | 局部变量 | 行:141 |
| | | textImage | com.asiainfo.utils.MimeBodyPart | 局部变量 | 行:150 |
| | | attach | com.asiainfo.utils.MimeBodyPart | 局部变量 | 行:158 |
| | | invalidAddresses |  | 局部变量 | 行:175 |
| | | validUnsentAddresses |  | 局部变量 | 行:178 |
| | getAttach | | | | D:\8\src\main\java\com\asiainfo\utils\MailUtil.java:方法:198 |
| | | attach | com.asiainfo.utils.MimeBodyPart | 局部变量 | 行:199 |
| | | rawData | javax.mail.util.ByteArrayDataSource | 局部变量 | 行:200 |
| | | dh | javax.activation.DataHandler | 局部变量 | 行:201 |
| | getEmailBean | | | | D:\8\src\main\java\com\asiainfo\utils\MailUtil.java:方法:207 |
| | | prop | com.asiainfo.utils.Properties | 局部变量 | 行:209 |
| | | session | com.asiainfo.utils.Session | 局部变量 | 行:214 |
| | | ts | com.asiainfo.utils.Transport | 局部变量 | 行:215 |
| | | host | com.asiainfo.utils.String | 局部变量 | 行:218 |
| | | username | com.asiainfo.utils.String | 局部变量 | 行:220 |
| | | password | com.asiainfo.utils.String | 局部变量 | 行:222 |
| | | mailConfig | com.asiainfo.utils.MailConfig | 局部变量 | 行:241 |
| | getEmailConfig | | | | D:\8\src\main\java\com\asiainfo\utils\MailUtil.java:方法:249 |
| | | map |  | 局部变量 | 行:250 |
| | replace | | | | D:\8\src\main\java\com\asiainfo\utils\MailUtil.java:方法:301 |
| | | sb | com.asiainfo.utils.StringBuffer | 局部变量 | 行:302 |
| | | m | java.util.regex.Matcher | 局部变量 | 行:304 |
| | | param | com.asiainfo.utils.String | 局部变量 | 行:306 |
| | | value | com.asiainfo.utils.Object | 局部变量 | 行:307 |
| | | MACRO_PATTERN | java.util.regex.Pattern | 类字段 | 行:25 |
| com.asiainfo.utils.PdfUtil | pdf2png | | | | D:\8\src\main\java\com\asiainfo\utils\PdfUtil.java:20 / 方法:33 |
| | | file | java.io.File | 局部变量 | 行:35 |
| | | doc | org.apache.pdfbox.pdmodel.PDDocument | 局部变量 | 行:37 |
| | | renderer | org.apache.pdfbox.rendering.PDFRenderer | 局部变量 | 行:38 |
| | | pageCount |  | 局部变量 | 行:39 |
| | | i |  | 局部变量 | 行:40 |
| | | image | java.awt.image.BufferedImage | 局部变量 | 行:41 |
| | pdf2png | | | | D:\8\src\main\java\com\asiainfo\utils\PdfUtil.java:方法:55 |
| | | doc | org.apache.pdfbox.pdmodel.PDDocument | 局部变量 | 行:58 |
| | | renderer | org.apache.pdfbox.rendering.PDFRenderer | 局部变量 | 行:59 |
| | | pageCount |  | 局部变量 | 行:60 |
| | | imageList |  | 局部变量 | 行:61 |
| | | currentSize |  | 局部变量 | 行:62 |
| | | i |  | 局部变量 | 行:63 |
| | | image | java.awt.image.BufferedImage | 局部变量 | 行:64 |
| | | outStream | java.io.ByteArrayOutputStream | 局部变量 | 行:66 |
| | | MAX_PIC_SIZE_BYTES | com.asiainfo.utils.Integer | 类字段 | 行:24 |
| com.asiainfo.utils.TimestampUtils | timestampToDateTimeString | | | | D:\8\src\main\java\com\asiainfo\utils\TimestampUtils.java:7 / 方法:17 |
| | | sdf |  | 局部变量 | 行:18 |
| | timestampToDateTimeString2 | | | | D:\8\src\main\java\com\asiainfo\utils\TimestampUtils.java:方法:22 |
| | timestampToDateTimeString | | | | D:\8\src\main\java\com\asiainfo\utils\TimestampUtils.java:方法:26 |
| | | sdf |  | 局部变量 | 行:27 |
| | dateTimeStringToTimestamp | | | | D:\8\src\main\java\com\asiainfo\utils\TimestampUtils.java:方法:31 |
| | dateTimeStringToDate | | | | D:\8\src\main\java\com\asiainfo\utils\TimestampUtils.java:方法:35 |
| | | sdf |  | 局部变量 | 行:36 |
| | dateTimeStringToDate | | | | D:\8\src\main\java\com\asiainfo\utils\TimestampUtils.java:方法:40 |
| | | sdf |  | 局部变量 | 行:41 |
| | dateToTimestamp | | | | D:\8\src\main\java\com\asiainfo\utils\TimestampUtils.java:方法:45 |
| | | dateTimePattern | com.asiainfo.utils.String | 类字段 | 行:9 |
| | | dateTimePattern2 | com.asiainfo.utils.String | 类字段 | 行:10 |
| | | DATE_PATTERN | com.asiainfo.utils.String | 类字段 | 行:11 |
| | | DATE_TIME_PATTERN | com.asiainfo.utils.String | 类字段 | 行:12 |
| com.asiainfo.utils.XMLFilesUtils | collectXMLFiles | | | | D:\8\src\main\java\com\asiainfo\utils\XMLFilesUtils.java:9 / 方法:11 |
| | | files |  | 局部变量 | 行:12 |
| | getStringFromXmlElement | | | | D:\8\src\main\java\com\asiainfo\utils\XMLFilesUtils.java:方法:30 |
| | | tagValue | com.asiainfo.utils.String | 局部变量 | 行:31 |
| | | numberElement | org.w3c.dom.Element | 局部变量 | 行:32 |
| com.asiainfo.verify.ExtractCharacters | main | | | | D:\8\src\main\java\com\asiainfo\verify\ExtractCharacters.java:5 / 方法:6 |
| | | input | com.asiainfo.verify.String | 局部变量 | 行:8 |
| | | pattern | com.asiainfo.verify.Pattern | 局部变量 | 行:13 |
| | | matcher | com.asiainfo.verify.Matcher | 局部变量 | 行:22 |
| | | extractedCharacters | com.asiainfo.verify.String | 局部变量 | 行:25 |
| com.asiainfo.verify.ExtractContent | main | | | | D:\8\src\main\java\com\asiainfo\verify\ExtractContent.java:5 / 方法:6 |
| | | input1 | com.asiainfo.verify.String | 局部变量 | 行:8 |
| | | input2 | com.asiainfo.verify.String | 局部变量 | 行:9 |
| | | pattern | com.asiainfo.verify.Pattern | 局部变量 | 行:12 |
| | | matcher1 | com.asiainfo.verify.Matcher | 局部变量 | 行:13 |
| | | matcher2 | com.asiainfo.verify.Matcher | 局部变量 | 行:14 |
| | | extractedCharacters | com.asiainfo.verify.String | 局部变量 | 行:17 |
| | | extractedCharacters | com.asiainfo.verify.String | 局部变量 | 行:23 |
| com.asiainfo.verify.RemoveSpecialCharacters | removeCharacters | | | | D:\8\src\main\java\com\asiainfo\verify\RemoveSpecialCharacters.java:3 / 方法:4 |
| | main | | | | D:\8\src\main\java\com\asiainfo\verify\RemoveSpecialCharacters.java:方法:9 |
| | | input | com.asiainfo.verify.String | 局部变量 | 行:10 |
| | | result | com.asiainfo.verify.String | 局部变量 | 行:11 |
| com.asiainfo.verify.SendEmail | main | | | | D:\8\src\main\java\com\asiainfo\verify\SendEmail.java:10 / 方法:12 |
| | | mailParam | com.asiainfo.utils.MailParam | 局部变量 | 行:14 |
| | | emailTo |  | 局部变量 | 行:16 |
| | | content1 | com.asiainfo.verify.String | 局部变量 | 行:31 |
| | | content2 | com.asiainfo.verify.String | 局部变量 | 行:37 |
| com.asiainfo.verify.SendEmail2 | main | | | | D:\8\src\main\java\com\asiainfo\verify\SendEmail2.java:15 / 方法:17 |
| | | mailParam | com.asiainfo.utils.MailParam | 局部变量 | 行:19 |
| | | emailTo |  | 局部变量 | 行:21 |
| | | alertContentTemplateConnection | com.asiainfo.cvd.model.AlertContentTemplateConnection | 局部变量 | 行:29 |
| | | alertContentSectionList |  | 局部变量 | 行:33 |
| | | alertContentTemplate1 | com.asiainfo.cvd.model.AlertContentTemplate | 局部变量 | 行:35 |
| | | alertContentTemplate2 | com.asiainfo.cvd.model.AlertContentTemplate | 局部变量 | 行:43 |
| | getAlertContentSectionList | | | | D:\8\src\main\java\com\asiainfo\verify\SendEmail2.java:方法:58 |
| | | alertContentSectionList |  | 局部变量 | 行:60 |
| | | alertContentSection1 | com.asiainfo.cvd.model.AlertContentSection | 局部变量 | 行:62 |
| | | alertContentSection2 | com.asiainfo.cvd.model.AlertContentSection | 局部变量 | 行:67 |
