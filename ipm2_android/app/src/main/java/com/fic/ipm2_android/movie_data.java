package com.fic.ipm2_android;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;


public class movie_data extends Activity
{

    // VARIABLE PARA PRUEBAS
    private int count = 0;

    //private algo movie = NULL;    // La película que mostramos

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_movie_data);

    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu)
    {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.movie_data, menu);
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
    public void onShowCommentsButtonClick(View v)
    {
        // Intent de nueva actividad
        Intent i = new Intent(this, movie_comments.class);
        // Pasamos como parámetro la peli de la cual coger los comentarios
        //// i.putExtra("movie", this.movie);
        // Iniciamos la actividad
        startActivity(i);
    }
}
