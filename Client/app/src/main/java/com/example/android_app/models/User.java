package com.example.android_app.models;

public class User {
    private int id;
    private String username;
    private String email;
    private String createdAt;

    public User(int id, String username, String email, String createdAt) {
        this.id = id;
        this.username = username;
        this.email = email;
        this.createdAt = createdAt;
    }

    public int getId() { return id; }
    public String getUsername() { return username; }
    public String getEmail() { return email; }
    public String getCreatedAt() { return createdAt; }
}