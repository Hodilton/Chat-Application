package com.example.android_app.models;

import android.util.Log;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import com.example.android_app.utils.HashPassword;

import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;
import java.util.List;

public class User {
    private static final String TAG = User.class.getSimpleName();

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

    public static JSONObject toJson(String email,
                                     String password,
                                     String username)
            throws JSONException, NoSuchAlgorithmException {
        JSONObject json = new JSONObject();
        json.put("email", email);
        json.put("password", HashPassword.hash(password));
        if (username != null) json.put("username", username);
        return json;
    }

    public JSONObject toJson()
            throws JSONException {
        JSONObject json = new JSONObject();
        json.put("id", id);
        json.put("email", email);
        json.put("username", username);
        if (username != null) json.put("username", username);
        return json;
    }

    public static User fromJson(JSONObject json) {
        try {
            return new User(
                    json.getInt("id"),
                    json.getString("username"),
                    json.getString("email")
            );
        } catch (Exception e) {
            Log.e(TAG, "Error parsing user json", e);
            return null;
        }
    }

    public static User fromJson(String jsonString) {
        try {
            JSONObject json = new JSONObject(jsonString);
            return fromJson(json);
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
                users.add(fromJson(jsonArray.getJSONObject(i)));
            }
        } catch (Exception e) {
            Log.e(TAG, "Error parsing users list", e);
        }
        return users;
    }
}