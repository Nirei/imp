package com.fic.ipm2_android;

import android.app.ListActivity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.TextView;

import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;


public class movie_list extends ListActivity
{
    private int count = 0;
    private int page = 1;

    private List<PreMovie> movieList = new ArrayList<PreMovie>(); // La lista de pelis

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_movie_list);

        ListView list = (ListView) findViewById(android.R.id.list);
        // Los elementos de la lista se pueden seleccionar
        list.setClickable(true);

        // Cargamos la primera página de películas
        this.loadMovieListPage();

        // Listener para cuando se pulsa un elemento de la lista
        list.setOnItemClickListener(new AdapterView.OnItemClickListener() {

            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
                Intent intent = new Intent(movie_list.this, movie_data.class);
                // Obtenemos la PreMovie de la peli seleccionada
                intent.putExtra("id", movieList.get(i).getId());
                startActivity(intent);

                return;
            }
        });
    }

    // Obtención de páginas de películas
    public void loadMovieListPage() {

        final Context context = this;

        new Thread(new Runnable() {
            @Override
            public void run() {
                // Obtenemos la siguiente página de pelis
                final List<PreMovie> nuevaLista = Model.getList(page, movieList);
                page = page+1;

                // Cada página nueva que se cargue implica actualizar la vista
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        // Indicamos al adaptador los datos a listar
                        movieList = nuevaLista;
                        ArrayAdapter ad = new MovieListAdapter(context, movieList);

                        // Le pasamos el adaptador a la lista
                        ListView list = (ListView) findViewById(android.R.id.list);
                        list.setAdapter(ad);
                    }
                });
            }
        }).start();

    }

    //EVENTOS DE LA INTERFAZ
    public void onSearchButtonClick(View v) {
        Button b = (Button) v;
        this.count++;
        b.setText("Pulsado " + this.count);
    }

    public void onLoadButtonClick(View v) {

        final Button b = (Button) v;

        // Dejamos un mensaje en el botón para que el usuario sepa que está en ello.
        b.setText(R.string.loading);

        new Thread(new Runnable() {
            @Override
            public void run() {
                final boolean hay = Model.areThereMorePages(page);

                // Cada página nueva que se cargue implica actualizar la vista
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        if(hay) {
                            // Actualizamos la lista de pelis
                            loadMovieListPage();
                            b.setText(R.string.movielist_load_button);
                        } else {
                            b.setText(R.string.no_more_pages);
                        }
                    }
                });


            }
        }).start();
    }
}
