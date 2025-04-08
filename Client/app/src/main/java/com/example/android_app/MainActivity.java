package com.example.android_app;

import android.os.Bundle;

import android.content.Intent;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        if(true) {
            startActivity(new Intent(MainActivity.this, LoginActivity.class));
        }
    }
}