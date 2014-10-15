package com.fic.ipm2_android;

/**
 * Created by nirei on 15/10/14.
 */
public class Movie {

    private int id;
    private String title;
    private String category;
    private String synopsis;
    private int year;

    public Movie(int id, String title, String category, String synopsis, int year) {
        this.id = id;
        this.title = title;
        this.category = category;
        this.synopsis = synopsis;
        this.year = year;
    }

    public int getId() {
        return id;
    }

    public int getYear() {
        return year;
    }

    public String getCategory() {
        return category;
    }

    public String getSynopsis() {
        return synopsis;
    }

    public String getTitle() {
        return title;
    }
}
