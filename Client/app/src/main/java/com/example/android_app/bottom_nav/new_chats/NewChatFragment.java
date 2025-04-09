package com.example.android_app.bottom_nav.new_chats;

import android.view.LayoutInflater;
import android.view.ViewGroup;

import com.example.android_app.bottom_nav.BaseFragment;
import com.example.android_app.databinding.FragmentNewChatBinding;

public class NewChatFragment extends BaseFragment<FragmentNewChatBinding> {
    @Override
    protected FragmentNewChatBinding inflateBinding(LayoutInflater inflater, ViewGroup container) {
        return FragmentNewChatBinding.inflate(inflater, container, false);
    }
}