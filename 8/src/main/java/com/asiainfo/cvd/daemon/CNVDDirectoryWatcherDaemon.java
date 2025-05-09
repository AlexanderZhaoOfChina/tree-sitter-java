/**
 * CNVD漏洞信息监控守护进程
 * 功能：
 * 1. 监控指定目录下的XML文件
 * 2. 解析XML文件中的漏洞信息
 * 3. 将漏洞信息存储为JSON文件
 * 4. 生成漏洞预警信息并发送邮件通知
 * 5. 备份已处理的XML文件
 */
package com.asiainfo.cvd.daemon;

import com.asiainfo.cvd.model.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import java.io.*;
import java.nio.file.*;
import java.util.*;

import static com.asiainfo.utils.XMLFilesUtils.collectXMLFiles;
import static com.asiainfo.utils.XMLFilesUtils.getStringFromXmlElement;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import com.asiainfo.cvd.service.ComponentService;
import com.asiainfo.cvd.service.VulnerabilityService;

public class CNVDDirectoryWatcherDaemon {

    private static final Logger logger = LoggerFactory.getLogger(CNVDDirectoryWatcherDaemon.class);

    // 基础目录（程序运行目录）
    private static final String BASE_DIR = System.getProperty("user.dir");

    // CNVD XML文件监控目录
    private static final String DIRECTORY_PATH = Paths.get(BASE_DIR, "cnvd").toString();

    // 数据存储根目录
    private static final String DATA_STORE_PATH = Paths.get(BASE_DIR, "data_store").toString();

    // 处理状态记录文件
    private static final String PROCESS_STATUS_FILE = Paths.get(BASE_DIR, "process_status.json").toString();

    // JSON文件操作工具
    private static final ObjectMapper objectMapper = new ObjectMapper().enable(SerializationFeature.INDENT_OUTPUT);

    // 扫描间隔时间（毫秒）
    private static final long SCAN_INTERVAL = 8000;

    // 组件服务
    private static final ComponentService componentService = new ComponentService();
    private static final VulnerabilityService vulnerabilityService = new VulnerabilityService(DATA_STORE_PATH);

    /**
     * 程序入口：启动CNVD目录监控守护进程
     */
    public static void main(String[] args) {
        // 确保必要的目录存在
        createDirectory(DIRECTORY_PATH);
        createDirectory(DATA_STORE_PATH);
        createDirectory(Paths.get(BASE_DIR, "config").toString());

        logger.info("Base Directory: {}", BASE_DIR);
        logger.info("CNVD XML Directory: {}", DIRECTORY_PATH);
        logger.info("Data Directory: {}", DATA_STORE_PATH);
        logger.info("Config Directory: {}", Paths.get(BASE_DIR, "config").toString());

        TimerTask task = new TimerTask() {
            @Override
            public void run() {
                logger.info("Start Scan Directory ...");
                try {
                    long startTime = System.currentTimeMillis();
                    scanDirectory();
                    logger.info("Scan Directory execution time: {} seconds", (System.currentTimeMillis() - startTime) / 1000.0);
                } catch (Exception e) {
                    logger.error("Error in scanning directory: {}", e.getMessage(), e);
                }
            }
        };

        Timer timer = new Timer(true);
        timer.scheduleAtFixedRate(task, 0, SCAN_INTERVAL);

        logger.info("Directory watcher started. Press Ctrl+C to exit.");

        try {
            Thread.currentThread().join();
        } catch (InterruptedException e) {
            logger.error("Thread interrupted", e);
        }
    }

    /**
     * 检查文件是否已处理
     */
    private static boolean isFileProcessed(String fileName) {
        try {
            File statusFile = new File(PROCESS_STATUS_FILE);
            if (!statusFile.exists()) {
                return false;
            }
            Map<String, String> processStatus = objectMapper.readValue(statusFile,
                    objectMapper.getTypeFactory().constructMapType(Map.class, String.class, String.class));
            return processStatus.containsKey(fileName) && "PROCESSED".equals(processStatus.get(fileName));
        } catch (IOException e) {
            return false;
        }
    }

    /**
     * 标记文件处理状态
     */
    private static void markFileStatus(String fileName, String status) throws IOException {
        File statusFile = new File(PROCESS_STATUS_FILE);
        Map<String, String> processStatus;
        if (statusFile.exists()) {
            processStatus = objectMapper.readValue(statusFile,
                    objectMapper.getTypeFactory().constructMapType(Map.class, String.class, String.class));
        } else {
            processStatus = new HashMap<>();
        }
        processStatus.put(fileName, status);
        objectMapper.writeValue(statusFile, processStatus);
    }

    /**
     * 高级目录扫描方法
     */
    private static void scanDirectory() throws Exception {
        File directory = new File(DIRECTORY_PATH);
        List<File> xmlFiles = new ArrayList<>();

        if (directory.exists() && directory.isDirectory()) {
            collectXMLFiles(directory, xmlFiles);
            for (File xmlFile : xmlFiles) {
                logger.info("Start Process XML file: {} ...", xmlFile.getName());
                long startTime = System.currentTimeMillis();
                processXmlFile(xmlFile);
                logger.info("Process XML file successfully: {}, execution time: {}", xmlFile.getName(), String.format("%.2f seconds", (System.currentTimeMillis() - startTime) / 1000.0));
            }
        }
    }

