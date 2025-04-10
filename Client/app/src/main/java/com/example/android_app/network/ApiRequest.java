package com.example.android_app.network;

import android.content.Context;
import android.os.Handler;
import android.os.Looper;
import android.util.Log;
import android.widget.Toast;

import androidx.annotation.NonNull;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import okhttp3.*;

import java.io.IOException;

public abstract class ApiRequest {
    private static final String TAG = ApiRequest.class.getSimpleName();
    private static final MediaType JSON_MEDIA_TYPE = MediaType.parse("application/json; charset=utf-8");
    private static final OkHttpClient client = new OkHttpClient();

    public interface ResponseCallback {
        void onResponse(boolean success, String message, String response);
    }

    protected static void sendRequest(Context context,
                                      String url,
                                      String json,
                                      String method,
                                      ResponseCallback callback) {
        RequestBody body = createRequestBody(json);
        Request request = buildRequest(url, method, body);

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

    protected static void runOnUiThread(Context context, Runnable action) {
        if (context instanceof android.app.Activity) {
            ((android.app.Activity) context).runOnUiThread(action);
        } else {
            action.run();
        }
    }

    private static RequestBody createRequestBody(String json) {
        return json != null ? RequestBody.create(json, JSON_MEDIA_TYPE) : null;
    }

    private static Request buildRequest(String url, String method, RequestBody body) {
        Request.Builder builder = new Request.Builder().url(url);

        switch (method.toUpperCase()) {
            case "POST":
                return body != null ? builder.post(body).build() : builder.build();
            case "PUT":
                return body != null ? builder.put(body).build() : builder.build();
            case "DELETE":
                return builder.delete().build();
            default:
                return builder.get().build();
        }
    }

    private static void handleSuccess(Context context, String responseBody, ResponseCallback callback) {
        String message = "Operation successful";
        try {
            try {
                JSONObject json = new JSONObject(responseBody);
                if (json.has("message")) {
                    message = json.getString("message");
                }
            } catch (JSONException e) {
                JSONArray jsonArray = new JSONArray(responseBody);
                message = "Received " + jsonArray.length() + " items";
            }
        } catch (JSONException e) {
            Log.e(TAG, "Error parsing success response", e);
        }
        showToast(context, message);
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
        handleError(context,errorMessage, callback);
    }

    private static void handleError(Context context, String message, ResponseCallback callback) {
        callback.onResponse(false, message, null);
    }

    private static void showToast(Context context, String message) {
        new Handler(Looper.getMainLooper()).post(() -> Toast.makeText(context.getApplicationContext(), message, Toast.LENGTH_LONG).show());
    }
}