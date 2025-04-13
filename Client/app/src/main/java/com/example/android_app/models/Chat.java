package com.example.android_app.models;

import android.util.Log;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

public class Chat {
    private static final String TAG = Chat.class.getSimpleName();

    private int id;
    private User otherUser;
    private String createdAt;

    public Chat(int id, User otherUser, String createdAt) {
        this.id = id;
        this.otherUser = otherUser;
        this.createdAt = createdAt;
    }

    public int getId() { return id; }
    public User getOtherUser() { return otherUser; }
    public String getCreatedAt() { return createdAt; }

    public static Chat fromJson(JSONObject json) {
        try {
            JSONObject userJson = json.getJSONObject("user");
            User user = User.fromJson(userJson);

            return new Chat(
                    json.getInt("chat_id"),
                    user,
                    json.getString("created_at")
            );
        } catch (Exception e) {
            Log.e(TAG, "Error parsing chat json", e);
            return null;
        }
    }

    public static Chat fromJson(String jsonString) {
        try {
            JSONObject json = new JSONObject(jsonString);
            return fromJson(json);
        } catch (Exception e) {
            Log.e(TAG, "Error parsing chat data", e);
            return null;
        }
    }

    public static List<Chat> listFromJson(String jsonString) {
        List<Chat> chats = new ArrayList<>();
        try {
            JSONObject root = new JSONObject(jsonString);
            JSONArray chatsArray = root.getJSONArray("chats");

            for (int i = 0; i < chatsArray.length(); i++) {
                chats.add(fromJson(chatsArray.getJSONObject(i)));
            }
        } catch (Exception e) {
            Log.e(TAG, "Error parsing chats list", e);
        }
        return chats;
    }

    public JSONObject toJson() throws JSONException {
        JSONObject json = new JSONObject();
        json.put("id", id);
        json.put("other_user", otherUser.toJson());
        json.put("created_at", createdAt);
        return json;
    }
}