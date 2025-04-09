package com.example.android_app.network;

import android.util.Log;

import com.example.android_app.models.User;

import org.json.JSONArray;
import org.json.JSONObject;
import java.util.ArrayList;
import java.util.List;

public class UserRequests extends ApiRequest {
    private static final String TAG = "UserRequests";

    public static List<User> parseUsersList(String response) {
        List<User> users = new ArrayList<>();
        try {
            JSONArray jsonArray = new JSONArray(response);
            for (int i = 0; i < jsonArray.length(); i++) {
                JSONObject json = jsonArray.getJSONObject(i);
                User user = new User(
                        json.getInt("id"),
                        json.getString("username"),
                        json.getString("email"),
                        json.getString("created_at")
                );
                users.add(user);
            }
        } catch (Exception e) {
            Log.e(TAG, "Error parsing users list", e);
        }
        return users;
    }

    public static User parseUser(String response) {
        try {
            JSONObject json = new JSONObject(response);
            return new User(
                    json.getInt("id"),
                    json.getString("username"),
                    json.getString("email"),
                    json.getString("created_at")
            );
        } catch (Exception e) {
            Log.e(TAG, "Error parsing user data", e);
            return null;
        }
    }
}