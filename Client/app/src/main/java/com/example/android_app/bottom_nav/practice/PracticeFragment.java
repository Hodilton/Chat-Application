package com.example.android_app.bottom_nav.practice;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.example.android_app.bottom_nav.BaseFragment;
import com.example.android_app.databinding.FragmentChatsBinding;

public class PracticeFragment extends BaseFragment<FragmentChatsBinding> {
    @Override
    protected FragmentChatsBinding inflateBinding(LayoutInflater inflater, ViewGroup container) {
        return FragmentChatsBinding.inflate(inflater, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        setupAdapter();
    }

    private void setupAdapter() {

    }
}