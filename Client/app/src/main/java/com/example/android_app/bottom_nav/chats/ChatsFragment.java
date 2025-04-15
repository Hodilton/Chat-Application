package com.example.android_app.bottom_nav.chats;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.example.android_app.adapters.ChatAdapter;
import com.example.android_app.bottom_nav.BaseFragment;
import com.example.android_app.databinding.FragmentChatsBinding;
import com.example.android_app.models.Chat;
import com.example.android_app.models.User;
import com.example.android_app.network.ChatRequests;
import com.example.android_app.view_models.UserViewModel;

import java.util.ArrayList;

public class ChatsFragment extends BaseFragment<FragmentChatsBinding> {
    private ChatAdapter chatAdapter;

    @Override
    protected FragmentChatsBinding inflateBinding(LayoutInflater inflater, ViewGroup container) {
        return FragmentChatsBinding.inflate(inflater, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        setupAdapter();
        loadChats();
    }

    private void setupAdapter() {
        chatAdapter = new ChatAdapter(requireContext(), new ArrayList<>());
        chatAdapter.setOnChatLongClickListener(this::showDeleteChatDialog);
        binding.chatsLv.setAdapter(chatAdapter);
    }

    private void loadChats() {
        setLoadingState(true);
        ChatRequests.getUserChats(requireContext(),
                userViewModel.getCurrentUser().getValue().getId(),
                (success, message, chats) -> {
                    setLoadingState(false);
                     if (success) {
                        if (chats == null || chats.isEmpty()) {
                            binding.emptyStateTv.setVisibility(View.VISIBLE);
                            binding.chatsLv.setVisibility(View.GONE);
                        } else {
                            binding.emptyStateTv.setVisibility(View.GONE);
                            binding.chatsLv.setVisibility(View.VISIBLE);
                            chatAdapter.updateList(chats);
                        }
                    } else {
                        Toast.makeText(requireContext(),
                                "Error: " + message, Toast.LENGTH_LONG).show();
                    }
                });
    }

    private void showDeleteChatDialog(Chat chat) {
        new ChatActionDialog.Builder(requireContext())
                .setOnConfirmAction(() -> deleteChatWithUser(chat))
                .setOnCancelAction(() -> { })
                .setOnDeleteChatAction(() -> { })
                .build()
                .show();
    }

    private void deleteChatWithUser(Chat chat) {
        User currentUser = UserViewModel.getInstance().getCurrentUser().getValue();
        if (currentUser == null || chat == null) return;

        setLoadingState(true);
        ChatRequests.deleteChat(requireContext(),
                currentUser.getId(),
                chat.getOtherUser().getId(),
                (success, message) -> {
                    setLoadingState(false);
                    if (success) {
                        loadChats();
                        Toast.makeText(requireContext(),
                                "Chat deleted", Toast.LENGTH_SHORT).show();
                    } else {
                        Toast.makeText(requireContext(),
                                "Error in delete chat: " + message, Toast.LENGTH_LONG).show();
                    }
                });
    }
}