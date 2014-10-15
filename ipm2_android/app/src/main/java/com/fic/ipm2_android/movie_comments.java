package com.fic.ipm2_android;

import android.app.Activity;
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


public class movie_comments extends Activity
{

    // VARIABLE PARA PRUEBAS
    private int count = 0;

    private String[] commentsList = {"prime", "mola", "no mola"};

    //private algo movie = NULL;    // La película al que pertenecen los comentarios

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_movie_comments);

        // Obtenemos los parámetros que nos pasó la actividad movie_data
        // Bundle bundle = getIntent.getExtras();
        // this.movie = bundle.getSomething("movie");

        // Indicamos al adaptador los datos a listar
        ArrayAdapter ad = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, this.commentsList);

        // Le pasamos el adaptador a la lista
        ListView list = (ListView) findViewById(android.R.id.list);
        list.setAdapter(ad);
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu)
    {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.movie_comments, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item)
    {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.action_settings)
        {
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    // EVENTOS DE LA INTERFAZ
    public void onSendButtonClick(View v)
    {
        Button b = (Button) v;
        this.count++;
        b.setText("Pulsado " + this.count);
    }
}
