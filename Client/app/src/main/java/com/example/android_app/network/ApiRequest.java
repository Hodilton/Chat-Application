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

import java.io.IOException;
import java.util.concurrent.TimeUnit;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public abstract class ApiRequest {
    private static final String TAG = ApiRequest.class.getSimpleName();
    private static final MediaType JSON_MEDIA_TYPE = MediaType.parse("application/json; charset=utf-8");
    private static final OkHttpClient client = new OkHttpClient.Builder()
            .connectTimeout(10, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .writeTimeout(15, TimeUnit.SECONDS)
            .build();

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

        Log.e(TAG, "Sending " + method + " request to: " + url);
        if (json != null) {
            Log.e(TAG, "Request body: " + json);
        }
        if (request.headers().size() > 0) {
            Log.e(TAG, "Request headers: " + request.headers());
        }

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(@NonNull Call call, @NonNull IOException e) {
                String errorMessage = "Network error: " + e.getMessage();
                Log.e(TAG, errorMessage, e);
                handleError(context, errorMessage, callback);
            }

            @Override
            public void onResponse(@NonNull Call call, @NonNull Response response) throws IOException {
                try {
                    String responseBody = response.body() != null ? response.body().string() : "";
                    Log.d(TAG, "Response from " + url + ": " + response.code() + " - " + responseBody);

                    if (response.isSuccessful()) {
                        handleSuccessResponse(context, responseBody, callback);
                    } else {
                        handleErrorResponse(context, response.code(), responseBody, callback);
                    }
                } catch (Exception e) {
                    String errorMessage = "Response parsing error: " + e.getMessage();
                    Log.e(TAG, errorMessage, e);
                    handleError(context, errorMessage, callback);
                }
            }
        });
    }

    private static RequestBody createRequestBody(String json) {
        return json != null ? RequestBody.create(json, JSON_MEDIA_TYPE) : null;
    }

    private static Request buildRequest(String url, String method, RequestBody body) {
        Request.Builder builder = new Request.Builder().url(url);

        switch (method.toUpperCase()) {
            case "POST":
                return body != null ? builder.post(body).build() : builder.post(RequestBody.create("", JSON_MEDIA_TYPE)).build();
            case "PUT":
                return body != null ? builder.put(body).build() : builder.put(RequestBody.create("", JSON_MEDIA_TYPE)).build();
            case "DELETE":
                return body != null ? builder.delete(body).build() : builder.delete().build();
            default:
                return builder.get().build();
        }
    }

    private static void handleSuccessResponse(Context context, String responseBody, ResponseCallback callback) {
        try {
            String message = "Operation successful";

            if (responseBody.startsWith("{")) {
                JSONObject json = new JSONObject(responseBody);
                if (json.has("message")) {
                    message = json.getString("message");
                }
            } else if (responseBody.startsWith("[")) {
                JSONArray jsonArray = new JSONArray(responseBody);
                message = "Received " + jsonArray.length() + " items";
            }

            showToast(context, message);
            callback.onResponse(true, message, responseBody);
        } catch (JSONException e) {
            callback.onResponse(true, "Operation completed", responseBody);
        }
    }

    private static void handleErrorResponse(Context context, int statusCode, String responseBody, ResponseCallback callback) {
        String errorMessage = "Error occurred";

        try {
            if (responseBody.startsWith("{")) {
                JSONObject json = new JSONObject(responseBody);

                if (json.has("detail")) {
                    errorMessage = json.getString("detail");
                }
                else if (json.has("message")) {
                    errorMessage = json.getString("message");
                } else if (json.has("error")) {
                    errorMessage = json.getString("error");
                }
            }
        } catch (JSONException e) {
            errorMessage = "Error " + statusCode + ": Invalid response format";
        }

        switch (statusCode) {
            case 400:
//                errorMessage = "Bad request: " + errorMessage;
                break;
            case 401:
                errorMessage = "Unauthorized: " + errorMessage;
                break;
            case 404:
                errorMessage = "Not found: " + errorMessage;
                break;
            case 500:
                errorMessage = "Server error: " + errorMessage;
                break;
        }

        handleError(context, errorMessage, callback);
    }

    private static void handleError(Context context, String message, ResponseCallback callback) {
        showToast(context, message);
        callback.onResponse(false, message, null);
    }

    private static void showToast(Context context, String message) {
        new Handler(Looper.getMainLooper()).post(() -> {
            if (context != null) {
                Toast.makeText(context.getApplicationContext(), message, Toast.LENGTH_LONG).show();
            }
        });
    }

    protected static void runOnUiThread(Context context, Runnable action) {
        if (context instanceof android.app.Activity) {
            ((android.app.Activity) context).runOnUiThread(action);
        } else {
            new Handler(Looper.getMainLooper()).post(action);
        }
    }
}