    /**
     * 处理单个XML文件
     */
    private static void processXmlFile(File xmlFile) throws Exception {
        String sourceFileNameWithoutSuffix = xmlFile.getName().substring(0, xmlFile.getName().lastIndexOf("."));

        if (isFileProcessed(sourceFileNameWithoutSuffix)) {
            logger.info("File already processed: {}", xmlFile.getName());
            backupXMLFile(xmlFile);
            return;
        }

        try {
            // 解析XML文档
            DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
            DocumentBuilder db = dbf.newDocumentBuilder();
            Document doc = db.parse(xmlFile);

            List<BoVulnerability> vulnerabilities = new ArrayList<>();
            List<BoVulnerabilityCve> cves = new ArrayList<>();
            List<BoVulnerabilityProduct> products = new ArrayList<>();

            // 解析XML文档中的漏洞信息
            NodeList vulnerabilitiesNodeList = doc.getElementsByTagName("vulnerability");

            for (int i = 0; i < vulnerabilitiesNodeList.getLength(); i++) {
                Element vulnerability = (Element) vulnerabilitiesNodeList.item(i);

                // 提取漏洞基本信息
                String number = getStringFromXmlElement(vulnerability, "number");
                String title = getStringFromXmlElement(vulnerability, "title");
                String serverity = getStringFromXmlElement(vulnerability, "serverity");
                String isEvent = getStringFromXmlElement(vulnerability, "isEvent");
                String submitTime = getStringFromXmlElement(vulnerability, "submitTime");
                String openTime = getStringFromXmlElement(vulnerability, "openTime");
                String referenceLink = getStringFromXmlElement(vulnerability, "referenceLink");
                String formalWay = getStringFromXmlElement(vulnerability, "formalWay");
                String description = getStringFromXmlElement(vulnerability, "description");
                String patchName = getStringFromXmlElement(vulnerability, "patchName");
                String patchDescription = getStringFromXmlElement(vulnerability, "patchDescription");

                // 赋值BoVulnerability
                BoVulnerability boVulnerability = new BoVulnerability();
                boVulnerability.setFileName(sourceFileNameWithoutSuffix);
                boVulnerability.setNumber(number);
                boVulnerability.setTitle(title);
                boVulnerability.setServerity(serverity);
                boVulnerability.setIsEvent(isEvent);
                boVulnerability.setSubmitTime(submitTime);
                boVulnerability.setOpenTime(openTime);
                boVulnerability.setReferenceLink(referenceLink);
                boVulnerability.setFormalWay(formalWay);
                boVulnerability.setDescription(description);
                boVulnerability.setPatchName(patchName);
                boVulnerability.setPatchDescription(patchDescription);

                vulnerabilities.add(boVulnerability);

                // 提取CVE关联信息
                NodeList cvesNodeList = vulnerability.getElementsByTagName("cve");
                for (int j = 0; j < cvesNodeList.getLength(); j++) {
                    Element cve = (Element) cvesNodeList.item(j);
                    String cveNumber = getStringFromXmlElement(cve, "cveNumber");
                    String cveUrl = getStringFromXmlElement(cve, "cveUrl");

                    BoVulnerabilityCve boVulnerabilityCve = new BoVulnerabilityCve();
                    boVulnerabilityCve.setFileName(sourceFileNameWithoutSuffix);
                    boVulnerabilityCve.setCnvdNumber(number);
                    boVulnerabilityCve.setCveNumber(cveNumber);
                    boVulnerabilityCve.setCveUrl(cveUrl);
                    cves.add(boVulnerabilityCve);
                }

                // 提取受影响的产品信息
                NodeList productsNodeList = vulnerability.getElementsByTagName("product");
                for (int k = 0; k < productsNodeList.getLength(); k++) {
                    Element product = (Element) productsNodeList.item(k);
                    String name = product.getTextContent();

                    BoVulnerabilityProduct boVulnerabilityProduct = new BoVulnerabilityProduct();
                    boVulnerabilityProduct.setFileName(sourceFileNameWithoutSuffix);
                    boVulnerabilityProduct.setCnvdNumber(number);
                    boVulnerabilityProduct.setProduct(name);
                    products.add(boVulnerabilityProduct);
                }
            }

            if (vulnerabilities.isEmpty()) {
                logger.warn("No vulnerabilities found in file: {}", xmlFile.getName());
                backupXMLFileForException(xmlFile);
                return;
            }

            // 使用VulnerabilityService保存数据
            vulnerabilityService.saveVulnerabilityData(sourceFileNameWithoutSuffix, vulnerabilities, cves, products);

            // 生成预警信息
            VulnerabilityAlertBrief alertBrief = new VulnerabilityAlertBrief();
            alertBrief.setReportingCycle(sourceFileNameWithoutSuffix);

            List<VulnerabilityAlert> alertList = new ArrayList<>();
            List<BoComponent> components = componentService.readComponentsFromExcel();

            for (BoComponent component : components) {
                List<String> filterNames = componentService.readComponentFilterNameList(component.getComponentName());
                for (String filterName : filterNames) {
                    // 使用VulnerabilityService查询产品列表
                    List<BoVulnerabilityProduct> boVulnerabilityProductList2 = vulnerabilityService.readVulnerabilityProducts(sourceFileNameWithoutSuffix, filterName);

                    //vulnerabilityService.printBoVulnerabilityProductList(sourceFileNameWithoutSuffix, boVulnerabilityProductList2);

                    for (BoVulnerabilityProduct boVulnerabilityProduct : boVulnerabilityProductList2) {
                        BoVulnerability boVulnerability =
                                vulnerabilityService.readVulnerability(sourceFileNameWithoutSuffix, boVulnerabilityProduct.getCnvdNumber());

                        VulnerabilityAlert vulnerabilityAlert = new VulnerabilityAlert();
                        vulnerabilityAlert.setSourceFileNameWithoutSuffix(sourceFileNameWithoutSuffix);
                        vulnerabilityAlert.setTitle(boVulnerability.getTitle());
                        alertBrief.appendComponent(component.getComponentName());
                        vulnerabilityAlert.setComponent(component.getComponentName());
                        vulnerabilityAlert.setCnvdNumber(boVulnerability.getNumber());
                        vulnerabilityAlert.setCveNumber(vulnerabilityService.vulnerabilityCveJoin(cves, boVulnerability.getNumber()));
                        vulnerabilityAlert.setDescription(boVulnerability.getDescription());
                        vulnerabilityAlert.setSeverity(boVulnerability.getServerity());
                        vulnerabilityAlert.setOpenTime(boVulnerability.getOpenTime());
                        vulnerabilityAlert.setAffectedVersion(boVulnerabilityProduct.getProduct());
                        vulnerabilityAlert.setRemediationAdvice(boVulnerability.getFormalWay());

                        alertList.add(vulnerabilityAlert);
                    }
                }
            }

            alertList = vulnerabilityService.eliminateDuplicate(alertList);

            if (!alertList.isEmpty()) {
                logger.info("Start Process Notification Email ...");
                long startTime = System.currentTimeMillis();
                NotificationEmailProcessor.process(alertBrief, alertList);
                logger.info(String.format("Process Notification Email successfully: %.2f seconds", (System.currentTimeMillis() - startTime) / 1000.0));
            }

            logger.info("File processed successfully: {}", xmlFile.getName());

            markFileStatus(sourceFileNameWithoutSuffix, "PROCESSED");
            backupXMLFile(xmlFile);

        } catch (Exception e) {
            logger.error("Error processing file: {}", xmlFile.getName(), e);
            markFileStatus(sourceFileNameWithoutSuffix, "FAILED");
            backupXMLFileForException(xmlFile);
        }
    }

