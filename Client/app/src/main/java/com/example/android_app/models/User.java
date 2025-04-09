package com.example.android_app.models;

import android.util.Log;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

public class User {
    private static final String TAG = "User";

    private int id;
    private String username;
    private String email;

    public User(int id, String username, String email) {
        this.id = id;
        this.username = username;
        this.email = email;
    }

    public int getId() { return id; }
    public String getUsername() { return username; }
    public String getEmail() { return email; }

    public static User fromJson(String jsonString) {
        try {
            JSONObject json = new JSONObject(jsonString);
            return new User(
                    json.getInt("id"),
                    json.getString("username"),
                    json.getString("email")
            );
        } catch (Exception e) {
            Log.e(TAG, "Error parsing user data", e);
            return null;
        }
    }

    public static List<User> listFromJson(String jsonString) {
        List<User> users = new ArrayList<>();
        try {
            JSONArray jsonArray = new JSONArray(jsonString);
            for (int i = 0; i < jsonArray.length(); i++) {
                users.add(fromJson(jsonArray.getJSONObject(i).toString()));
            }
        } catch (Exception e) {
            Log.e(TAG, "Error parsing users list", e);
        }
        return users;
    }
}