package com.example.android_app.network;

import android.content.Context;
import android.util.Log;
import org.json.JSONObject;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class AuthRequests extends ApiRequest {
    private static final String TAG = "AuthRequests";

    public static void login(Context context, String email, String password, ResponseCallback callback) {
        String url = ServerConfig.BASE_URL + "/login";
        try {
            JSONObject json = new JSONObject();
            json.put("email", email);
            json.put("password", hashPassword(password));

            sendRequest(context, url, json.toString(), "POST", callback);
        } catch (Exception e) {
            Log.e(TAG, "Login error", e);
            callback.onResponse(false, "Login request creation failed.", null);
        }
    }

    public static void register(Context context, String username, String email, String password, ResponseCallback callback) {
        String url = ServerConfig.BASE_URL + "/register";
        try {
            JSONObject json = new JSONObject();
            json.put("username", username);
            json.put("email", email);
            json.put("password", hashPassword(password));

            sendRequest(context, url, json.toString(), "POST", callback);
        } catch (Exception e) {
            Log.e(TAG, "Register error", e);
            callback.onResponse(false, "Registration request creation failed.", null);
        }
    }

    private static String hashPassword(String password) throws NoSuchAlgorithmException {
        MessageDigest digest = MessageDigest.getInstance("SHA-256");
        byte[] hash = digest.digest(password.getBytes(StandardCharsets.UTF_8));
        StringBuilder hexString = new StringBuilder();

        for (byte b : hash) {
            String hex = Integer.toHexString(0xff & b);
            if (hex.length() == 1) hexString.append('0');
            hexString.append(hex);
        }

        return hexString.toString();
    }
}