package com.fic.ipm2_android;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.http.AndroidHttpClient;

import org.apache.http.HttpResponse;
import org.apache.http.client.methods.HttpDelete;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
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
                    list.add(row);
                }
            }

        } catch(Exception e) {
            e.printStackTrace();
        } finally {
            client.close();
        }

        return list;
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

    public static List<PreMovie> findMovies(String criteria) {
        // IMPORTANTE: Hay que parchear espacios y sustituírlos por %20 o NO FUNCIONARÁ
        String criteria_patched = criteria.replace(" ", "%20");

        String url = address + "movies?q=" + criteria_patched;

        AndroidHttpClient client = AndroidHttpClient.newInstance(GlobalNames.HTTP_USER_AGENT);
        HttpGet request = new HttpGet(url);
        HttpResponse response = null;
        JSONObject responseObject = null;

        List<PreMovie> listaMovies = new ArrayList<PreMovie>();

        try {

            response = client.execute(request);
            responseObject = new JSONObject(EntityUtils.toString(response.getEntity()));

            PreMovie row = null;

            // Tenemos varias películas con ese criterio
            if(responseObject.getString("result").startsWith("success")) {
                // Lista resultante
                JSONArray lista = responseObject.getJSONArray("data");
                for(int i=0; i<lista.length(); i++) {
                    JSONObject elemento = lista.getJSONObject(i);
                    row = new PreMovie(elemento);
                    listaMovies.add(row);
                }
            }

        } catch(Exception e) {
            e.printStackTrace();
        } finally {
            client.close();
        }

        return listaMovies;
    }

    public static boolean getFavorite(Movie movie) {

        String url = address + "movies/" + Integer.toString(movie.getId()) + "/fav";

        AndroidHttpClient client = AndroidHttpClient.newInstance(GlobalNames.HTTP_USER_AGENT);
        HttpGet request = new HttpGet(url);
        HttpResponse response = null;
        JSONObject responseObject = null;

        // IMPORTANTE: Es necesario pasar la cookie
        request.addHeader("Cookie", cookie);

        boolean fav = false;

        try {

            response = client.execute(request);
            responseObject = new JSONObject(EntityUtils.toString(response.getEntity()));

            // El server respondió
            if(responseObject.getString("result").startsWith("success")) {

                String favorito = responseObject.getString("data");

                fav = favorito.startsWith("true");
            }

        } catch(Exception e) {
            e.printStackTrace();
        } finally {
            client.close();
        }

        return fav;
    }

    public static void setFavorite(Movie movie, boolean fav) {
        String url = address + "movies/" + Integer.toString(movie.getId()) + "/fav";

        AndroidHttpClient client = AndroidHttpClient.newInstance(GlobalNames.HTTP_USER_AGENT);
        HttpResponse response = null;

        // Marcar como favorito
        if(fav) {
            HttpPost request = new HttpPost(url);
            JSONObject responseObject = null;

            // IMPORTANTE: Es necesario pasar la cookie
            request.addHeader("Cookie", cookie);

            try {

                response = client.execute(request);
                responseObject = new JSONObject(EntityUtils.toString(response.getEntity()));

                // El server no pudo realizar la petición
                if(responseObject.getString("result").startsWith("failure")) {
                    throw new Exception();
                }

            } catch(Exception e) {
                e.printStackTrace();
            } finally {
                client.close();
            }
        // Desmarcar como favorito
        } else {
            HttpDelete request = new HttpDelete(url);
            JSONObject responseObject = null;

            // IMPORTANTE: Es necesario pasar la cookie
            request.addHeader("Cookie", cookie);

            try {

                response = client.execute(request);
                responseObject = new JSONObject(EntityUtils.toString(response.getEntity()));

                // El server no pudo realizar la petición
                if(responseObject.getString("result").startsWith("failure")) {
                    throw new Exception();
                }

            } catch(Exception e) {
                e.printStackTrace();
            } finally {
                client.close();
            }
        }
    }

    // Comments API
    public static List<Comment> getComments(int id, int page, List<Comment> list) {
        String url = address + "movies/" + Integer.toString(id) + "/comments/page/" + Integer.toString(page);

        AndroidHttpClient client = AndroidHttpClient.newInstance(GlobalNames.HTTP_USER_AGENT);
        HttpGet request = new HttpGet(url);
        HttpResponse response = null;
        JSONObject responseObject = null;

        try {

            response = client.execute(request);
            responseObject = new JSONObject(EntityUtils.toString(response.getEntity()));

            Comment row = null;

            // Hay más comentarios para cargar
            if(responseObject.getString("result").startsWith("success")) {
                // Lista final
                JSONArray lista = responseObject.getJSONArray("data");
                for(int i=0; i<lista.length(); i++) {
                    JSONObject elemento = lista.getJSONObject(i);
                    row = new Comment(elemento);
                    list.add(row);
                }
            }

        } catch(Exception e) {
            e.printStackTrace();
        } finally {
            client.close();
        }

        return list;
    }

    public static boolean areThereMoreComments(int id, int page) {

        List<Comment> resultado = Model.getComments(id, page, new ArrayList<Comment>());

        // Si la lista devuelta está vacía, no hay más páginas
        return !resultado.isEmpty();

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
