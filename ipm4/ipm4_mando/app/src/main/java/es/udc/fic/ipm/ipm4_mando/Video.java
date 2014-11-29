package es.udc.fic.ipm.ipm4_mando;

/**
 * Created by sauron on 11/29/14.
 */
public class Video {

    private String name;
    private String videoId;

    public Video(String name, String videoId) {
        this.name = name;
        this.videoId = videoId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getVideoId() {
        return videoId;
    }

    public void setVideoId(String videoId) {
        this.videoId = videoId;
    }
}
