package cn.edu.xjtlu.eee.wifiscanner;

import android.app.AlertDialog;
import android.content.Context;
import android.os.AsyncTask;

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLEncoder;

/**
 * Created by zheng on 2017/7/13.
 */

public class BackgroundTask extends AsyncTask<String, String, String>{
    AlertDialog alertDialog;
    Context ctx;

    BackgroundTask(Context ctx) {
        this.ctx = ctx;
    }

    @Override
    protected void onPreExecute() {
        alertDialog = new AlertDialog.Builder(ctx).create();
        alertDialog.setTitle("Log Information...");
    }

    @Override
    protected String doInBackground(String... params) {
        String reg_url = "http://192.168.43.222/wifi_fingerprint/register.php";
        String method =params[0];
        String list = params[1];

        //String login_url = "http://192.168.43.222ebapp/login.php";
        String[] arrays = list.split(",");

        int aps = arrays.length / 8;

        String[] Building;
        Building = new String[aps];
        String[] Floor;
        Floor = new String[aps];
        String[] Location_x;
        Location_x = new String[aps];
        String[] Location_y;
        Location_y = new String[aps];
        String[] SSID;
        SSID = new String[aps];
        String[] BSSID;
        BSSID = new String[aps];
        String[] frequency;
        frequency = new String[aps];
        String[] level;
        level = new String[aps];

        for(int i=0; i< aps; i++) {
            Building[i] = arrays[8*i];
            Floor[i] = arrays[8*i + 1];
            Location_x[i] = arrays[8*i + 2];
            Location_y[i] = arrays[8*i + 3];
            SSID[i] = arrays[8*i + 4];
            BSSID[i] = arrays[8*i + 5];
            frequency[i] = arrays[8*i + 6];
            level[i] = arrays[8*i + 7];
        }
        //Toast.makeText(ctx, "Kao", Toast.LENGTH_LONG).show();

        if (method.equals("register")) {
            try {
                for(int i=0; i<aps; i++){
                    URL url = new URL(reg_url);
                    HttpURLConnection httpURLConnection = (HttpURLConnection) url.openConnection();
                    httpURLConnection.setRequestMethod("POST");
                    httpURLConnection.setDoOutput(true);
                    OutputStream OS = httpURLConnection.getOutputStream();

                    BufferedWriter bufferedWriter = new BufferedWriter(new OutputStreamWriter(OS, "UTF-8"));

                    String data = URLEncoder.encode("Building", "UTF-8") + "=" + URLEncoder.encode(Building[i], "UTF-8") + "&" +
                            URLEncoder.encode("Floor", "UTF-8") + "=" + URLEncoder.encode(Floor[i], "UTF-8") + "&" +
                            URLEncoder.encode("Location_x", "UTF-8") + "=" + URLEncoder.encode(Location_x[i], "UTF-8") + "&" +
                            URLEncoder.encode("Location_y", "UTF-8") + "=" + URLEncoder.encode(Location_y[i], "UTF-8") + "&" +
                            URLEncoder.encode("SSID", "UTF-8") + "=" + URLEncoder.encode(SSID[i], "UTF-8") + "&" +
                            URLEncoder.encode("BSSID", "UTF-8") + "=" + URLEncoder.encode(BSSID[i], "UTF-8") + "&" +
                            URLEncoder.encode("Frequency", "UTF-8") + "=" + URLEncoder.encode(frequency[i], "UTF-8") + "&" +
                            URLEncoder.encode("Level", "UTF-8") + "=" + URLEncoder.encode(level[i], "UTF-8");
                    bufferedWriter.write(data);
                    bufferedWriter.close();

                    OS.close();
                    InputStream IS = httpURLConnection.getInputStream();
                    IS.close();

                }
                return "Loading data success...";
            } catch (MalformedURLException e) {
                e.printStackTrace();
            }  catch (IOException e) {
                e.printStackTrace();
            }

        }

        /*if (method.equals("register"))
        {
            for(int i =0; i < aps; i++)
            {
                Building[i] = temp[i * 8].toString();
                Floor[i] = temp[1 + i * 8].toString();
                Location_x[i] = temp[2 + i * 8].toString();
                Location_y[i] = temp[3 + i * 8].toString();
                SSID[i] = temp[4 + i * 8].toString();
                BSSID[i] = temp[5 + i * 8].toString();
                frequency[i] = temp[6 + i * 8].toString();
                level[i] = temp[7 + i * 8].toString();
            }

            try {
                for(int i = 0; i < aps; i++) {
                    URL url = new URL(reg_url);
                    HttpURLConnection httpURLConnection = (HttpURLConnection) url.openConnection();
                    httpURLConnection.setRequestMethod("POST");
                    httpURLConnection.setDoOutput(true);
                    OutputStream OS = httpURLConnection.getOutputStream();


                    BufferedWriter bufferedWriter = new BufferedWriter(new OutputStreamWriter(OS, "UTF-8"));

                    String data = URLEncoder.encode("Building", "UTF-8") + "=" + URLEncoder.encode(Building[i], "UTF-8") + "&" +
                            URLEncoder.encode("Floor", "UTF-8") + "=" + URLEncoder.encode(Floor[i], "UTF-8") + "&" +
                            URLEncoder.encode("Location_x", "UTF-8") + "=" + URLEncoder.encode(Location_x[i], "UTF-8") + "&" +
                            URLEncoder.encode("Location_y", "UTF-8") + "=" + URLEncoder.encode(Location_y[i], "UTF-8") + "&" +
                            URLEncoder.encode("SSID", "UTF-8") + "=" + URLEncoder.encode(SSID[i], "UTF-8") + "&" +
                            URLEncoder.encode("BSSID", "UTF-8") + "=" + URLEncoder.encode(BSSID[i], "UTF-8") + "&" +
                            URLEncoder.encode("frequency", "UTF-8") + "=" + URLEncoder.encode(frequency[i], "UTF-8") + "&" +
                            URLEncoder.encode("level", "UTF-8") + "=" + URLEncoder.encode(level[i], "UTF-8");

                    bufferedWriter.write(data);
                    bufferedWriter.close();

                    OS.close();
                    InputStream IS = httpURLConnection.getInputStream();
                    IS.close();
                    return "Registration Success...";
                }

            } catch (MalformedURLException e) {
                e.printStackTrace();
            } catch (ProtocolException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }*/
        cancel(true);
        if(isCancelled()) return null;
        return null;
    }  // doin Back


    @Override
    protected void onPostExecute(String s) {
        super.onPostExecute(s);
    }

    @Override
    protected void onProgressUpdate(String... values) {
        if(isCancelled()) return;
    }

    @Override
    protected void onCancelled() {
        super.onCancelled();
    }
}
