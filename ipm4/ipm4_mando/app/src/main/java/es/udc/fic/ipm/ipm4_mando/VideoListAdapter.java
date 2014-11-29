package es.udc.fic.ipm.ipm4_mando;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import java.util.List;

/**
 * Created by sauron on 11/29/14.
 */
public class VideoListAdapter extends ArrayAdapter<Video> {
    private final Context context;
    private final List<Video> values;

    public VideoListAdapter(Context context, List<Video> values) {
        super(context, R.layout.video_list_layout, values);
        this.context = context;
        this.values = values;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        LayoutInflater inflater = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        View rowView = inflater.inflate(R.layout.video_list_layout, parent, false);
        TextView name = (TextView) rowView.findViewById(R.id.videoName);

        name.setText(values.get(position).getName());

        return rowView;
    }

}