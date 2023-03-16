import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

import com.jcraft.jsch.JSch;
import com.jcraft.jsch.Session;

public class MainActivity extends AppCompatActivity {

    private static final String LOCAL_USER = "your_local_username";
    private static final String LOCAL_IP = "your_local_ip";
    private static final int LOCAL_PORT = 22;
    private static final String LOCAL_PASSWORD = "your_local_password";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button buttonPwn = findViewById(R.id.button_pwn);
        buttonPwn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                new ExecuteSSHCommand().execute();
            }
        });
    }

    private static class ExecuteSSHCommand extends AsyncTask<Void, Void, Void> {

        @Override
        protected Void doInBackground(Void... voids) {
            try {
                JSch jsch = new JSch();
                Session session = jsch.getSession(LOCAL_USER, LOCAL_IP, LOCAL_PORT);
                session.setPassword(LOCAL_PASSWORD);
                session.setConfig("StrictHostKeyChecking", "no");
                session.connect();

                // Esegui il comando "~/home/autopwn.py"
                session.openChannel("exec").setCommand("~/home/autopwn.py").connect();

                session.disconnect();
            } catch (Exception e) {
                e.printStackTrace();
            }

            return null;
        }
    }
}
