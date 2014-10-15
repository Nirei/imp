package com.fic.ipm2_android;

import android.app.Activity;
import android.app.ListActivity;
import android.content.Intent;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;


public class movie_list extends ListActivity
{

    // VARIABLES PARA PRUEBAS
    private int count = 0;

    private StringBuffer[] movieList = {new StringBuffer("Shrek"), new StringBuffer("El padrion"),
                                        new StringBuffer("Papá pitufo"), new StringBuffer("Harry Potter"),
                                        new StringBuffer("Brave Heart")}; // La lista de pelis

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_movie_list);

        // Indicamos al adaptador los datos a listar
        ArrayAdapter ad = new ArrayAdapter<StringBuffer>(this, android.R.layout.simple_list_item_1, this.movieList);

        // Le pasamos el adaptador a la lista
        ListView list = (ListView) findViewById(android.R.id.list);
        list.setAdapter(ad);

        // Los elementos de la lista se pueden seleccionar
        list.setClickable(true);

        list.setOnItemClickListener(new AdapterView.OnItemClickListener() {

            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int i, long l)
            {
                TextView item = (TextView) view;

                Intent intent = new Intent(movie_list.this, movie_data.class);
                //intent.putExtra("movie", view.getText());
                startActivity(intent);

                return;
            }
        });
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu)
    {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.movie_list, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item)
    {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if(id == R.id.action_settings)
        {
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    //EVENTOS DE LA INTERFAZ
    public void onAdvSearchButtonClick(View v)
    {
        Button b = (Button) v;
        this.count++;
        b.setText("Pulsado " + this.count);
    }

    public void onMovieList(View v)
    {

    }
}
