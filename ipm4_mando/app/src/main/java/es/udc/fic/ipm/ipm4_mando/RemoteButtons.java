package es.udc.fic.ipm.ipm4_mando;

import android.app.ListActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.ToggleButton;

public class RemoteButtons extends ListActivity {

    private String last_selected;
    private ArrayAdapter ad;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_remote_buttons);

        ListView list = (ListView) findViewById(android.R.id.list);
        // Los elementos de la lista se pueden seleccionar
        list.setClickable(true);

        // Cargamos el adaptador con la lista inicial de vídeos
        ad = new VideoListAdapter(this, VideoList.getVideoList());
        list.setAdapter(ad);

        // Listener para cuando se pulsa un elemento de la lista
        list.setOnItemClickListener(new AdapterView.OnItemClickListener() {

            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {

                final int pos = i;

                final ToggleButton borrar = (ToggleButton) findViewById(R.id.removeButton);

                // Se ha marcado para borrar
                if(borrar.isChecked()) {
                    new Thread(new Runnable() {
                        @Override
                        public void run() {

                            VideoList.removeVideo(pos);

                            runOnUiThread(new Runnable() {
                                @Override
                                public void run() {

                                    // Refresca la lista de videos
                                    ad.notifyDataSetChanged();
                                    // Desmarca el botón de borrado
                                    borrar.setChecked(false);
                                }
                            });

                        }
                    }).start();
                } else {
                    new Thread(new Runnable() {
                        @Override
                        public void run() {
                            String videoId = VideoList.getVideo(pos).getVideoId();
                            Model.sendVideo(videoId);
                        }
                    }).start();
                }


                return;
            }
        });

    }

    public void onPlayButtonClick(View v) {

        ToggleButton borrar = (ToggleButton) findViewById(R.id.removeButton);
        borrar.setChecked(false);

        new Thread(new Runnable() {
            @Override
            public void run() {
                Model.sendPlay();
            }
        }).start();
    }

    public void onPauseButtonClick(View v) {

        ToggleButton borrar = (ToggleButton) findViewById(R.id.removeButton);
        borrar.setChecked(false);

        new Thread(new Runnable() {
            @Override
            public void run() {
                Model.sendPause();
            }
        }).start();
    }

    public void onAddVideoClick(View v) {

        ToggleButton borrar = (ToggleButton) findViewById(R.id.removeButton);
        borrar.setChecked(false);

        LinearLayout botones = (LinearLayout) findViewById(R.id.listLayout);
        LinearLayout formulario = (LinearLayout) findViewById(R.id.formLayout);
        ListView lista = (ListView) findViewById(android.R.id.list);

        lista.setVisibility(View.GONE);
        botones.setVisibility(View.GONE);
        formulario.setVisibility(View.VISIBLE);
    }

    public void onCancelFormClick(View v) {

        LinearLayout botones = (LinearLayout) findViewById(R.id.listLayout);
        LinearLayout formulario = (LinearLayout) findViewById(R.id.formLayout);
        ListView lista = (ListView) findViewById(android.R.id.list);

        formulario.setVisibility(View.GONE);
        lista.setVisibility(View.VISIBLE);
        botones.setVisibility(View.VISIBLE);
    }

}