    /**
     * 将处理异常的XML文件备份到指定目录
     *
     * @param xmlFile 需要备份的XML文件
     * @throws IOException IO异常
     */
    private static void backupXMLFileForException(File xmlFile) throws IOException {
        String sourceDirectory = xmlFile.getParent();
        String sourceFileName = xmlFile.getName();
        String sourcePath = xmlFile.getAbsolutePath();
        String backupDirectory = sourceDirectory + "/backup_for_exception";
        createDirectory(backupDirectory);
        String backupPath = backupDirectory + "/" + sourceFileName;

        if (Files.exists(Path.of(sourcePath))) {
            Files.move(Path.of(sourcePath), Path.of(backupPath));
            logger.info("Backup file for exception successfully: {}", sourceFileName);
        }
    }

    /**
     * 将处理完成的XML文件备份到指定目录
     *
     * @param xmlFile 需要备份的XML文件
     * @throws IOException IO异常
     */
    private static void backupXMLFile(File xmlFile) throws IOException {
        logger.info("Start Backup XML File: {} ...", xmlFile.getName());
        long backupStartTime = System.currentTimeMillis();

        String sourceDirectory = xmlFile.getParent();
        String sourceFileName = xmlFile.getName();
        String sourcePath = xmlFile.getAbsolutePath();
        String backupDirectory = sourceDirectory + "/backup";
        createDirectory(backupDirectory);
        String backupPath = backupDirectory + "/" + sourceFileName;

        try {
            if (Files.exists(Path.of(sourcePath))) {
                Files.move(Path.of(sourcePath), Path.of(backupPath));
                logger.info("Backup XML file successfully: {}", sourceFileName);
            }
        } catch (Exception e) {
            logger.error("Backup XML file failed: {}", sourceFileName, e);
            return;
        }

        long backupEndTime = System.currentTimeMillis();
        logger.info("Backup file execution time: {} seconds", (backupEndTime - backupStartTime) / 1000.0);
    }

    /**
     * 创建目录（如果不存在）
     *
     * @param directory 目录路径
     */
    private static void createDirectory(String directory) {
        File file = new File(directory);
        if (!file.exists()) {
            file.mkdirs();
        }
    }
}