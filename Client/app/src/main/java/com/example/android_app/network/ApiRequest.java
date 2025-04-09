package com.example.android_app.network;

import android.content.Context;
import android.util.Log;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONException;
import org.json.JSONObject;

import okhttp3.*;

import java.io.IOException;

public abstract class ApiRequest {
    private static final String TAG = "ApiRequest";
    private static final MediaType JSON_MEDIA_TYPE = MediaType.parse("application/json; charset=utf-8");
    private static final OkHttpClient client = new OkHttpClient();

    public interface ResponseCallback {
        void onResponse(boolean success, String message, String response);
    }

    protected static void sendRequest(Context context, String url, String json, String method, ResponseCallback callback) {
        RequestBody body = json != null ? RequestBody.create(json, JSON_MEDIA_TYPE) : null;
        Request.Builder requestBuilder = new Request.Builder().url(url);

        switch (method.toUpperCase()) {
            case "POST":
                if (body != null) requestBuilder.post(body);
                break;
            case "PUT":
                if (body != null) requestBuilder.put(body);
                break;
            case "DELETE":
                requestBuilder.delete();
                break;
            default:
                requestBuilder.get();
                break;
        }

        Request request = requestBuilder.build();

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(@NonNull Call call, @NonNull IOException e) {
                handleError(context, "Connection error: " + e.getMessage(), callback);
            }

            @Override
            public void onResponse(@NonNull Call call, @NonNull Response response) throws IOException {
                String responseBody = response.body() != null ? response.body().string() : "";
                if (response.isSuccessful()) {
                    handleSuccess(context, responseBody, callback);
                } else {
                    parseErrorResponse(context, responseBody, callback);
                }
            }
        });
    }

    private static void handleSuccess(Context context, String responseBody, ResponseCallback callback) {
        String message = "Operation successful";
        try {
            JSONObject json = new JSONObject(responseBody);
            if (json.has("message")) {
                message = json.getString("message");
            }
        } catch (JSONException e) {
            Log.e(TAG, "Error parsing success response", e);
        }
        showToast(context, message, false);
        callback.onResponse(true, message, responseBody);
    }

    private static void parseErrorResponse(Context context, String responseBody, ResponseCallback callback) {
        String errorMessage = "Request failed";
        try {
            JSONObject json = new JSONObject(responseBody);
            if (json.has("error")) {
                errorMessage = json.getString("error");
            } else if (json.has("message")) {
                errorMessage = json.getString("message");
            }
        } catch (JSONException e) {
            Log.e(TAG, "Error parsing error response", e);
        }
        handleError(context, errorMessage, callback);
    }

    private static void handleError(Context context, String message, ResponseCallback callback) {
//        showToast(context, message, true);
        callback.onResponse(false, message, null);
    }

    private static void showToast(Context context, String message, boolean isError) {
        if (context instanceof AppCompatActivity) {
            ((AppCompatActivity) context).runOnUiThread(() -> {
                Toast.makeText(context, message, Toast.LENGTH_LONG).show();
            });
        }
    }
}