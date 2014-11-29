package es.udc.fic.ipm.ipm4_mando;

import android.app.ListActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;

public class RemoteButtons extends ListActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_remote_buttons);

        ListView list = (ListView) findViewById(android.R.id.list);
        // Los elementos de la lista se pueden seleccionar
        list.setClickable(true);

        // Cargamos el adaptador con la lista inicial de vídeos
        ArrayAdapter ad = new VideoListAdapter(this, VideoList.getVideoList());
        list.setAdapter(ad);

        // Listener para cuando se pulsa un elemento de la lista
        list.setOnItemClickListener(new AdapterView.OnItemClickListener() {

            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
                Model.sendVideo(VideoList.getVideo(i).getVideoId());

                return;
            }
        });

    }

    public void onPlayButtonClick(View v) {

        new Thread(new Runnable() {
            @Override
            public void run() {
                Model.sendPlay();
            }
        }).start();
    }

    public void onPauseButtonClick(View v) {

    }

    public void onAddVideoClick(View v) {

    }

    public void onRemoveVideoClick(View v) {

    }

}
