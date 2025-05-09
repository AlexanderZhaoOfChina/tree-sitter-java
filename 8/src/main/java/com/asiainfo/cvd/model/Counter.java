package com.asiainfo.cvd.model;

public class Counter {

    private int count = 0;

    public Counter() {
    }

    public Counter increment() {
        count++;
        return this;
    }

    public String getCount() {
        count++;
        return String.valueOf(addZero(count));
    }

    public String getRawCount() {
        count++;
        return String.valueOf(count);
    }

    public static String addZero(int number) {
        String numberString = String.valueOf(number);

        if (number < 10) {
            numberString = "00" + number;
        }

        if (number >= 10 && number < 100) {
            numberString = "0" + number;
        }

        return numberString;
    }
}
