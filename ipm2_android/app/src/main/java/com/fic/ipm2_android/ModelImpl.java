package com.fic.ipm2_android;

import java.util.List;

/**
 * Created by nirei on 15/10/14.
 */
public class ModelImpl implements Model {

    private String address;
    private int port;

    public ModelImpl(String address, int port) {
        this.address = address;
        this.port = port;
    }

    @Override
    public void login(String username, String password) {}

    @Override
    public void logout() {}

    @Override
    public boolean isLoggedIn() {
       return false;
    }

    @Override
    public void addComment() {}

    @Override
    public void deleteComment() {}

    @Override
    public List<Comment> getComments() {
        return null;
    }

    @Override
    public List<Movie> getList() {
        return null;
    }

    @Override
    public void setFavorite(int number, boolean fav) {}

    @Override
    public Movie getMovie(int id) {
       return null;
    }

}
