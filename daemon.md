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