package com.example.android_app;

import android.os.Bundle;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.android_app.databinding.ActivityRegisterBinding;
import com.example.android_app.network.AuthRequests;

public class RegisterActivity extends AppCompatActivity {
    private ActivityRegisterBinding binding;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityRegisterBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());
        setupListeners();
    }

    private void setupListeners() {
        binding.backBtn.setOnClickListener(v -> finish());
        binding.signUpBtn.setOnClickListener(v -> attemptRegistration());
    }

    private void attemptRegistration() {
        String username = binding.usernameEt.getText().toString().trim();
        String email = binding.emailEt.getText().toString().trim();
        String password = binding.passwordEt.getText().toString().trim();

        if (username.isEmpty() || email.isEmpty() || password.isEmpty()) {
            showToast("Все поля должны быть заполнены.");
            return;
        }

        AuthRequests.register(this, username, email, password,
                new AuthRequests.ResponseCallback() {
                    @Override
                    public void onResponse(boolean success, String response) {
                        if (success) {
                            showToast("Регистрация успешна!");
                            finish();
                        } else {
                            showToast("Ошибка регистрации.");
                        }
                    }
                });
    }

    private void showToast(String message) {
        Toast.makeText(this, message, Toast.LENGTH_SHORT).show();
    }
}