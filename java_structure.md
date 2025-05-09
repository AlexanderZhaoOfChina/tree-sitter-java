# Java项目结构分析

| 类 | 方法 | 变量名 | 变量类型 | 变量位置 |
|---|------|-------|--------|--------|
| com.asiainfo.cvd.daemon.CNVDDirectoryWatcherDaemon | main | | | |
| | | task | com.asiainfo.cvd.daemon.TimerTask | 局部变量 |
| | | startTime |  | 局部变量 |
| | | timer | com.asiainfo.cvd.daemon.Timer | 局部变量 |
| | isFileProcessed | | | |
| | | statusFile | com.asiainfo.cvd.daemon.File | 局部变量 |
| | | processStatus |  | 局部变量 |
| | markFileStatus | | | |
| | | statusFile | com.asiainfo.cvd.daemon.File | 局部变量 |
| | | processStatus |  | 局部变量 |
| | scanDirectory | | | |
| | | directory | com.asiainfo.cvd.daemon.File | 局部变量 |
| | | xmlFiles |  | 局部变量 |
| | | startTime |  | 局部变量 |
| | processXmlFile | | | |
| | | sourceFileNameWithoutSuffix | com.asiainfo.cvd.daemon.String | 局部变量 |
| | | dbf | javax.xml.parsers.DocumentBuilderFactory | 局部变量 |
| | | db | javax.xml.parsers.DocumentBuilder | 局部变量 |
| | | doc | org.w3c.dom.Document | 局部变量 |
| | | vulnerabilities |  | 局部变量 |
| | | cves |  | 局部变量 |
| | | products |  | 局部变量 |
| | | vulnerabilitiesNodeList | org.w3c.dom.NodeList | 局部变量 |
| | | i |  | 局部变量 |
| | | vulnerability | org.w3c.dom.Element | 局部变量 |
| | | number | com.asiainfo.cvd.daemon.String | 局部变量 |
| | | title | com.asiainfo.cvd.daemon.String | 局部变量 |
| | | serverity | com.asiainfo.cvd.daemon.String | 局部变量 |
| | | isEvent | com.asiainfo.cvd.daemon.String | 局部变量 |
| | | submitTime | com.asiainfo.cvd.daemon.String | 局部变量 |
| | | openTime | com.asiainfo.cvd.daemon.String | 局部变量 |
| | | referenceLink | com.asiainfo.cvd.daemon.String | 局部变量 |
| | | formalWay | com.asiainfo.cvd.daemon.String | 局部变量 |
| | | description | com.asiainfo.cvd.daemon.String | 局部变量 |
| | | patchName | com.asiainfo.cvd.daemon.String | 局部变量 |
| | | patchDescription | com.asiainfo.cvd.daemon.String | 局部变量 |
| | | boVulnerability | com.asiainfo.cvd.daemon.BoVulnerability | 局部变量 |
| | | cvesNodeList | org.w3c.dom.NodeList | 局部变量 |
| | | j |  | 局部变量 |
| | | cve | org.w3c.dom.Element | 局部变量 |
| | | cveNumber | com.asiainfo.cvd.daemon.String | 局部变量 |
| | | cveUrl | com.asiainfo.cvd.daemon.String | 局部变量 |
| | | boVulnerabilityCve | com.asiainfo.cvd.daemon.BoVulnerabilityCve | 局部变量 |
| | | productsNodeList | org.w3c.dom.NodeList | 局部变量 |
| | | k |  | 局部变量 |
| | | product | org.w3c.dom.Element | 局部变量 |
| | | name | com.asiainfo.cvd.daemon.String | 局部变量 |
| | | boVulnerabilityProduct | com.asiainfo.cvd.daemon.BoVulnerabilityProduct | 局部变量 |
| | | alertBrief | com.asiainfo.cvd.daemon.VulnerabilityAlertBrief | 局部变量 |
| | | alertList |  | 局部变量 |
| | | components |  | 局部变量 |
| | | filterNames |  | 局部变量 |
| | | boVulnerabilityProductList2 |  | 局部变量 |
| | | boVulnerability | com.asiainfo.cvd.daemon.BoVulnerability | 局部变量 |
| | | vulnerabilityAlert | com.asiainfo.cvd.daemon.VulnerabilityAlert | 局部变量 |
| | | startTime |  | 局部变量 |
| | backupXMLFileForException | | | |
| | | sourceDirectory | com.asiainfo.cvd.daemon.String | 局部变量 |
| | | sourceFileName | com.asiainfo.cvd.daemon.String | 局部变量 |
| | | sourcePath | com.asiainfo.cvd.daemon.String | 局部变量 |
| | | backupDirectory | com.asiainfo.cvd.daemon.String | 局部变量 |
| | | backupPath | com.asiainfo.cvd.daemon.String | 局部变量 |
| | backupXMLFile | | | |
| | | backupStartTime |  | 局部变量 |
| | | sourceDirectory | com.asiainfo.cvd.daemon.String | 局部变量 |
| | | sourceFileName | com.asiainfo.cvd.daemon.String | 局部变量 |
| | | sourcePath | com.asiainfo.cvd.daemon.String | 局部变量 |
| | | backupDirectory | com.asiainfo.cvd.daemon.String | 局部变量 |
| | | backupPath | com.asiainfo.cvd.daemon.String | 局部变量 |
| | | backupEndTime |  | 局部变量 |
| | createDirectory | | | |
| | | file | com.asiainfo.cvd.daemon.File | 局部变量 |
| | | logger | org.slf4j.Logger | 类字段 |
| | | BASE_DIR | com.asiainfo.cvd.daemon.String | 类字段 |
| | | DIRECTORY_PATH | com.asiainfo.cvd.daemon.String | 类字段 |
| | | DATA_STORE_PATH | com.asiainfo.cvd.daemon.String | 类字段 |
| | | PROCESS_STATUS_FILE | com.asiainfo.cvd.daemon.String | 类字段 |
| | | objectMapper | com.fasterxml.jackson.databind.ObjectMapper | 类字段 |
| | | SCAN_INTERVAL |  | 类字段 |
| | | componentService | com.asiainfo.cvd.service.ComponentService | 类字段 |
| | | vulnerabilityService | com.asiainfo.cvd.service.VulnerabilityService | 类字段 |
| com.asiainfo.cvd.daemon.DataCleanupProcessor | cleanupDataStore | | | |
| | | dataStorePath | com.asiainfo.cvd.daemon.Path | 局部变量 |
| | deleteProcessStatus | | | |
| | | processStatusPath | com.asiainfo.cvd.daemon.Path | 局部变量 |
| | moveBackupFile | | | |
| | | sourcePath | com.asiainfo.cvd.daemon.Path | 局部变量 |
| | | targetPath | com.asiainfo.cvd.daemon.Path | 局部变量 |
| | moveBackupExceptionFile | | | |
| | | sourcePath | com.asiainfo.cvd.daemon.Path | 局部变量 |
| | | targetPath | com.asiainfo.cvd.daemon.Path | 局部变量 |
| | performFullCleanup | | | |
| | main | | | |
| | | logger | org.slf4j.Logger | 类字段 |
| com.asiainfo.cvd.daemon.EmailListBuilder | initializeIfNeeded | | | |
| | isTestMode | | | |
| | parseEmailList | | | |
| | getExpertEmails | | | |
| | | testEmails |  | 局部变量 |
| | | expertList | com.asiainfo.cvd.daemon.String | 局部变量 |
| | | expertEmails |  | 局部变量 |
| | getCcEmails | | | |
| | | ccList | com.asiainfo.cvd.daemon.String | 局部变量 |
| | | ccEmails |  | 局部变量 |
| | | logger | org.slf4j.Logger | 类字段 |
| | | properties | java.util.Properties | 类字段 |
| | | initialized |  | 类字段 |
| com.asiainfo.cvd.daemon.NotificationEmailProcessor | process | | | |
| | | mailParam | com.asiainfo.utils.MailParam | 局部变量 |
| | | alertContentTemplateConnection | com.asiainfo.cvd.daemon.AlertContentTemplateConnection | 局部变量 |
| | | overview | com.asiainfo.cvd.daemon.StringBuilder | 局部变量 |
| | | componentDescription | com.asiainfo.cvd.daemon.String | 局部变量 |
| | | alertContentSectionList |  | 局部变量 |
| | | alertContentTemplate | com.asiainfo.cvd.daemon.AlertContentTemplate | 局部变量 |
| | isEmailSendEnabled | | | |
| | | properties | java.util.Properties | 局部变量 |
| | getAlertContentSectionList | | | |
| | | alertContentSectionList |  | 局部变量 |
| | | alertContentSection0 | com.asiainfo.cvd.daemon.AlertContentSection | 局部变量 |
| | | alertContentSection1 | com.asiainfo.cvd.daemon.AlertContentSection | 局部变量 |
| | | alertContentSection2 | com.asiainfo.cvd.daemon.AlertContentSection | 局部变量 |
| | | alertContentSection3 | com.asiainfo.cvd.daemon.AlertContentSection | 局部变量 |
| | | alertContentSection4 | com.asiainfo.cvd.daemon.AlertContentSection | 局部变量 |
| | | alertContentSection5 | com.asiainfo.cvd.daemon.AlertContentSection | 局部变量 |
| | | logger | org.apache.logging.log4j.Logger | 类字段 |
| com.asiainfo.cvd.model.AlertContentSection | getData | | | |
| | getData2 | | | |
| | getData1 | | | |
| | | newline | com.asiainfo.cvd.model.String | 局部变量 |
| | | sectionName | com.asiainfo.cvd.model.String | 类字段 |
| | | sectionDescription | com.asiainfo.cvd.model.String | 类字段 |
| com.asiainfo.cvd.model.AlertContentTemplate | getData | | | |
| | | content | com.asiainfo.cvd.model.StringBuilder | 局部变量 |
| | addVulnerabilityDesc | | | |
| | addVulnerabilityNumber | | | |
| | addVulnerabilitySeverity | | | |
| | addVulnerabilityaffectedVersion | | | |
| | addVulnerabilityRemediationAdvice | | | |
| | | title | com.asiainfo.cvd.model.String | 类字段 |
| | | subTitle | com.asiainfo.cvd.model.String | 类字段 |
| | | alertContentSectionList |  | 类字段 |
| com.asiainfo.cvd.model.AlertContentTemplateConnection | addAlertContentTemplate | | | |
| | getData | | | |
| | | content | com.asiainfo.cvd.model.StringBuilder | 局部变量 |
| | | recipient | com.asiainfo.cvd.model.String | 类字段 |
| | | brief | com.asiainfo.cvd.model.String | 类字段 |
| | | overview | com.asiainfo.cvd.model.String | 类字段 |
| | | alertContentTemplateList |  | 类字段 |
| | | endingFragment | com.asiainfo.cvd.model.String | 类字段 |
| com.asiainfo.cvd.model.BoComponent | | id | com.asiainfo.cvd.model.Long | 类字段 |
| | | componentName | com.asiainfo.cvd.model.String | 类字段 |
| | | componentDescribe | com.asiainfo.cvd.model.String | 类字段 |
| | | useCount | com.asiainfo.cvd.model.Long | 类字段 |
| | | useCountExcludeBss | com.asiainfo.cvd.model.Long | 类字段 |
| | | belongDirectoryName | com.asiainfo.cvd.model.String | 类字段 |
| | | belongDirectoryId | com.asiainfo.cvd.model.Long | 类字段 |
| | | officialLink | com.asiainfo.cvd.model.String | 类字段 |
| | | sourceCodeLink | com.asiainfo.cvd.model.String | 类字段 |
| | | lastVersion | com.asiainfo.cvd.model.String | 类字段 |
| | | lastModifiedDate | java.time.LocalDateTime | 类字段 |
| | | licenseType | com.asiainfo.cvd.model.String | 类字段 |
| | | vendor | com.asiainfo.cvd.model.String | 类字段 |
| | | vendorCountry | com.asiainfo.cvd.model.String | 类字段 |
| | | cveProductName | com.asiainfo.cvd.model.String | 类字段 |
| | | riskType | com.asiainfo.cvd.model.String | 类字段 |
| | | influenceType | com.asiainfo.cvd.model.String | 类字段 |
| | | replaceSolution | com.asiainfo.cvd.model.String | 类字段 |
| | | componentVersion | com.asiainfo.cvd.model.String | 类字段 |
| | | componentStatus | com.asiainfo.cvd.model.String | 类字段 |
| com.asiainfo.cvd.model.BoVulnerability | | id | com.asiainfo.cvd.model.Long | 类字段 |
| | | fileName | com.asiainfo.cvd.model.String | 类字段 |
| | | number | com.asiainfo.cvd.model.String | 类字段 |
| | | title | com.asiainfo.cvd.model.String | 类字段 |
| | | serverity | com.asiainfo.cvd.model.String | 类字段 |
| | | isEvent | com.asiainfo.cvd.model.String | 类字段 |
| | | submitTime | com.asiainfo.cvd.model.String | 类字段 |
| | | openTime | com.asiainfo.cvd.model.String | 类字段 |
| | | referenceLink | com.asiainfo.cvd.model.String | 类字段 |
| | | formalWay | com.asiainfo.cvd.model.String | 类字段 |
| | | description | com.asiainfo.cvd.model.String | 类字段 |
| | | patchName | com.asiainfo.cvd.model.String | 类字段 |
| | | patchDescription | com.asiainfo.cvd.model.String | 类字段 |
| com.asiainfo.cvd.model.BoVulnerabilityCve | | id | com.asiainfo.cvd.model.Long | 类字段 |
| | | fileName | com.asiainfo.cvd.model.String | 类字段 |
| | | cnvdNumber | com.asiainfo.cvd.model.String | 类字段 |
| | | cveNumber | com.asiainfo.cvd.model.String | 类字段 |
| | | cveUrl | com.asiainfo.cvd.model.String | 类字段 |
| com.asiainfo.cvd.model.BoVulnerabilityProduct | | id | com.asiainfo.cvd.model.Long | 类字段 |
| | | fileName | com.asiainfo.cvd.model.String | 类字段 |
| | | cnvdNumber | com.asiainfo.cvd.model.String | 类字段 |
| | | product | com.asiainfo.cvd.model.String | 类字段 |
| com.asiainfo.cvd.model.Counter | increment | | | |
| | getCount | | | |
| | getRawCount | | | |
| | addZero | | | |
| | | numberString | com.asiainfo.cvd.model.String | 局部变量 |
| | | count |  | 类字段 |
| com.asiainfo.cvd.model.VulnerabilityAlert | | sourceFileNameWithoutSuffix | com.asiainfo.cvd.model.String | 类字段 |
| | | component | com.asiainfo.cvd.model.String | 类字段 |
| | | cnvdNumber | com.asiainfo.cvd.model.String | 类字段 |
| | | cveNumber | com.asiainfo.cvd.model.String | 类字段 |
| | | title | com.asiainfo.cvd.model.String | 类字段 |
| | | description | com.asiainfo.cvd.model.String | 类字段 |
| | | Severity | com.asiainfo.cvd.model.String | 类字段 |
| | | openTime | com.asiainfo.cvd.model.String | 类字段 |
| | | affectedVersion | com.asiainfo.cvd.model.String | 类字段 |
| | | remediationAdvice | com.asiainfo.cvd.model.String | 类字段 |
| com.asiainfo.cvd.model.VulnerabilityAlertBrief | appendComponent | | | |
| | getData | | | |
| | | brief | com.asiainfo.cvd.model.StringBuilder | 局部变量 |
| | | issuingOrganization | com.asiainfo.cvd.model.String | 类字段 |
| | | reportingCycle | com.asiainfo.cvd.model.String | 类字段 |
| | | componentScope |  | 类字段 |
| | | dataSources | com.asiainfo.cvd.model.String | 类字段 |
| | | CNVD_AND_CVE | com.asiainfo.cvd.model.String | 类字段 |
| com.asiainfo.cvd.model.VulnerabilityDefinitions | | CVE_NUMBER | com.asiainfo.cvd.model.String | 类字段 |
| | | VULNERABILITY_TITLE | com.asiainfo.cvd.model.String | 类字段 |
| | | COMPONENT | com.asiainfo.cvd.model.String | 类字段 |
| | | CNVD_NUMBER | com.asiainfo.cvd.model.String | 类字段 |
| | | VULNERABILITY_DESC | com.asiainfo.cvd.model.String | 类字段 |
| | | VULNERABILITY_SEVERITY | com.asiainfo.cvd.model.String | 类字段 |
| | | AFFECTED_VERSION | com.asiainfo.cvd.model.String | 类字段 |
| | | REMEDIATION_ADVICE | com.asiainfo.cvd.model.String | 类字段 |
| com.asiainfo.cvd.service.ComponentService | readComponentsFromExcel | | | |
| | | components |  | 局部变量 |
| | | configFile | com.asiainfo.cvd.service.File | 局部变量 |
| | | sheet | com.asiainfo.cvd.service.Sheet | 局部变量 |
| | | rowIterator |  | 局部变量 |
| | | row | com.asiainfo.cvd.service.Row | 局部变量 |
| | | component | com.asiainfo.cvd.model.BoComponent | 局部变量 |
| | | dateStr | com.asiainfo.cvd.service.String | 局部变量 |
| | | dateTime | java.time.LocalDateTime | 局部变量 |
| | getStringValue | | | |
| | getIntValue | | | |
| | readComponentFilterNameList | | | |
| | | filterNames |  | 局部变量 |
| | | configFile | com.asiainfo.cvd.service.File | 局部变量 |
| | | sheet | com.asiainfo.cvd.service.Sheet | 局部变量 |
| | | rowIterator |  | 局部变量 |
| | | row | com.asiainfo.cvd.service.Row | 局部变量 |
| | | currentComponentName | com.asiainfo.cvd.service.String | 局部变量 |
| | | filterName | com.asiainfo.cvd.service.String | 局部变量 |
| | | logger | org.slf4j.Logger | 类字段 |
| | | BASE_DIR | com.asiainfo.cvd.service.String | 类字段 |
| | | COMPONENTS_CONFIG_PATH | com.asiainfo.cvd.service.String | 类字段 |
| | | COMPONENT_FILTERS_PATH | com.asiainfo.cvd.service.String | 类字段 |
| com.asiainfo.cvd.service.VulnerabilityService | saveVulnerabilityData | | | |
| | | datePath | com.asiainfo.cvd.service.String | 局部变量 |
| | | storePath | com.asiainfo.cvd.service.String | 局部变量 |
| | | vulnFile | java.io.File | 局部变量 |
| | | cveFile | java.io.File | 局部变量 |
| | | productFile | java.io.File | 局部变量 |
| | readVulnerability | | | |
| | | dateDirs |  | 局部变量 |
| | | vulnFiles |  | 局部变量 |
| | | vulnerabilities |  | 局部变量 |
| | | found |  | 局部变量 |
| | readVulnerabilityProducts | | | |
| | | datePath | com.asiainfo.cvd.service.String | 局部变量 |
| | | storePath | com.asiainfo.cvd.service.String | 局部变量 |
| | | productFile | java.io.File | 局部变量 |
| | | allProducts |  | 局部变量 |
| | eliminateDuplicate | | | |
| | | counter | com.asiainfo.cvd.service.Counter | 局部变量 |
| | | sourceFileNameWithoutSuffix | com.asiainfo.cvd.service.String | 局部变量 |
| | | component | com.asiainfo.cvd.service.String | 局部变量 |
| | | cnvdNumber | com.asiainfo.cvd.service.String | 局部变量 |
| | | cveNumber | com.asiainfo.cvd.service.String | 局部变量 |
| | | title | com.asiainfo.cvd.service.String | 局部变量 |
| | | description | com.asiainfo.cvd.service.String | 局部变量 |
| | | severity | com.asiainfo.cvd.service.String | 局部变量 |
| | | openTime | com.asiainfo.cvd.service.String | 局部变量 |
| | | affectedVersions | com.asiainfo.cvd.service.String | 局部变量 |
| | | remediationAdvice | com.asiainfo.cvd.service.String | 局部变量 |
| | vulnerabilityCveJoin | | | |
| | printBoVulnerabilityProductList | | | |
| | | counter | com.asiainfo.cvd.service.Counter | 局部变量 |
| | createDirectoryIfNotExists | | | |
| | | file | java.io.File | 局部变量 |
| | | logger | org.slf4j.Logger | 类字段 |
| | | objectMapper | com.fasterxml.jackson.databind.ObjectMapper | 类字段 |
| | | dataStorePath | com.asiainfo.cvd.service.String | 类字段 |
| com.asiainfo.utils.ConfigurationExporter | exportAllConfigurations | | | |
| | exportComponents | | | |
| | | components |  | 局部变量 |
| | | sql | com.asiainfo.utils.String | 局部变量 |
| | | component | com.asiainfo.cvd.model.BoComponent | 局部变量 |
| | | componentsFile | java.io.File | 局部变量 |
| | exportComponentFilters | | | |
| | | sql | com.asiainfo.utils.String | 局部变量 |
| | | filterMap |  | 局部变量 |
| | | componentName | com.asiainfo.utils.String | 局部变量 |
| | | filterName | com.asiainfo.utils.String | 局部变量 |
| | | componentName | com.asiainfo.utils.String | 局部变量 |
| | | filters |  | 局部变量 |
| | | filterFile | java.io.File | 局部变量 |
| | createConfigDirectory | | | |
| | | configDir | java.io.File | 局部变量 |
| | main | | | |
| | | dbUrl | com.asiainfo.utils.String | 局部变量 |
| | | dbUser | com.asiainfo.utils.String | 局部变量 |
| | | dbPassword | com.asiainfo.utils.String | 局部变量 |
| | | exporter | com.asiainfo.utils.ConfigurationExporter | 局部变量 |
| | | CONFIG_DIR | com.asiainfo.utils.String | 类字段 |
| | | objectMapper | com.fasterxml.jackson.databind.ObjectMapper | 类字段 |
| | | dbUrl | com.asiainfo.utils.String | 类字段 |
| | | dbUser | com.asiainfo.utils.String | 类字段 |
| | | dbPassword | com.asiainfo.utils.String | 类字段 |
| com.asiainfo.utils.DataExporter | exportAllToExcel | | | |
| | | timestamp | com.asiainfo.utils.String | 局部变量 |
| | | excelFileName | com.asiainfo.utils.String | 局部变量 |
| | | excelFile | java.io.File | 局部变量 |
| | | conn | com.asiainfo.utils.Connection | 局部变量 |
| | exportComponentsToSheet | | | |
| | | sheet | com.asiainfo.utils.Sheet | 局部变量 |
| | | headerStyle | com.asiainfo.utils.CellStyle | 局部变量 |
| | | headerRow | com.asiainfo.utils.Row | 局部变量 |
| | | headers |  | 局部变量 |
| | | i |  | 局部变量 |
| | | cell | com.asiainfo.utils.Cell | 局部变量 |
| | | sql | com.asiainfo.utils.String | 局部变量 |
| | | rowNum |  | 局部变量 |
| | | row | com.asiainfo.utils.Row | 局部变量 |
| | | i |  | 局部变量 |
| | exportFiltersToSheet | | | |
| | | sheet | com.asiainfo.utils.Sheet | 局部变量 |
| | | headerStyle | com.asiainfo.utils.CellStyle | 局部变量 |
| | | headerRow | com.asiainfo.utils.Row | 局部变量 |
| | | headers |  | 局部变量 |
| | | i |  | 局部变量 |
| | | cell | com.asiainfo.utils.Cell | 局部变量 |
| | | sql | com.asiainfo.utils.String | 局部变量 |
| | | rowNum |  | 局部变量 |
| | | row | com.asiainfo.utils.Row | 局部变量 |
| | | i |  | 局部变量 |
| | getStringValue | | | |
| | | value | com.asiainfo.utils.Object | 局部变量 |
| | createHeaderStyle | | | |
| | | style | com.asiainfo.utils.CellStyle | 局部变量 |
| | | font | com.asiainfo.utils.Font | 局部变量 |
| | createExportDirectory | | | |
| | | exportDir | java.io.File | 局部变量 |
| | main | | | |
| | | dbUrl | com.asiainfo.utils.String | 局部变量 |
| | | dbUser | com.asiainfo.utils.String | 局部变量 |
| | | dbPassword | com.asiainfo.utils.String | 局部变量 |
| | | exporter | com.asiainfo.utils.DataExporter | 局部变量 |
| | | EXPORT_DIR | com.asiainfo.utils.String | 类字段 |
| | | dbUrl | com.asiainfo.utils.String | 类字段 |
| | | dbUser | com.asiainfo.utils.String | 类字段 |
| | | dbPassword | com.asiainfo.utils.String | 类字段 |
| com.asiainfo.utils.ExcelTemplateGenerator | generateComponentsTemplate | | | |
| | | sheet | com.asiainfo.utils.Sheet | 局部变量 |
| | | headerRow | com.asiainfo.utils.Row | 局部变量 |
| | | headers |  | 局部变量 |
| | | headerStyle | com.asiainfo.utils.CellStyle | 局部变量 |
| | | i |  | 局部变量 |
| | | cell | com.asiainfo.utils.Cell | 局部变量 |
| | generateComponentFiltersTemplate | | | |
| | | sheet | com.asiainfo.utils.Sheet | 局部变量 |
| | | headerRow | com.asiainfo.utils.Row | 局部变量 |
| | | headers |  | 局部变量 |
| | | headerStyle | com.asiainfo.utils.CellStyle | 局部变量 |
| | | i |  | 局部变量 |
| | | cell | com.asiainfo.utils.Cell | 局部变量 |
| | createHeaderStyle | | | |
| | | style | com.asiainfo.utils.CellStyle | 局部变量 |
| | | font | com.asiainfo.utils.Font | 局部变量 |
| | main | | | |
| | | configDir | java.io.File | 局部变量 |
| com.asiainfo.utils.MailConfig | | transport | javax.mail.Transport | 类字段 |
| | | session | javax.mail.Session | 类字段 |
| | | properties | java.util.Properties | 类字段 |
| | | mimeMessage | javax.mail.internet.MimeMessage | 类字段 |
| com.asiainfo.utils.MailParam | | tos |  | 类字段 |
| | | ccs |  | 类字段 |
| | | title | com.asiainfo.utils.String | 类字段 |
| | | content | com.asiainfo.utils.String | 类字段 |
| | | attachmentName | com.asiainfo.utils.String | 类字段 |
| | | attachment |  | 类字段 |
| com.asiainfo.utils.MailUtil | sendPdfToPicture | | | |
| | sendText | | | |
| | send | | | |
| | | mailConfig | com.asiainfo.utils.MailConfig | 局部变量 |
| | | message | com.asiainfo.utils.MimeMessage | 局部变量 |
| | | ts | com.asiainfo.utils.Transport | 局部变量 |
| | | nick | com.asiainfo.utils.String | 局部变量 |
| | | toList |  | 局部变量 |
| | | ccList |  | 局部变量 |
| | | formDataJsonObject |  | 局部变量 |
| | | emailContent | com.asiainfo.utils.String | 局部变量 |
| | | mp | com.asiainfo.utils.MimeMultipart | 局部变量 |
| | | text | com.asiainfo.utils.MimeBodyPart | 局部变量 |
| | | attach | com.asiainfo.utils.MimeBodyPart | 局部变量 |
| | | imageOutputStreamList |  | 局部变量 |
| | | imageList |  | 局部变量 |
| | | sb | com.asiainfo.utils.StringBuilder | 局部变量 |
| | | i |  | 局部变量 |
| | | image | com.asiainfo.utils.MimeBodyPart | 局部变量 |
| | | imageDataSource | javax.mail.util.ByteArrayDataSource | 局部变量 |
| | | imageDh | javax.activation.DataHandler | 局部变量 |
| | | mmTextImage | com.asiainfo.utils.MimeMultipart | 局部变量 |
| | | textImage | com.asiainfo.utils.MimeBodyPart | 局部变量 |
| | | attach | com.asiainfo.utils.MimeBodyPart | 局部变量 |
| | | invalidAddresses |  | 局部变量 |
| | | validUnsentAddresses |  | 局部变量 |
| | getAttach | | | |
| | | attach | com.asiainfo.utils.MimeBodyPart | 局部变量 |
| | | rawData | javax.mail.util.ByteArrayDataSource | 局部变量 |
| | | dh | javax.activation.DataHandler | 局部变量 |
| | getEmailBean | | | |
| | | prop | com.asiainfo.utils.Properties | 局部变量 |
| | | session | com.asiainfo.utils.Session | 局部变量 |
| | | ts | com.asiainfo.utils.Transport | 局部变量 |
| | | host | com.asiainfo.utils.String | 局部变量 |
| | | username | com.asiainfo.utils.String | 局部变量 |
| | | password | com.asiainfo.utils.String | 局部变量 |
| | | mailConfig | com.asiainfo.utils.MailConfig | 局部变量 |
| | getEmailConfig | | | |
| | | map |  | 局部变量 |
| | replace | | | |
| | | sb | com.asiainfo.utils.StringBuffer | 局部变量 |
| | | m | java.util.regex.Matcher | 局部变量 |
| | | param | com.asiainfo.utils.String | 局部变量 |
| | | value | com.asiainfo.utils.Object | 局部变量 |
| | | MACRO_PATTERN | java.util.regex.Pattern | 类字段 |
| com.asiainfo.utils.PdfUtil | pdf2png | | | |
| | | file | java.io.File | 局部变量 |
| | | doc | org.apache.pdfbox.pdmodel.PDDocument | 局部变量 |
| | | renderer | org.apache.pdfbox.rendering.PDFRenderer | 局部变量 |
| | | pageCount |  | 局部变量 |
| | | i |  | 局部变量 |
| | | image | java.awt.image.BufferedImage | 局部变量 |
| | pdf2png | | | |
| | | doc | org.apache.pdfbox.pdmodel.PDDocument | 局部变量 |
| | | renderer | org.apache.pdfbox.rendering.PDFRenderer | 局部变量 |
| | | pageCount |  | 局部变量 |
| | | imageList |  | 局部变量 |
| | | currentSize |  | 局部变量 |
| | | i |  | 局部变量 |
| | | image | java.awt.image.BufferedImage | 局部变量 |
| | | outStream | java.io.ByteArrayOutputStream | 局部变量 |
| | | MAX_PIC_SIZE_BYTES | com.asiainfo.utils.Integer | 类字段 |
| com.asiainfo.utils.TimestampUtils | timestampToDateTimeString | | | |
| | | sdf |  | 局部变量 |
| | timestampToDateTimeString2 | | | |
| | timestampToDateTimeString | | | |
| | | sdf |  | 局部变量 |
| | dateTimeStringToTimestamp | | | |
| | dateTimeStringToDate | | | |
| | | sdf |  | 局部变量 |
| | dateTimeStringToDate | | | |
| | | sdf |  | 局部变量 |
| | dateToTimestamp | | | |
| | | dateTimePattern | com.asiainfo.utils.String | 类字段 |
| | | dateTimePattern2 | com.asiainfo.utils.String | 类字段 |
| | | DATE_PATTERN | com.asiainfo.utils.String | 类字段 |
| | | DATE_TIME_PATTERN | com.asiainfo.utils.String | 类字段 |
| com.asiainfo.utils.XMLFilesUtils | collectXMLFiles | | | |
| | | files |  | 局部变量 |
| | getStringFromXmlElement | | | |
| | | tagValue | com.asiainfo.utils.String | 局部变量 |
| | | numberElement | org.w3c.dom.Element | 局部变量 |
| com.asiainfo.verify.ExtractCharacters | main | | | |
| | | input | com.asiainfo.verify.String | 局部变量 |
| | | pattern | com.asiainfo.verify.Pattern | 局部变量 |
| | | matcher | com.asiainfo.verify.Matcher | 局部变量 |
| | | extractedCharacters | com.asiainfo.verify.String | 局部变量 |
| com.asiainfo.verify.ExtractContent | main | | | |
| | | input1 | com.asiainfo.verify.String | 局部变量 |
| | | input2 | com.asiainfo.verify.String | 局部变量 |
| | | pattern | com.asiainfo.verify.Pattern | 局部变量 |
| | | matcher1 | com.asiainfo.verify.Matcher | 局部变量 |
| | | matcher2 | com.asiainfo.verify.Matcher | 局部变量 |
| | | extractedCharacters | com.asiainfo.verify.String | 局部变量 |
| | | extractedCharacters | com.asiainfo.verify.String | 局部变量 |
| com.asiainfo.verify.RemoveSpecialCharacters | removeCharacters | | | |
| | main | | | |
| | | input | com.asiainfo.verify.String | 局部变量 |
| | | result | com.asiainfo.verify.String | 局部变量 |
| com.asiainfo.verify.SendEmail | main | | | |
| | | mailParam | com.asiainfo.utils.MailParam | 局部变量 |
| | | emailTo |  | 局部变量 |
| | | content1 | com.asiainfo.verify.String | 局部变量 |
| | | content2 | com.asiainfo.verify.String | 局部变量 |
| com.asiainfo.verify.SendEmail2 | main | | | |
| | | mailParam | com.asiainfo.utils.MailParam | 局部变量 |
| | | emailTo |  | 局部变量 |
| | | alertContentTemplateConnection | com.asiainfo.cvd.model.AlertContentTemplateConnection | 局部变量 |
| | | alertContentSectionList |  | 局部变量 |
| | | alertContentTemplate1 | com.asiainfo.cvd.model.AlertContentTemplate | 局部变量 |
| | | alertContentTemplate2 | com.asiainfo.cvd.model.AlertContentTemplate | 局部变量 |
| | getAlertContentSectionList | | | |
| | | alertContentSectionList |  | 局部变量 |
| | | alertContentSection1 | com.asiainfo.cvd.model.AlertContentSection | 局部变量 |
| | | alertContentSection2 | com.asiainfo.cvd.model.AlertContentSection | 局部变量 |
