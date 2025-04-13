package com.example.android_app.bottom_nav.users;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.example.android_app.bottom_nav.BaseFragment;
import com.example.android_app.adapters.UserAdapter;
import com.example.android_app.databinding.FragmentUsersBinding;
import com.example.android_app.models.User;
import com.example.android_app.network.ChatRequests;
import com.example.android_app.network.UserRequests;
import com.example.android_app.view_models.UserViewModel;

import java.util.ArrayList;

public class UsersFragment extends BaseFragment<FragmentUsersBinding> {
    private UserAdapter userAdapter;

    @Override
    protected FragmentUsersBinding inflateBinding(LayoutInflater inflater, ViewGroup container) {
        return FragmentUsersBinding.inflate(inflater, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        setupAdapter();
        loadUsers();
    }

    private void setupAdapter() {
        userAdapter = new UserAdapter(requireContext(), new ArrayList<>());
        userAdapter.setOnUserLongClickListener(this::showUserActionsDialog);
        binding.usersLv.setAdapter(userAdapter);
    }

    private void loadUsers() {
        setLoadingState(true);
        UserRequests.getAllUsersExcept(requireContext(),
                userViewModel.getCurrentUser().getValue().getId(),
                (success, message, users) -> {
            setLoadingState(false);
            if (success && users != null) {
                userAdapter.updateList(users);
            } else {
                Toast.makeText(requireContext(), "Error: " + message, Toast.LENGTH_LONG).show();
            }
        });
    }

    private void showUserActionsDialog(User user) {
        new UserActionDialog.Builder(requireContext())
                .setOnConfirmAction(() -> createNewChatWithUser(user))
                .setOnCancelAction(() -> {  })
                .setOnCreateChatAction(() -> {  })
                .build()
                .show();
    }

    private void createNewChatWithUser(User otherUser) {
        User currentUser = UserViewModel.getInstance().getCurrentUser().getValue();
        if (currentUser == null || otherUser == null) return;

        setLoadingState(true);
        ChatRequests.startChat(requireContext(),
                String.valueOf(currentUser.getId()),
                String.valueOf(otherUser.getId()),
                (success, message, chat) -> {
            setLoadingState(false);
            if (success) {
                Toast.makeText(requireContext(),
                        "Chat created with " + otherUser.getUsername(),
                        Toast.LENGTH_SHORT).show();
            } else {
                Toast.makeText(requireContext(),
                        "Error in create chat: " + message,
                        Toast.LENGTH_LONG).show();
            }
        });
    }
}