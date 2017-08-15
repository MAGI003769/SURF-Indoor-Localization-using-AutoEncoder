package cn.edu.xjtlu.eee.wifiscanner;

import android.app.AlertDialog;
import android.content.Context;
import android.os.AsyncTask;
import android.util.Log;

import java.io.BufferedOutputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLEncoder;
import java.util.HashMap;
import java.util.Map;

/**
 * Created by zheng on 2017/7/13.
 */

public class BackgroundTask extends AsyncTask<String, String, String>{
    public static String submitPostData(Map<String, String> params, String encode) throws MalformedURLException {
        /**
         * 发送POST请求到服务器并返回服务器信息
         * @param params 请求体内容
         * @param encode 编码格式
         * @return 服务器返回信息
         */
        byte[] data = getRequestData(params, encode).toString().getBytes();
        //URL url = new URL("http://127.0.0.1:5000");
        URL url = new URL("http://192.168.43.222:5000");

        HttpURLConnection httpURLConnection = null;
        try{
            httpURLConnection = (HttpURLConnection)url.openConnection();
            httpURLConnection.setConnectTimeout(3000);  // set connecting overtime
            httpURLConnection.setDoInput(true);         // Open input flow, to get info from server
            httpURLConnection.setDoOutput(true);        // Open output flow, to put info to server
            httpURLConnection.setRequestMethod("POST"); // set the request method as POST
            httpURLConnection.setUseCaches(false);      // Not allowed to user caches with POST method

            //httpURLConnection.connect();

           // int response = httpURLConnection.getResponseCode();
           // if (response != HttpURLConnection.HTTP_OK) {
            //    return "Fail";
           // }
            // set the content type
            httpURLConnection.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
            // set the length of request
            httpURLConnection.setRequestProperty("Content-Length", String.valueOf(data.length));
            // 获得输入流，向服务器写入数
            OutputStream outputStream = new BufferedOutputStream(httpURLConnection.getOutputStream());
            outputStream.write(data);
            outputStream.flush();                       // after flush(), data could really be send

            InputStream inputStream = httpURLConnection.getInputStream();

            return dealResponseResult(inputStream);             // deal with the result

        } catch (IOException e) {
            e.printStackTrace();
            return "Fail";
        } finally {
            httpURLConnection.disconnect();
            return "Success";
        }
    }

    /**
     * 封装请求体信息
     * @param params 请求体内容
     * @param encode 编码格式
     * @return 请求体信息
     */
    public static StringBuffer getRequestData(Map<String, String> params, String encode) {
        StringBuffer stringBuffer = new StringBuffer();            //存储封装好的请求体信息
        try {
            for (Map.Entry<String, String> entry : params.entrySet()) {
                stringBuffer.append(entry.getKey())
                        .append("=")
                        .append(URLEncoder.encode(entry.getValue(), encode))
                        .append("&");
            }
            stringBuffer.deleteCharAt(stringBuffer.length() - 1);   // 删除最后一个"&"
        } catch (Exception e) {
            e.printStackTrace();
        }
        return stringBuffer;
    }

    /**
     * 处理服务器的响应结果（将输入流转换成字符串)
     * @param inputStream 服务器的响应输入流
     * @return 服务器响应结果字符串
     */
    public static String dealResponseResult(InputStream inputStream) {
        String resultData = null;
        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
        byte[] data = new byte[1024];
        int len = 0;
        try {
            while ((len = inputStream.read(data)) != -1) {
                byteArrayOutputStream.write(data, 0, len);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        resultData = new String(byteArrayOutputStream.toByteArray());
        return resultData;
    }

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

        //String reg_url = "http://192.168.43.222/wifi_fingerprint/register.php";
        String method =params[0];
        String list = params[1];

        if (method.equals("register")) {
            //String login_url = "http://192.168.43.222ebapp/login.php";
            String[] arrays = list.split(",");
            int aps = arrays.length / 8;
            String post_result = null;

            for (int i = 0; i < aps; i++) {
                Map<String, String> param = new HashMap<String, String>();

                param.put("Building", arrays[8 * i]);
                param.put("Room", arrays[8 * i + 1]);
                param.put("Location_x", arrays[8 * i + 2]);
                param.put("Location_y", arrays[8 * i + 3]);
                param.put("SSID", arrays[8 * i + 4]);
                param.put("BSSID", arrays[8 * i + 5]);
                param.put("Frequency", arrays[8 * i + 6]);
                param.put("Level", arrays[8 * i + 7]);
                if (i != aps - 1) {
                    param.put("Down?", "NO");
                } else {
                    param.put("Down?", "YES");
                }
                try {
                    post_result = submitPostData(param, "utf-8");
                } catch (MalformedURLException e) {
                    e.printStackTrace();
                }
            }
            Log.i("POST_RESULT", post_result);
            return post_result;
        }
        return null;
    }

    @Override
    protected void onPostExecute(String Results) {
        alertDialog = new AlertDialog.Builder(ctx).create();
        alertDialog.setTitle(Results);
        //super.onPostExecute(s);
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
