package com.fic.ipm2_android;

import java.net.CookieStore;
import java.util.ArrayList;
import java.util.List;

import android.net.http.AndroidHttpClient;
import android.os.AsyncTask;
import android.util.Log;

import org.apache.http.HttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.util.EntityUtils;
import org.json.JSONArray;
import org.json.JSONObject;

/**
 * Created by nirei on 15/10/14.
 */
public class Model {

    static String address;
    static String user;
    static String cookie;
    static int page;

    // Login API
    public static void login(String name, String token) {
        user = name;
        cookie = token;
        if(name.endsWith(GlobalNames.ACCOUNT_NAME_DEVELOPMENT_SERVER_SUFFIX)) {
            address = GlobalNames.ADDRESS_LOCAL;
        }
        else {
            address = GlobalNames.ADDRESS_NET;
        }
        page = 1;
    }


    // Movie API
    public static List<PreMovie> getList() {

        String url = address + "movies/page/" + Integer.toString(page++);

        AndroidHttpClient client = AndroidHttpClient.newInstance(GlobalNames.HTTP_USER_AGENT);
        HttpGet request = new HttpGet(url);
        HttpResponse response = null;
        JSONObject responseObject = null;

        List<PreMovie> movielist = new ArrayList<PreMovie>();

        try {

            response = client.execute(request);
            responseObject = new JSONObject(EntityUtils.toString(response.getEntity()));

            PreMovie row = null;

            // Lista final
            JSONArray lista = responseObject.getJSONArray("data");
            for(int i=0; i<lista.length(); i++) {
                JSONObject elemento = lista.getJSONObject(i);
                row = new PreMovie(elemento);
                movielist.add(row);
            }

        } catch(Exception e) {
            e.printStackTrace();
        } finally {
            client.close();
        }

        return movielist;
    }

    public static Movie getMovie(int id) {
        return null;
    }

    public static void setFavorite(int number, boolean fav) {}

    // Comments API
    public static List<Comment> getComments(int page) {
        return null;
    }

    public static void addComment(String comment) {}

    public static void deleteComment(int commentId) {}



}
