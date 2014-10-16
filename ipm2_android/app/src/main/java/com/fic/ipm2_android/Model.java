package com.fic.ipm2_android;
import java.util.List;

/**
 * Created by nirei on 15/10/14.
 */
public interface Model {

    // Login API
    public void login(String username, String password);
    public void logout();
    public boolean isLoggedIn();

    // Movie API
    public List<Movie> getList();
    public Movie getMovie(int number);
    public void setFavorite(int number, boolean fav);

    // Comment API
    public List<Comment> getComments(int page);
    public void addComment(String comment);
    public void deleteComment(int commentId);

}
