# Java项目结构分析

| 类 | 方法 | 变量名 | 变量类型 |
|---|------|-------|--------|
| com.asiainfo.cvd.daemon.CNVDDirectoryWatcherDaemon | main | | |
| | isFileProcessed | | |
| | markFileStatus | | |
| | scanDirectory | | |
| | processXmlFile | | |
| | backupXMLFileForException | | |
| | backupXMLFile | | |
| | createDirectory | | |
| | | logger | org.slf4j.Logger |
| | | BASE_DIR | com.asiainfo.cvd.daemon.String |
| | | DIRECTORY_PATH | com.asiainfo.cvd.daemon.String |
| | | DATA_STORE_PATH | com.asiainfo.cvd.daemon.String |
| | | PROCESS_STATUS_FILE | com.asiainfo.cvd.daemon.String |
| | | objectMapper | com.fasterxml.jackson.databind.ObjectMapper |
| | | SCAN_INTERVAL |  |
| | | componentService | com.asiainfo.cvd.service.ComponentService |
| | | vulnerabilityService | com.asiainfo.cvd.service.VulnerabilityService |
| com.asiainfo.cvd.daemon.DataCleanupProcessor | cleanupDataStore | | |
| | deleteProcessStatus | | |
| | moveBackupFile | | |
| | moveBackupExceptionFile | | |
| | performFullCleanup | | |
| | main | | |
| | | logger | org.slf4j.Logger |
| com.asiainfo.cvd.daemon.EmailListBuilder | initializeIfNeeded | | |
| | isTestMode | | |
| | parseEmailList | | |
| | getExpertEmails | | |
| | getCcEmails | | |
| | | logger | org.slf4j.Logger |
| | | properties | java.util.Properties |
| | | initialized |  |
| com.asiainfo.cvd.daemon.NotificationEmailProcessor | process | | |
| | isEmailSendEnabled | | |
| | getAlertContentSectionList | | |
| | | logger | org.apache.logging.log4j.Logger |
| com.asiainfo.cvd.model.AlertContentSection | getData | | |
| | getData2 | | |
| | getData1 | | |
| | | sectionName | com.asiainfo.cvd.model.String |
| | | sectionDescription | com.asiainfo.cvd.model.String |
| com.asiainfo.cvd.model.AlertContentTemplate | getData | | |
| | addVulnerabilityDesc | | |
| | addVulnerabilityNumber | | |
| | addVulnerabilitySeverity | | |
| | addVulnerabilityaffectedVersion | | |
| | addVulnerabilityRemediationAdvice | | |
| | | title | com.asiainfo.cvd.model.String |
| | | subTitle | com.asiainfo.cvd.model.String |
| | | alertContentSectionList |  |
| com.asiainfo.cvd.model.AlertContentTemplateConnection | addAlertContentTemplate | | |
| | getData | | |
| | | recipient | com.asiainfo.cvd.model.String |
| | | brief | com.asiainfo.cvd.model.String |
| | | overview | com.asiainfo.cvd.model.String |
| | | alertContentTemplateList |  |
| | | endingFragment | com.asiainfo.cvd.model.String |
| com.asiainfo.cvd.model.BoComponent | | id | com.asiainfo.cvd.model.Long |
| | | componentName | com.asiainfo.cvd.model.String |
| | | componentDescribe | com.asiainfo.cvd.model.String |
| | | useCount | com.asiainfo.cvd.model.Long |
| | | useCountExcludeBss | com.asiainfo.cvd.model.Long |
| | | belongDirectoryName | com.asiainfo.cvd.model.String |
| | | belongDirectoryId | com.asiainfo.cvd.model.Long |
| | | officialLink | com.asiainfo.cvd.model.String |
| | | sourceCodeLink | com.asiainfo.cvd.model.String |
| | | lastVersion | com.asiainfo.cvd.model.String |
| | | lastModifiedDate | java.time.LocalDateTime |
| | | licenseType | com.asiainfo.cvd.model.String |
| | | vendor | com.asiainfo.cvd.model.String |
| | | vendorCountry | com.asiainfo.cvd.model.String |
| | | cveProductName | com.asiainfo.cvd.model.String |
| | | riskType | com.asiainfo.cvd.model.String |
| | | influenceType | com.asiainfo.cvd.model.String |
| | | replaceSolution | com.asiainfo.cvd.model.String |
| | | componentVersion | com.asiainfo.cvd.model.String |
| | | componentStatus | com.asiainfo.cvd.model.String |
| com.asiainfo.cvd.model.BoVulnerability | | id | com.asiainfo.cvd.model.Long |
| | | fileName | com.asiainfo.cvd.model.String |
| | | number | com.asiainfo.cvd.model.String |
| | | title | com.asiainfo.cvd.model.String |
| | | serverity | com.asiainfo.cvd.model.String |
| | | isEvent | com.asiainfo.cvd.model.String |
| | | submitTime | com.asiainfo.cvd.model.String |
| | | openTime | com.asiainfo.cvd.model.String |
| | | referenceLink | com.asiainfo.cvd.model.String |
| | | formalWay | com.asiainfo.cvd.model.String |
| | | description | com.asiainfo.cvd.model.String |
| | | patchName | com.asiainfo.cvd.model.String |
| | | patchDescription | com.asiainfo.cvd.model.String |
| com.asiainfo.cvd.model.BoVulnerabilityCve | | id | com.asiainfo.cvd.model.Long |
| | | fileName | com.asiainfo.cvd.model.String |
| | | cnvdNumber | com.asiainfo.cvd.model.String |
| | | cveNumber | com.asiainfo.cvd.model.String |
| | | cveUrl | com.asiainfo.cvd.model.String |
| com.asiainfo.cvd.model.BoVulnerabilityProduct | | id | com.asiainfo.cvd.model.Long |
| | | fileName | com.asiainfo.cvd.model.String |
| | | cnvdNumber | com.asiainfo.cvd.model.String |
| | | product | com.asiainfo.cvd.model.String |
| com.asiainfo.cvd.model.Counter | increment | | |
| | getCount | | |
| | getRawCount | | |
| | addZero | | |
| | | count |  |
| com.asiainfo.cvd.model.VulnerabilityAlert | | sourceFileNameWithoutSuffix | com.asiainfo.cvd.model.String |
| | | component | com.asiainfo.cvd.model.String |
| | | cnvdNumber | com.asiainfo.cvd.model.String |
| | | cveNumber | com.asiainfo.cvd.model.String |
| | | title | com.asiainfo.cvd.model.String |
| | | description | com.asiainfo.cvd.model.String |
| | | Severity | com.asiainfo.cvd.model.String |
| | | openTime | com.asiainfo.cvd.model.String |
| | | affectedVersion | com.asiainfo.cvd.model.String |
| | | remediationAdvice | com.asiainfo.cvd.model.String |
| com.asiainfo.cvd.model.VulnerabilityAlertBrief | appendComponent | | |
| | getData | | |
| | | issuingOrganization | com.asiainfo.cvd.model.String |
| | | reportingCycle | com.asiainfo.cvd.model.String |
| | | componentScope |  |
| | | dataSources | com.asiainfo.cvd.model.String |
| | | CNVD_AND_CVE | com.asiainfo.cvd.model.String |
| com.asiainfo.cvd.model.VulnerabilityDefinitions | | CVE_NUMBER | com.asiainfo.cvd.model.String |
| | | VULNERABILITY_TITLE | com.asiainfo.cvd.model.String |
| | | COMPONENT | com.asiainfo.cvd.model.String |
| | | CNVD_NUMBER | com.asiainfo.cvd.model.String |
| | | VULNERABILITY_DESC | com.asiainfo.cvd.model.String |
| | | VULNERABILITY_SEVERITY | com.asiainfo.cvd.model.String |
| | | AFFECTED_VERSION | com.asiainfo.cvd.model.String |
| | | REMEDIATION_ADVICE | com.asiainfo.cvd.model.String |
| com.asiainfo.cvd.service.ComponentService | readComponentsFromExcel | | |
| | getStringValue | | |
| | getIntValue | | |
| | readComponentFilterNameList | | |
| | | logger | org.slf4j.Logger |
| | | BASE_DIR | com.asiainfo.cvd.service.String |
| | | COMPONENTS_CONFIG_PATH | com.asiainfo.cvd.service.String |
| | | COMPONENT_FILTERS_PATH | com.asiainfo.cvd.service.String |
| com.asiainfo.cvd.service.VulnerabilityService | saveVulnerabilityData | | |
| | readVulnerability | | |
| | readVulnerabilityProducts | | |
| | eliminateDuplicate | | |
| | vulnerabilityCveJoin | | |
| | printBoVulnerabilityProductList | | |
| | createDirectoryIfNotExists | | |
| | | logger | org.slf4j.Logger |
| | | objectMapper | com.fasterxml.jackson.databind.ObjectMapper |
| | | dataStorePath | com.asiainfo.cvd.service.String |
| com.asiainfo.utils.ConfigurationExporter | exportAllConfigurations | | |
| | exportComponents | | |
| | exportComponentFilters | | |
| | createConfigDirectory | | |
| | main | | |
| | | CONFIG_DIR | com.asiainfo.utils.String |
| | | objectMapper | com.fasterxml.jackson.databind.ObjectMapper |
| | | dbUrl | com.asiainfo.utils.String |
| | | dbUser | com.asiainfo.utils.String |
| | | dbPassword | com.asiainfo.utils.String |
| com.asiainfo.utils.DataExporter | exportAllToExcel | | |
| | exportComponentsToSheet | | |
| | exportFiltersToSheet | | |
| | getStringValue | | |
| | createHeaderStyle | | |
| | createExportDirectory | | |
| | main | | |
| | | EXPORT_DIR | com.asiainfo.utils.String |
| | | dbUrl | com.asiainfo.utils.String |
| | | dbUser | com.asiainfo.utils.String |
| | | dbPassword | com.asiainfo.utils.String |
| com.asiainfo.utils.ExcelTemplateGenerator | generateComponentsTemplate | | |
| | generateComponentFiltersTemplate | | |
| | createHeaderStyle | | |
| | main | | |
| com.asiainfo.utils.MailConfig | | transport | javax.mail.Transport |
| | | session | javax.mail.Session |
| | | properties | java.util.Properties |
| | | mimeMessage | javax.mail.internet.MimeMessage |
| com.asiainfo.utils.MailParam | | tos |  |
| | | ccs |  |
| | | title | com.asiainfo.utils.String |
| | | content | com.asiainfo.utils.String |
| | | attachmentName | com.asiainfo.utils.String |
| | | attachment |  |
| com.asiainfo.utils.MailUtil | sendPdfToPicture | | |
| | sendText | | |
| | send | | |
| | getAttach | | |
| | getEmailBean | | |
| | getEmailConfig | | |
| | replace | | |
| | | MACRO_PATTERN | java.util.regex.Pattern |
| com.asiainfo.utils.PdfUtil | pdf2png | | |
| | pdf2png | | |
| | | MAX_PIC_SIZE_BYTES | com.asiainfo.utils.Integer |
| com.asiainfo.utils.TimestampUtils | timestampToDateTimeString | | |
| | timestampToDateTimeString2 | | |
| | timestampToDateTimeString | | |
| | dateTimeStringToTimestamp | | |
| | dateTimeStringToDate | | |
| | dateTimeStringToDate | | |
| | dateToTimestamp | | |
| | | dateTimePattern | com.asiainfo.utils.String |
| | | dateTimePattern2 | com.asiainfo.utils.String |
| | | DATE_PATTERN | com.asiainfo.utils.String |
| | | DATE_TIME_PATTERN | com.asiainfo.utils.String |
| com.asiainfo.utils.XMLFilesUtils | collectXMLFiles | | |
| | getStringFromXmlElement | | |
| com.asiainfo.verify.ExtractCharacters | main | | |
| com.asiainfo.verify.ExtractContent | main | | |
| com.asiainfo.verify.RemoveSpecialCharacters | removeCharacters | | |
| | main | | |
| com.asiainfo.verify.SendEmail | main | | |
| com.asiainfo.verify.SendEmail2 | main | | |
| | getAlertContentSectionList | | |
