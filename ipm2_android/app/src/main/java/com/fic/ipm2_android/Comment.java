package com.fic.ipm2_android;

/**
 * Created by nirei on 15/10/14.
 */
public class Comment {

    private String content;
    private String date;
    private String user;
    private String email;

    public Comment(String content, String date, String user, String email) {
        this.content = content;
        this.date = date;
        this.user = user;
        this.email = email;
    }

    public String getContent() {
        return content;
    }

    public String getDate() {
        return date;
    }

    public String getEmail() {
        return email;
    }

    public String getUser() {
        return user;
    }
}
