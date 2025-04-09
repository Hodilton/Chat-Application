package com.example.android_app.bottom_nav.profile;

import android.view.LayoutInflater;
import android.view.ViewGroup;

import com.example.android_app.bottom_nav.BaseFragment;
import com.example.android_app.databinding.FragmentProfileBinding;

public class ProfileFragment extends BaseFragment<FragmentProfileBinding> {
    @Override
    protected FragmentProfileBinding inflateBinding(LayoutInflater inflater, ViewGroup container) {
        return FragmentProfileBinding.inflate(inflater, container, false);
    }
}