package com.fic.ipm2_android;
import java.util.List;
/**
 * Created by nirei on 15/10/14.
 */
public interface ModelInterface
{
    // Datos de sesión
    public void login(String username, String password);
    public void logout();
    public boolean isLoggedIn();

    // Datos de pelis
    public List<Movie> getMovieList(int page);
    public Movie getMovieData(int position);
    public boolean setFavorite(int number, boolean fav);

    // Datos de comentarios
    public List<Comment> getCommentList(Movie movie, int page);
    public boolean sendComment(String comment);
}