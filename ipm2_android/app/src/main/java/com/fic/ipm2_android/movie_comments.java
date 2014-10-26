package com.fic.ipm2_android;

import android.app.Activity;
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


public class movie_comments extends Activity
{

    // VARIABLE PARA PRUEBAS
    private int count = 0;

    // Id de la película
    private int id;

    // Última página de comentarios cargada
    private int page = 1;

    private List<Comment> commentsList = new ArrayList();

    //private algo movie = NULL;    // La película al que pertenecen los comentarios

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_movie_comments);

        // Obtenemos el intent que inició la actividad
        Intent intent = getIntent();

        // Y sacamos la id de la peli cuyos comentarios debemos mostrar
        this.id = intent.getIntExtra("id", -1);

        ListView list = (ListView) findViewById(android.R.id.list);
        // Los elementos de la lista se pueden seleccionar (para poder borrarlos)
        list.setClickable(true);

        // Cargamos la primera página de comentarios
        this.loadCommentListPage();

        // Creamos evento para tocar comentarios
        list.setOnItemClickListener(new AdapterView.OnItemClickListener() {

            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
                Intent intent = new Intent(movie_comments.this, comment_display.class);
                // Obtenemos la PreMovie de la peli seleccionada
                intent.putExtra("movie_id", id);
                intent.putExtra("comment_id", commentsList.get(i).getId());
                intent.putExtra("content", commentsList.get(i).getContent());
                intent.putExtra("date", commentsList.get(i).getDate());
                intent.putExtra("username", commentsList.get(i).getUser());
                intent.putExtra("email", commentsList.get(i).getEmail());
                startActivity(intent);

                return;
            }
        });

    }

    // Obtención de páginas de películas
    public void loadCommentListPage() {

        final Context context = this;

        new Thread(new Runnable() {
            @Override
            public void run() {
                // Obtenemos la siguiente página de pelis
                if(page == 1) {
                    commentsList = new ArrayList<Comment>();
                }
                final List<Comment> nuevaLista = Model.getComments(id, page, commentsList);
                page = page+1;

                // Cada página nueva que se cargue implica actualizar la vista
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        // Indicamos al adaptador los datos a listar
                        commentsList = nuevaLista;
                        ArrayAdapter ad = new CommentListAdapter(context, commentsList);

                        // Le pasamos el adaptador a la lista
                        ListView list = (ListView) findViewById(android.R.id.list);
                        list.setAdapter(ad);
                    }
                });
            }
        }).start();

    }

    // EVENTOS DE LA INTERFAZ
    public void onSendButtonClick(View v)
    {
        // Obtenemos el texto del comentario
        EditText texto = (EditText) findViewById(R.id.commentField);
        final String content = texto.getText().toString();

        // ¡¡Ojo, si el campo de texto está vacío no mandamos nada!!
        if(content.isEmpty()) {
            return;
        }

        // Indicamos al usuario que el mensaje se está enviando
        final Button b = (Button) v;
        b.setText(R.string.sending);

        new Thread(new Runnable() {
            @Override
            public void run() {

                final int comment_id = Model.addComment(id, content);

                // Cada página nueva que se cargue implica actualizar la vista
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        if(comment_id != -1) {
                            // Reiniciamos la lista de comentarios
                            page = 1;
                            loadCommentListPage();
                            b.setText(R.string.commentlist_load_button);
                        } else {
                            b.setText(R.string.not_found);
                        }
                    }
                });
            }
        }).start();
    }

    public void onLoadCommentsButtonClick(View v) {

        final Button b = (Button) v;

        // Advertimos al usuario de que estamos realizando la petición
        b.setText(R.string.loading);

        new Thread(new Runnable() {
            @Override
            public void run() {

                final boolean hay = Model.areThereMoreComments(id, page);

                // Cada página nueva que se cargue implica actualizar la vista
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        if(hay) {
                            // Actualizamos la lista de pelis
                            loadCommentListPage();
                            b.setText(R.string.commentlist_load_button);
                        } else {
                            b.setText(R.string.no_more_comments);
                        }
                    }
                });


            }
        }).start();
    }
}
