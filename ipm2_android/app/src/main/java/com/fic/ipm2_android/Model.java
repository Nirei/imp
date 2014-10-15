package com.fic.ipm2_android;

import java.util.List;

/**
 * Created by nirei on 15/10/14.
 */
public class Model implements ModelInterface {

    private String address;
    private int port;

    public Model(String address, int port) {
        this.address = address;
        this.port = port;
    }

    @Override
    public void login(String username, String password) {
        
    }

    @Override
    public void logout() {

    }

    @Override
    public boolean isLoggedIn() {
        return false;
    }

    @Override
    public List<Movie> getList(int page) {
        return null;
    }

    @Override
    public Movie getMovie(int id) {
        return null;
    }

    @Override
    public void addMovie(Movie movie) {

    }

    @Override
    public void modifyMovie(Movie movie) {

    }

    @Override
    public void deleteMovie(int id) {

    }
}
