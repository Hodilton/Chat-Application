package com.example.android_app.view_models;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;
import com.example.android_app.models.User;
import java.util.List;

public class UserViewModel extends ViewModel {
    private final MutableLiveData<User> currentUser = new MutableLiveData<>();
    private final MutableLiveData<List<User>> allUsers = new MutableLiveData<>();

    public LiveData<User> getCurrentUser() { return currentUser; }
    public void setCurrentUser(User user) { currentUser.setValue(user); }
    public LiveData<List<User>> getAllUsers() { return allUsers; }
    public void setAllUsers(List<User> users) { allUsers.setValue(users); }

    public void logout() {
        currentUser.setValue(null);
    }
}