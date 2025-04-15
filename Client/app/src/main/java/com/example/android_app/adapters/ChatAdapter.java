package com.example.android_app.adapters;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.ViewGroup;

import androidx.annotation.NonNull;

import com.example.android_app.databinding.ItemChatBinding;
import com.example.android_app.models.Chat;

import java.util.List;

public class ChatAdapter extends BaseListAdapter<Chat, ItemChatBinding, ChatAdapter.ChatViewHolder> {

    private OnChatLongClickListener longClickListener;

    public interface OnChatLongClickListener {
        void onChatLongClicked(Chat chat);
    }

    public ChatAdapter(@NonNull Context context, @NonNull List<Chat> chats) {
        super(context, chats);
    }

    public void setOnChatLongClickListener(OnChatLongClickListener listener) {
        this.longClickListener = listener;
    }

    @NonNull
    @Override
    protected ItemChatBinding createBinding(@NonNull LayoutInflater inflater, @NonNull ViewGroup parent) {
        return ItemChatBinding.inflate(inflater, parent, false);
    }

    @NonNull
    @Override
    protected ChatViewHolder createViewHolder(@NonNull ItemChatBinding binding) {
        return new ChatViewHolder(binding);
    }

    @Override
    protected void bindViewHolder(@NonNull ChatViewHolder holder, int position) {
        holder.bind(getItem(position));
    }

    protected class ChatViewHolder extends BaseViewHolder<ItemChatBinding> {
        public ChatViewHolder(@NonNull ItemChatBinding binding) {
            super(binding);
        }

        void bind(@NonNull Chat chat) {
            binding.usernameTv.setText(chat.getOtherUser().getUsername());
            binding.lastMessageTv.setText("Last message.");
            binding.timestampTv.setText(chat.getCreatedAt());

            binding.getRoot().setOnLongClickListener(v -> {
                if (longClickListener != null) {
                    longClickListener.onChatLongClicked(chat);
                    return true;
                }
                return false;
            });
        }
    }
}