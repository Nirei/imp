package com.fic.ipm2_android;

import org.json.JSONException;
import org.json.JSONObject;

/**
 * Created by nirei on 15/10/14.
 */
public class Comment {

    private int id;
    private String content;
    private String date;
    private String user;
    private String email;

    public Comment(JSONObject data) {
        try {
            id = data.getInt("id");
            content = data.getString("content");
            date = data.getString("comment_date");
            user = data.getString("username");
            email = data.getString("email");
        } catch(JSONException e) {
            e.printStackTrace();
        }
    }

    public Comment(int id, String content, String date, String user, String email) {
        this.id = id;
        this.content = content;
        this.date = date;
        this.user = user;
        this.email = email;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public String getDate() {
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    }

    public String getUser() {
        return user;
    }

    public void setUser(String user) {
        this.user = user;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }
}
