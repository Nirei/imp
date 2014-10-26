package com.fic.ipm2_android;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.net.CookieStore;
import java.util.ArrayList;
import java.util.List;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
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
    }


    // Movie API
    public static List<PreMovie> getList(int page, List<PreMovie> list) {

        String url = address + "movies/page/" + Integer.toString(page);

        AndroidHttpClient client = AndroidHttpClient.newInstance(GlobalNames.HTTP_USER_AGENT);
        HttpGet request = new HttpGet(url);
        HttpResponse response = null;
        JSONObject responseObject = null;

        List<PreMovie> movielist = list;

        try {

            response = client.execute(request);
            responseObject = new JSONObject(EntityUtils.toString(response.getEntity()));

            PreMovie row = null;

            // Hay más pelis para cargar
            if(responseObject.getString("result").startsWith("success")) {
                // Lista final
                JSONArray lista = responseObject.getJSONArray("data");
                for(int i=0; i<lista.length(); i++) {
                    JSONObject elemento = lista.getJSONObject(i);
                    row = new PreMovie(elemento);
                    movielist.add(row);
                }
            }

        } catch(Exception e) {
            e.printStackTrace();
        } finally {
            client.close();
        }

        return movielist;
    }

    public static boolean areThereMorePages(int page) {

        List<PreMovie> resultado = Model.getList(page, new ArrayList<PreMovie>());

        // Si la lista devuelta está vacía, no hay más páginas
        return !resultado.isEmpty();

    }

    public static Movie getMovie(int id) {

        String url = address + "movies/" + Integer.toString(id);

        AndroidHttpClient client = AndroidHttpClient.newInstance(GlobalNames.HTTP_USER_AGENT);
        HttpGet request = new HttpGet(url);
        HttpResponse response = null;
        JSONObject responseObject = null;

        Movie datos = null;

        try {

            response = client.execute(request);
            responseObject = new JSONObject(EntityUtils.toString(response.getEntity()));

            // Hay más pelis para cargar
            if(responseObject.getString("result").startsWith("success")) {
                // Carga de datos
                JSONObject json = responseObject.getJSONObject("data");
                datos = new Movie(json);
            }

        } catch(Exception e) {
            e.printStackTrace();
        } finally {
            client.close();
        }

        return datos;
    }

    public static void setFavorite(int number, boolean fav) {}

    // Comments API
    public static List<Comment> getComments(int page) {
        return null;
    }

    public static void addComment(String comment) {}

    public static void deleteComment(int commentId) {}

    // Image API
    // Obtención de la imagen (servidor distinto a la BD de películas)
    public static Bitmap getImage(String image_url) {

        AndroidHttpClient client = AndroidHttpClient.newInstance(GlobalNames.HTTP_USER_AGENT);
        HttpGet request = new HttpGet(image_url);
        request.setHeader("User-Agent", "Mozilla/4.0");
        HttpResponse response = null;
        JSONObject responseObject = null;

        Bitmap datos = null;

        try {

            response = client.execute(request);
            InputStream stream = response.getEntity().getContent();

            // Si descargó la imagen la parcheamos para el ImageView
            if(stream != null) {
                ByteArrayOutputStream baos = new ByteArrayOutputStream();
                int bufferSize = 1024;
                byte[] buffer = new byte[bufferSize];
                int len = 0;
                while ((len = stream.read(buffer)) != -1) {
                    baos.write(buffer, 0, len);
                }
                baos.close();
                byte[] b = baos.toByteArray();
                datos = BitmapFactory.decodeByteArray(b, 0, b.length);
            }

        } catch(Exception e) {
            e.printStackTrace();
        } finally {
            client.close();
        }

        return datos;
    }

}
