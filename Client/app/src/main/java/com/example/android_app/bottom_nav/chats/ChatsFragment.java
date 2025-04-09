package com.example.android_app.bottom_nav.chats;

import android.view.LayoutInflater;
import android.view.ViewGroup;

import com.example.android_app.bottom_nav.BaseFragment;
import com.example.android_app.databinding.FragmentChatsBinding;

public class ChatsFragment extends BaseFragment<FragmentChatsBinding> {
    @Override
    protected FragmentChatsBinding inflateBinding(LayoutInflater inflater, ViewGroup container) {
        return FragmentChatsBinding.inflate(inflater, container, false);
    }
}