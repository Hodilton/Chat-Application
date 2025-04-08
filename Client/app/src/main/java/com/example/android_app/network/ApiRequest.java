package com.example.android_app.network;

import android.content.Context;
import android.util.Log;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import okhttp3.*;

import java.io.IOException;

public abstract class ApiRequest {
    private static final String TAG = "ApiRequest";
    private static final MediaType JSON_MEDIA_TYPE = MediaType.parse("application/json; charset=utf-8");
    private static final OkHttpClient client = new OkHttpClient();

    public interface ResponseCallback {
        void onResponse(boolean success, String response);
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
                if (context instanceof AppCompatActivity) {
                    ((AppCompatActivity) context).runOnUiThread(() ->
                            Toast.makeText(context, "Ошибка соединения", Toast.LENGTH_SHORT).show()
                    );
                }
                Log.e(TAG, "Request failed", e);
                callback.onResponse(false, null);
            }

            @Override
            public void onResponse(@NonNull Call call, @NonNull Response response) throws IOException {
                boolean success = response.isSuccessful();
                String responseBody = response.body() != null ? response.body().string() : "";

                if (context instanceof AppCompatActivity) {
                    ((AppCompatActivity) context).runOnUiThread(() -> {
                        if (success) {
                            Toast.makeText(context, "Запрос выполнен успешно", Toast.LENGTH_SHORT).show();
                        } else {
                            Toast.makeText(context, "Ошибка выполнения запроса", Toast.LENGTH_SHORT).show();
                        }
                    });
                }
                callback.onResponse(success, responseBody);
            }
        });
    }
}