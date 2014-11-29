package es.udc.fic.ipm.ipm4_mando;

import android.net.http.AndroidHttpClient;
import org.apache.http.client.methods.HttpGet;

/**
 * Created by sauron on 11/29/14.
 */
public class Model {

    private static String address = "http://192.168.0.8:8888/";

    public static void sendPlay() {

        String url = address + "msg/play";
        AndroidHttpClient client = AndroidHttpClient.newInstance("Mozilla/5.0");
        HttpGet request = new HttpGet(url);

        try {
            client.execute(request);
        } catch(Exception e) {
            e.printStackTrace();
        } finally {
            client.close();
        }
    }

    public static void sendPause() {

        String url = address + "msg/pause";
        AndroidHttpClient client = AndroidHttpClient.newInstance("Mozilla/5.0");
        HttpGet request = new HttpGet(url);

        try {
            client.execute(request);
        } catch(Exception e) {
            e.printStackTrace();
        } finally {
            client.close();
        }
    }

    public static void sendVideo(String videoId) {

        String url = address + "msg/video=" + videoId;
        AndroidHttpClient client = AndroidHttpClient.newInstance("Mozilla/5.0");
        HttpGet request = new HttpGet(url);

        try {
            client.execute(request);
        } catch(Exception e) {
            e.printStackTrace();
        } finally {
            client.close();
        }
    }
}
