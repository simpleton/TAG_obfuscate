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
        public String TAG = "AAA";
        Log.d(TAG, "onCreate");
        Log.d(TAG, "onCreate");
        Log.d(TAG, "onCreate");
        setListAdapter(new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, options));
    }

    @Override
    protected void onListItemClick(ListView l, View v, int position, long id) {
        Intent intent;

        Log.d(TAG, "onListItemClick%s", A);
        Log.v("test", "test onListItemClick%s test", A);
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
            private final String TAG = "test1";
            Log.i(Test.TAG, "aaa%s", AA);
        }
        public static final String TAG = "Test2";
    }
    private static final String TAG = "MainActivity111";
}

class Test1 {
    public static final String TAG_TEST = "Sim Test";
}
