package com.fic.ipm2_android;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.util.DisplayMetrics;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;


public class movie_data extends Activity
{

    // VARIABLE PARA PRUEBAS
    private int count = 0;

    // La id de la peli
    private int id;
    // Los datos de la peli
    private Movie datos = null;


    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_movie_data);

        // Obtenemos el intent que inició la actividad
        Intent intent = getIntent();

        // Y sacamos la id de la peli a mostrar
        this.id = intent.getIntExtra("id", -1);



        new Thread(new Runnable() {
            @Override
            public void run() {
                datos = Model.getMovie(id);

                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        // Localizamos los widgets de los campos
                        TextView titulo = (TextView) findViewById(R.id.titleField);
                        TextView sinopsis = (TextView) findViewById(R.id.synopsisField);
                        TextView user = (TextView) findViewById(R.id.userField);
                        TextView email = (TextView) findViewById(R.id.emailField);

                        // ¡¡Comprobamos que el servidor devolvió algo!!
                        if(datos != null) {
                            // E insertamos los datos
                            String title = new String(datos.getTitle() + " (" + Integer.toString(datos.getYear())
                                    + ", " + datos.getCategory() + ")");
                            titulo.setText(title);
                            sinopsis.setText(datos.getSynopsis());
                            user.setText(datos.getUsername());
                            email.setText(datos.getEmail());

                            // Aquí pediremos la imagen
                            new Thread(new Runnable() {
                                @Override
                                public void run() {
                                    final Bitmap bmp = Model.getImage(datos.getImage_url());

                                    runOnUiThread(new Runnable() {
                                        @Override
                                        public void run() {
                                            // Configuramos el widget (tamaño de imagen y reescalado)
                                            ImageView imageView = (ImageView)findViewById(R.id.imageView);
                                            DisplayMetrics tam = new DisplayMetrics();
                                            getWindowManager().getDefaultDisplay().getMetrics(tam);
                                            // Máximo de ancho la mitad de la pantalla
                                            imageView.setMaxWidth(tam.widthPixels/2);

                                            // Ponemos la imagen en su widget
                                            imageView.setImageBitmap(bmp);
                                        }
                                    });
                                }
                            }).start();
                        }
                    }
                });
            }
        }).start();

    }

    // EVENTOS DE LA INTERFAZ
    public void onShowCommentsButtonClick(View v)
    {
        // Intent de nueva actividad
        Intent i = new Intent(this, movie_comments.class);
        // Pasamos como parámetro la peli de la cual coger los comentarios
        i.putExtra("id", this.id);
        // Iniciamos la actividad
        startActivity(i);
    }
}
