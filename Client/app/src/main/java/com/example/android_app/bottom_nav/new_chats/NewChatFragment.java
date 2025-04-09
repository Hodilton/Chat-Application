package com.example.android_app.bottom_nav.new_chats;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.example.android_app.bottom_nav.BaseFragment;
import com.example.android_app.databinding.FragmentNewChatBinding;

public class NewChatFragment extends BaseFragment<FragmentNewChatBinding> {
    @Override
    protected FragmentNewChatBinding inflateBinding(LayoutInflater inflater, ViewGroup container) {
        return FragmentNewChatBinding.inflate(inflater, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
    }
}