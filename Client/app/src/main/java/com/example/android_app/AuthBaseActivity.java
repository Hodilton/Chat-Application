package com.example.android_app;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

public abstract class AuthBaseActivity extends AppCompatActivity {
    protected EditText emailEt, passwordEt, usernameEt;
    protected ProgressBar progressBar;
    protected Button actionBtn;
    protected View backBtn;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        getLayoutResource();
        initViews();
        setupListeners();
    }

    protected abstract void getLayoutResource();
    protected abstract void initViews();
    protected abstract void setupListeners();
    protected abstract void performAuthAction();

    protected void setLoadingState(boolean isLoading) {
        progressBar.setVisibility(isLoading ? View.VISIBLE : View.GONE);
        actionBtn.setEnabled(!isLoading);
        if (backBtn != null) backBtn.setEnabled(!isLoading);
    }

    protected boolean validateEmail(String email) {
        if (email.isEmpty()) {
            emailEt.setError("Email is required");
            return false;
        }
        if (!android.util.Patterns.EMAIL_ADDRESS.matcher(email).matches()) {
            emailEt.setError("Valid email required");
            return false;
        }
        return true;
    }

    protected boolean validatePassword(String password) {
        if (password.isEmpty()) {
            passwordEt.setError("Password is required");
            return false;
        }
        if (password.length() < 6) {
            passwordEt.setError("Password must be at least " + 6 + " characters");
            return false;
        }
        return true;
    }

    protected boolean validateUsername(String username) {
        if (username != null && username.isEmpty()) {
            usernameEt.setError("Username is required");
            return false;
        }
        return true;
    }

    protected void handleAuthError(String message) {
        runOnUiThread(() -> {
            if (emailEt != null) emailEt.setError(null);
            if (passwordEt != null) passwordEt.setError(null);
            if (usernameEt != null) usernameEt.setError(null);

            String lowerMsg = message.toLowerCase();

            if (lowerMsg.contains("парол") || lowerMsg.contains("password")) {
                if (passwordEt != null) passwordEt.setError(message);
            }
            else if (lowerMsg.contains("почт") || lowerMsg.contains("email")) {
                if (emailEt != null) emailEt.setError(message);
            }
            else if ((lowerMsg.contains("имя") || lowerMsg.contains("username")) && usernameEt != null) {
                usernameEt.setError(message);
            }
            else {
                Toast.makeText(this, message, Toast.LENGTH_LONG).show();
            }
        });
    }
}