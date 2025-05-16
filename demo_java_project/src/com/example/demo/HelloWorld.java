package com.example.demo;

public class HelloWorld {
    private String message;

    public HelloWorld() {
        this.message = "Hello, World!";
    }

    public void sayHello() {
        System.out.println(message);
    }

    public static void main(String[] args) {
        HelloWorld hello = new HelloWorld();
        hello.sayHello();
    }
} 