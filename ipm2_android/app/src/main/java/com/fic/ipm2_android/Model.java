package com.fic.ipm2_android;
import java.util.List;

/**
 * Created by nirei on 15/10/14.
 */
public class Model implements ModelInterface
{
    // Server data
    private String address;
    private int port;

    // Movie / Comment page
    private int movie_page = 0;
    private int comment_page = 0;

    // Movie / Comment list
    private List<Movie> movie_list;
    private List<Comment> comment_list;

    public Model(String address, int port)
    {
        this.address = address;
        this.port = port;
    }

    @Override
    public void login(String username, String password)
    {
    }

    @Override
    public void logout()
    {
    }

    @Override
    public boolean isLoggedIn()
    {
        return false;
    }

    @Override
    public List<Movie> getMovieList(int page)
    {
        return null;
    }

    @Override
    public Movie getMovieData(int position)
    {
        return null;
    }

    @Override
    public boolean setFavorite(int number, boolean fav)
    {
        return false;
    }

    @Override
    public List<Comment> getCommentList(Movie movie, int page)
    {
        return null;
    }

    @Override
    public boolean sendComment(String comment)
    {
        return false;
    }
}