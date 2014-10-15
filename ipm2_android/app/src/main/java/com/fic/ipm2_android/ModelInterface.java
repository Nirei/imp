package com.fic.ipm2_android;

import java.util.List;

/**
 * Created by nirei on 15/10/14.
 */
public interface ModelInterface {

    public void login(String username, String password);
    public void logout();
    public boolean isLoggedIn();

    public List<Movie> getList();
    public Movie getMovie(int number);
    public void setFavorite(int number, boolean fav);
    public List<Comment> getComments();

}
