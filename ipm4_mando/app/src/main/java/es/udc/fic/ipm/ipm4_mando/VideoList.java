package es.udc.fic.ipm.ipm4_mando;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by sauron on 11/29/14.
 */
public class VideoList {

    private static List<Video> lista;

    // Sólo una vez al iniciar la aplicación, rellena la lista con vídeos predefinidos
    static {
        Video elem = null;

        lista = new ArrayList<Video>();

        elem = new Video("Video from example", "YD9SEtaVKgA");
        lista.add(elem);
        elem = new Video("7-seconds video example", "DX_eeOZVS2o");
        lista.add(elem);
        elem = new Video("30-minutes video example", "FQZuu8hAeeA");
        lista.add(elem);
        elem = new Video("10-hours video example", "imn3HoDZXrw");
        lista.add(elem);
        elem = new Video("Trololo", "oavMtUWDBTM");
        lista.add(elem);
        elem = new Video("Just for Laughs", "rsMPlqQmvTQ");
        lista.add(elem);
        elem = new Video("Game Theorists", "LplSnXQMf38");
        lista.add(elem);
        elem = new Video("Fiesta Pagana", "XTO-toY3Wao");
        lista.add(elem);
        elem = new Video("We are the champions", "Jmd4OLzhQw0");
        lista.add(elem);
    }

    public static void addVideo(Video video) {
        lista.add(video);
    }

    public static void removeVideo(int pos) {
        lista.remove(pos);
    }

    public static Video getVideo(int pos) {
        return lista.get(pos);
    }

    public static List<Video> getVideoList() {
        return lista;
    }
}


