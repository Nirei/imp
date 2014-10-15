package com.fic.ipm2_android;

import java.util.List;

/**
 * Created by nirei on 15/10/14.
 */
public interface ModelInterface {

    public void login(String username, String password);
    public void logout();
    public boolean isLoggedIn();

    public List<Movie> getList(int page);
    public Movie getMovie(int id);
    public void addMovie(Movie movie);
    public void modifyMovie(Movie movie);
    public void deleteMovie(int id);
}
