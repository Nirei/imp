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
    public static List<String> getList() {

        String url = address + "movies/" + Integer.toString(page++);

        AndroidHttpClient client = AndroidHttpClient.newInstance(GlobalNames.HTTP_USER_AGENT);
        HttpGet request = new HttpGet(url);
        HttpResponse response = null;
        JSONObject responseObject = null;

        List<String> movielist = new ArrayList<String>();
        movielist.add(url);

        try {

            movielist.add("z");
            response = client.execute(request);
            movielist.add("a");
            responseObject = new JSONObject(EntityUtils.toString(response.getEntity()));

            movielist.add("b");

            movielist.add(responseObject.getString("result"));

            movielist.add("c");
            //movielist.add(responseObject.get("data").toString());

            // Lista final
            /*JSONArray lista = responseObject.getJSONArray("data");
            for(int i=0; i<lista.length(); i++) {
                JSONObject elemento = lista.getJSONObject(i);
                movielist.add(elemento.getString("title"));
            }*/

        } catch(Exception e) {
            e.printStackTrace();
        } finally {
            client.close();
        }

        movielist.add("HECHO");

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
