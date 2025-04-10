package com.example.android_app.adapters;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.ViewGroup;

import androidx.annotation.NonNull;

import com.example.android_app.R;
import com.example.android_app.databinding.ItemUserBinding;
import com.example.android_app.models.User;

import java.util.List;

public class UserAdapter extends BaseListAdapter<
        User,
        ItemUserBinding,
        UserAdapter.UserViewHolder> {

    public UserAdapter(@NonNull Context context, @NonNull List<User> users) {
        super(context, users);
    }

    @NonNull
    @Override
    protected ItemUserBinding createBinding(@NonNull LayoutInflater inflater,
                                            @NonNull ViewGroup parent) {
        return ItemUserBinding.inflate(inflater, parent, false);
    }

    @NonNull
    @Override
    protected UserViewHolder createViewHolder(@NonNull ItemUserBinding binding) {
        return new UserViewHolder(binding);
    }

    @Override
    protected void bindViewHolder(@NonNull UserViewHolder holder, int position) {
        holder.bind(getItem(position));
    }

    protected static class UserViewHolder extends BaseViewHolder<ItemUserBinding> {
        public UserViewHolder(@NonNull ItemUserBinding binding) {
            super(binding);
        }

        void bind(@NonNull User user) {
            binding.usernameTv.setText(user.getUsername());
            binding.profileIv.setImageResource(R.drawable.baseline_person_outline_24);
        }
    }
}