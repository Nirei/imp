package com.fic.ipm2_android;

import android.app.ListActivity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;

import java.util.ArrayList;
import java.util.List;


public class movie_list extends ListActivity
{
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
        // Indicamos que se está realizando la búsqueda
        final Button b = (Button) v;
        b.setText(R.string.searching);

        EditText campo = (EditText) findViewById(R.id.simpleSearchField);
        final String criteria = campo.getText().toString();
        final Context context = this;

        new Thread(new Runnable() {
            @Override
            public void run() {

                List<PreMovie> res = null;

                // Si el criterio es una cadena vacía, cargamos la página normal de películas
                if(criteria.isEmpty()) {
                    res = Model.getList(1, new ArrayList<PreMovie>());
                    page = 1; // La primera página vuelve a ser la 1
                } else {
                    res = Model.findMovies(criteria);
                    page = -2; // Usamos la página para marcar que es una lista de búsqueda
                }
                final List<PreMovie> nuevaLista = res;

                // Ahora la interfaz debe cargar los datos de la película
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {

                        // Indicamos al adaptador los datos a listar
                        movieList = nuevaLista;
                        ArrayAdapter ad = new MovieListAdapter(context, movieList);

                        // Le pasamos el adaptador a la lista
                        ListView list = (ListView) findViewById(android.R.id.list);
                        list.setAdapter(ad);

                        // Actualizamos la info del botón
                        b.setText(R.string.movielist_search_button);

                        // En los resultados de búsqueda el botón de cargar sobra, lo quitamos
                        Button b2 = (Button) findViewById(R.id.loadButton);
                        if(page == -2) {
                            b2.setVisibility(View.GONE);
                        } else {
                            b2.setVisibility(View.VISIBLE);
                        }
                    }
                });
            }
        }).start();
    }

    public void onLoadButtonClick(View v) {

        final Button b = (Button) v;

        // Dejamos un mensaje en el botón para que el usuario sepa que está en ello.
        b.setText(R.string.loading);

        new Thread(new Runnable() {
            @Override
            public void run() {
                // Este bucle no debería poder ejecutarse NUNCA (el botón no está en pantalla cuando
                // se muestra una búsqueda concreta, y por tanto no puede ejecutarse este evento),
                // pero lo pongo igual para evitar problemas.
                if(page == -2) {
                    page = 1;
                }

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
