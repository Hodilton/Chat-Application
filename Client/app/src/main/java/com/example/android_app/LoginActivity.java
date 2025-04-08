package com.example.android_app;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.android_app.databinding.ActivityLoginBinding;
import com.example.android_app.network.AuthRequests;

public class LoginActivity extends AppCompatActivity {
    private ActivityLoginBinding binding;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityLoginBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());
        setupListeners();
    }

    private void setupListeners() {
        binding.loginBtn.setOnClickListener(v -> attemptLogin());
        binding.goToRegisterActivityTv.setOnClickListener(v ->
                startActivity(new Intent(this, RegisterActivity.class)));
    }

    private void attemptLogin() {
        String email = binding.emailEt.getText().toString().trim();
        String password = binding.passwordEt.getText().toString().trim();

        if (email.isEmpty() || password.isEmpty()) {
            showToast("Все поля должны быть заполнены.");
            return;
        }

        AuthRequests.login(this, email, password,
                new AuthRequests.ResponseCallback() {
            @Override
            public void onResponse(boolean success, String response) {
                if (success) {
                    startActivity(new Intent(LoginActivity.this, MainActivity.class));
                    finish();
                } else {
                    showToast("Ошибка входа. Проверьте данные.");
                }
            }
        });
    }

    private void showToast(String message) {
        Toast.makeText(this, message, Toast.LENGTH_SHORT).show();
    }
}
