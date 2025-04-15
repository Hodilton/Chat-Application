package com.example.android_app;

import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.text.Editable;
import android.text.TextWatcher;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.android_app.adapters.MessageAdapter;
import com.example.android_app.databinding.ActivityChatBinding;
import com.example.android_app.models.Message;
import com.example.android_app.models.User;
import com.example.android_app.network.MessageRequests;
import com.example.android_app.view_models.UserViewModel;

import java.util.ArrayList;

public class ChatActivity extends AppCompatActivity {
    private ActivityChatBinding binding;
    private MessageAdapter messageAdapter;

    private int chatId;
    private User otherUser;

    private int lastMessageId = 0;
    private Handler refreshHandler;
    private static final long REFRESH_DELAY = 2000;

    private final Runnable refreshRunnable = new Runnable() {
        @Override
        public void run() {
            loadNewMessages();
            refreshHandler.postDelayed(this, REFRESH_DELAY);
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityChatBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        refreshHandler = new Handler(Looper.getMainLooper());

        chatId = getIntent().getIntExtra("chat_id", -1);
        otherUser = getIntent().getParcelableExtra("other_user");

        if (chatId == -1 || otherUser == null) {
            Toast.makeText(this, "Invalid chat data", Toast.LENGTH_SHORT).show();
            finish();
            return;
        }

        setTitle(otherUser.getUsername());
        setupListeners();
        setupAdapter();
        loadInitialMessages();
        setupListeners();
    }

    @Override
    protected void onResume() {
        super.onResume();
        startAutoRefresh();
    }

    @Override
    protected void onPause() {
        super.onPause();
        stopAutoRefresh();
    }

    private void startAutoRefresh() {
        if (refreshHandler == null) {
            refreshHandler = new Handler(Looper.getMainLooper());
        }
        refreshHandler.postDelayed(refreshRunnable, REFRESH_DELAY);
    }

    private void stopAutoRefresh() {
        if (refreshHandler != null) {
            refreshHandler.removeCallbacks(refreshRunnable);
        }
    }

    private void loadInitialMessages() {
        MessageRequests.getChatMessages(this, chatId,
                (success, message, messages) -> {
            if (success && messages != null && !messages.isEmpty()) {
                messageAdapter.updateList(messages);
                lastMessageId = messages.get(messages.size() - 1).getId();
                scrollToBottom();
            }
        });
    }

    private void loadNewMessages() {
        MessageRequests.getNewMessages(this, chatId, lastMessageId,
                (success, message, messages) -> {
            if (success && messages != null && !messages.isEmpty()) {
                for (Message msg : messages) {
                    messageAdapter.addMessage(msg);
                }
                lastMessageId = messages.get(messages.size() - 1).getId();
                scrollToBottom();
            }
        });
    }

    private void setupAdapter() {
        messageAdapter = new MessageAdapter(this, new ArrayList<>());
        binding.messagesLv.setAdapter(messageAdapter);
    }

    private void loadMessages() {
        MessageRequests.getChatMessages(this, chatId,
                (success, message, messages) -> {
                    if (success && messages != null) {
                        messageAdapter.updateList(messages);
                        scrollToBottom();
                    } else {
                        Toast.makeText(this, "Error: " + message, Toast.LENGTH_SHORT).show();
                    }
                });
    }

    private void setupListeners() {
        binding.backButton.setOnClickListener(v -> finish());
        binding.sendMessageBtn.setOnClickListener(v -> sendMessage());

        binding.messageEt.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {}

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                binding.sendMessageBtn.setEnabled(s.length() > 0);
            }

            @Override
            public void afterTextChanged(Editable s) {}
        });
    }

    private void sendMessage() {
        String content =  binding.messageEt.getText().toString().trim();
        if (content.isEmpty()) return;

        User currentUser = UserViewModel.getInstance().getCurrentUser().getValue();
        if (currentUser == null) return;

        binding.messageEt.setText("");
        binding.sendMessageBtn.setEnabled(false);
        MessageRequests.sendMessage(this, chatId, currentUser.getId(), content,
                (success, message, newMessage) -> {
                    binding.sendMessageBtn.setEnabled(true);
                    if (success && newMessage != null) {
//                        messageAdapter.addMessage(newMessage);
                        scrollToBottom();
                    } else {
                        Toast.makeText(this, "Error: " + message, Toast.LENGTH_SHORT).show();
                    }
                });
    }

    private void scrollToBottom() {
        binding.messagesLv.post(() -> binding.messagesLv.setSelection(messageAdapter.getCount() - 1));
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        stopAutoRefresh();
    }
}