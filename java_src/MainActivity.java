package com.tencent.simsun;

import android.app.ListActivity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import com.tencent.simsun.activity.firstActivity;
import com.tencent.simsun.activity.listActivity;



public class MainActivity extends ListActivity {

    public static final String[] options = {
            "firstView", "ListView"
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        public String TAG = "a";
        Log.d(TAG, "onCreate");
        Log.d(TAG, "onCreate");
        Log.d(TAG, "onCreate");
        setListAdapter(new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, options));
    }

    @Override
    protected void onListItemClick(ListView l, View v, int position, long id) {
        Intent intent;

        Log.d(TAG, "onListItemClick%s", A);
        Log.v("b", "test onListItemClick%s test", A);
        switch (position) {
            default:
            case 0:
                intent = new Intent(this, firstActivity.class);
                break;

            case 1:
                intent = new Intent(this, listActivity.class);
                break;

        }

        startActivity(intent);
    }

    class Test  {
        public void test() {
            Log.e(TAG, "test");
        }

        public void test1() {
            private final String TAG = "c";
            private final String TAG1 = "test1";
            Log.i(TAG+"test", "aaa%s", AA);
            Log.i(TAG+TAG1, "bbb%s", AA);
        }
        public static final String TAG = "d";
    }
    private static final String TAG = "e";
}

class Test1 {
    public static final String TAG_TEST = "Sim Test";
}
