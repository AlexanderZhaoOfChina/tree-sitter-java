package com.asiainfo.utils;


/**
 * Created by Alex on 2017/3/25.
 */
public class TimestampUtils {

    private static String dateTimePattern = "yyyy-MM-dd HH:mm:ss.SSS";
    private static String dateTimePattern2 = "yyyyMMddHHmmssSSS";
    public static  String DATE_PATTERN = "yyyy-MM-dd";
    public static  String DATE_TIME_PATTERN = "yyyy-MM-dd HH:mm:ss.SSS";

    private TimestampUtils() {
    }

    public static String timestampToDateTimeString(java.sql.Timestamp timestamp) {
        java.text.DateFormat sdf = new java.text.SimpleDateFormat(dateTimePattern2);
        return sdf.format(timestamp);
    }

    public static String timestampToDateTimeString2(java.sql.Timestamp timestamp) {
        return timestampToDateTimeString(timestamp, dateTimePattern);
    }

    public static String timestampToDateTimeString(java.sql.Timestamp timestamp, String dateTimePattern) {
        java.text.DateFormat sdf = new java.text.SimpleDateFormat(dateTimePattern);
        return sdf.format(timestamp);
    }

    public static java.sql.Timestamp dateTimeStringToTimestamp(String dateTimeString) {
        return java.sql.Timestamp.valueOf(dateTimeString);
    }

    public static java.util.Date dateTimeStringToDate(String dateTimeString) throws java.text.ParseException {
        java.text.DateFormat sdf = new java.text.SimpleDateFormat(dateTimePattern2);
        return sdf.parse(dateTimeString);
    }

    public static java.util.Date dateTimeStringToDate(String dateTimeString, String dateTimePattern) throws java.text.ParseException {
        java.text.DateFormat sdf = new java.text.SimpleDateFormat(dateTimePattern);
        return sdf.parse(dateTimeString);
    }

    public static java.sql.Timestamp dateToTimestamp(java.util.Date date) {
        return new java.sql.Timestamp(date.getTime());
    }

}
