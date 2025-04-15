package com.example.android_app.network;

import android.content.Context;
import android.util.Log;

import com.example.android_app.models.Chat;

import org.json.JSONObject;

import java.util.List;

public class ChatRequests extends ApiRequest {
    private static final String TAG = ChatRequests.class.getSimpleName();

    public interface ChatsResponseCallback {
        void onResponse(boolean success, String message, List<Chat> chats);
    }

    public interface ChatResponseCallback {
        void onResponse(boolean success, String message, Chat chat);
    }

    public interface BasicResponseCallback {
        void onResponse(boolean success, String message);
    }

    public static void getUserChats(Context context, int userId, ChatsResponseCallback callback) {
        String url = ServerConfig.BASE_URL + "/chats?user_id=" + userId;
        try {
            sendRequest(context, url, null,"GET",
                    (success, message, response) -> runOnUiThread(context, () -> {
                        List<Chat> chats = success ? Chat.listFromJson(response) : null;
                        callback.onResponse(success, message, chats);
                    }));
        } catch (Exception e) {
            Log.e(TAG, "Get chats error", e);
            callback.onResponse(false, "Get chats request failed.", null);
        }
    }

    public static void startChat(Context context, String user1Id, String user2Id, ChatResponseCallback callback) {
        String url = ServerConfig.BASE_URL + "/chats/start";
        try {
            JSONObject json = new JSONObject();
            json.put("user1_id", user1Id);
            json.put("user2_id", user2Id);

            sendRequest(context, url, json.toString(), "POST",
                    (success, message, response) -> runOnUiThread(context, () -> {
                        Chat chat = success ? Chat.fromJson(response) : null;
                        callback.onResponse(success, message, chat);
                    }));
        } catch (Exception e) {
            Log.e(TAG, "Start chat error", e);
            callback.onResponse(false, "Start chat request failed.", null);
        }
    }

    public static void deleteChat(Context context, int chatId, BasicResponseCallback callback) {
        String url = ServerConfig.BASE_URL + "/chats/" + chatId;

        try {
            sendRequest(context, url, null, "DELETE",
                    (success, message, response) -> runOnUiThread(context, () -> {
                        callback.onResponse(success, message);
                    }));
        } catch (Exception e) {
            Log.e(TAG, "Delete chat error", e);
            callback.onResponse(false, "Delete chat request failed.");
        }
    }
}