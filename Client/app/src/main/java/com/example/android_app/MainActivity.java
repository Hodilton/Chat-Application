package com.example.android_app;

import android.content.Intent;
import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;

import com.example.android_app.bottom_nav.chats.ChatsFragment;
import com.example.android_app.bottom_nav.new_chats.NewChatFragment;
import com.example.android_app.bottom_nav.profile.ProfileFragment;
import com.example.android_app.view_models.UserViewModel;
import com.example.android_app.databinding.ActivityMainBinding;

public class MainActivity extends AppCompatActivity {
    private static final int DEFAULT_FRAGMENT_ID = R.id.chats;
    private ActivityMainBinding binding;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        observeData();
        setupFragments();
        setupBottomNavigation();
    }

    private void observeData() {
        UserViewModel.getInstance().getCurrentUser().observe(this, user -> {
            if (user == null) {
                startActivity(new Intent(this, LoginActivity.class));
                finish();
            }
        });
    }

    private void setupFragments() {
        replaceFragment(new ChatsFragment());
        binding.bottomNav.setSelectedItemId(DEFAULT_FRAGMENT_ID);
    }

    private void setupBottomNavigation() {
        binding.bottomNav.setOnItemSelectedListener(item -> {
            int itemId = item.getItemId();

            if (itemId == R.id.chats) {
                replaceFragment(new ChatsFragment());
                return true;
            } else if (itemId == R.id.new_chat) {
                replaceFragment(new NewChatFragment());
                return true;
            } else if (itemId == R.id.profile) {
                replaceFragment(new ProfileFragment());
                return true;
            }
            return false;
        });
    }

    private void replaceFragment(Fragment fragment) {
        getSupportFragmentManager()
                .beginTransaction()
                .replace(binding.fragmentContainer.getId(), fragment)
                .commit();
    }
}