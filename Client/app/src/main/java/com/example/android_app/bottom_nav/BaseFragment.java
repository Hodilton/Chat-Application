package com.example.android_app.bottom_nav;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;
import androidx.viewbinding.ViewBinding;

import com.example.android_app.MainActivity;
import com.example.android_app.view_models.UserViewModel;

public abstract class BaseFragment<B extends ViewBinding> extends Fragment {
    protected B binding;
    protected abstract B inflateBinding(LayoutInflater inflater, ViewGroup container);
    protected UserViewModel userViewModel;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater,
                             @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        binding = inflateBinding(inflater, container);
        return binding.getRoot();
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        if (getActivity() instanceof MainActivity) {
            userViewModel = ((MainActivity) getActivity()).getUserViewModel();
        } else {
            userViewModel = new ViewModelProvider(requireActivity()).get(UserViewModel.class);
        }
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }
}