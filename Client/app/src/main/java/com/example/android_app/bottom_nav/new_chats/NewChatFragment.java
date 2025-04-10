package com.example.android_app.bottom_nav.new_chats;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.example.android_app.bottom_nav.BaseFragment;
import com.example.android_app.databinding.FragmentNewChatBinding;
import com.example.android_app.adapters.UserAdapter;
import com.example.android_app.network.UserRequests;

import java.util.ArrayList;

public class NewChatFragment extends BaseFragment<FragmentNewChatBinding> {
    private UserAdapter userAdapter;

    @Override
    protected FragmentNewChatBinding inflateBinding(LayoutInflater inflater, ViewGroup container) {
        return FragmentNewChatBinding.inflate(inflater, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        setupAdapter();
        loadUsers();
    }

    private void setupAdapter() {
        userAdapter = new UserAdapter(requireContext(), new ArrayList<>());
        binding.usersLv.setAdapter(userAdapter);
    }

    private void loadUsers() {
        setLoadingState(true);
        UserRequests.getAllUsers(requireContext(),
                (success, message, users) -> {
            setLoadingState(false);
            if (success && users != null) {
                userAdapter.updateList(users);
            } else {
                Toast.makeText(requireContext(), "Error: " + message, Toast.LENGTH_LONG).show();
            }
        });
    }
}