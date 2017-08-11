package cn.edu.xjtlu.eee.wifiscanner;

import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.net.wifi.ScanResult;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.util.List;

import static cn.edu.xjtlu.eee.wifiscanner.R.id.Send;

public class MainActivity extends Activity implements View.OnClickListener{
	EditText Building, Room, Location_x, Location_y;
	String building, room, location_x, location_y;
	String okSSID1 = "AAA", okSSID2 = "AA", okSSID3 = "A";			// filter these wifi signal

	Button send;
	TextView mainText;
	WifiManager mainWifi;
	WifiReceiver receiverWifi;
	List<ScanResult> wifiList;

	StringBuilder sb = new StringBuilder();		// info for display
	StringBuilder csv = new StringBuilder();	// transfer info
	boolean scanFinished = false;


	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);

		Building = (EditText) findViewById(R.id.Building);
		Room = (EditText) findViewById(R.id.Room);
		Location_x = (EditText) findViewById(R.id.Location_x);
		Location_y = (EditText) findViewById(R.id.Location_y);

		send = (Button) findViewById(Send);
		mainText = (TextView) findViewById(R.id.mainText);
		mainWifi = (WifiManager) getApplicationContext().getSystemService(Context.WIFI_SERVICE);
		send.setOnClickListener(this);

		receiverWifi = new WifiReceiver();
		registerReceiver(receiverWifi, new IntentFilter(
				WifiManager.SCAN_RESULTS_AVAILABLE_ACTION));
		mainText.setText("Press \"Send\" to update...\n");
	}

	public boolean onCreateOptionsMenu(Menu menu) {
		menu.add(0, 0, 0, "Refresh");
		menu.add(0, 1, 1, "Finish");
		return super.onCreateOptionsMenu(menu);
	}

	//Check if wifi mode is open
	public boolean isWiFi() {
		ConnectivityManager connectivityManager = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
		NetworkInfo networkInfo = connectivityManager.getActiveNetworkInfo();
		if (networkInfo != null && networkInfo.getType() == ConnectivityManager.TYPE_WIFI) {
			return true;
		} else {
			return false;
		}
	}

	public boolean onMenuItemSelected(int featureId, MenuItem item) {
		switch (item.getItemId()) {
		case 0:
			mainWifi.startScan();
			mainText.setText("Starting Scan...\n");
			break;
		case 1:
			// To return CSV-formatted text back to calling activity (e.g., MIT
			// App Inventor App)
			Intent scanResults = new Intent();
			scanResults.putExtra("AP_LIST", csv.toString());
			setResult(RESULT_OK, scanResults);
			finish();
			break;
		default:
			break;
		}
		return super.onMenuItemSelected(featureId, item);
	}

	protected void onPause() {
		super.onPause();
	}

	protected void onResume() {
		super.onResume();

		registerReceiver(receiverWifi, new IntentFilter(
				WifiManager.SCAN_RESULTS_AVAILABLE_ACTION));

		mainWifi.startScan();
		wifiList = mainWifi.getScanResults();
		mainText.setText((Integer.valueOf(wifiList.size())).toString());
	}

	class WifiReceiver extends BroadcastReceiver {
		public void onReceive(Context c, Intent intent) {

			// notify that Wi-Fi scan has finished
			scanFinished = true;
		}
	}

	public void onClick(View view)
	{
		sb = new StringBuilder();
		csv = new StringBuilder();
		mainText.setText(null);

		building = Building.getText().toString();
		room = Room.getText().toString();
		location_x = Location_x.getText().toString();
		location_y = Location_y.getText().toString();

		if (isWiFi() != true) {
			Toast.makeText(this, "Open WiFi mode please....", Toast.LENGTH_SHORT).show();
			return;
		}

		registerReceiver(receiverWifi, new IntentFilter(
				WifiManager.SCAN_RESULTS_AVAILABLE_ACTION));
		if (building.length() == 0 || room.length() == 0 || location_x.length() == 0 || location_y.length() == 0) {
			Toast.makeText(this, "Incomplete input, try again..", Toast.LENGTH_SHORT).show();
			return;
		}
		else
		{
			//mainWifi
            /*Intent scanResults = new Intent();
            scanResults.putExtra("AP_LIST", csv.toString());
            setResult(RESULT_OK, scanResults);
            finish();*/
			mainWifi.startScan();
			wifiList = mainWifi.getScanResults();

			sb.append("Number of APs Detected: ");
			sb.append((Integer.valueOf(wifiList.size())).toString());
			sb.append("\n\n");
			// SSID
			for (int i = 0; i < wifiList.size(); i++) {
				// sb.append((Integer.valueOf(i + 1)).toString() + ".");
				// prepare text for display and CSV table
				if (((wifiList.get(i)).SSID.equals(okSSID1)) || ((wifiList.get(i)).SSID.equals(okSSID2)) || ((wifiList.get(i)).SSID.equals(okSSID3))) {// && !((wifiList.get(i)).SSID.equals(okSSID3)) && !((wifiList.get(i)).SSID.equals(okSSID4))) {
					continue;
				}
				sb.append("SSID:").append((wifiList.get(i)).SSID);
				sb.append("\n");
				sb.append("BSSID:").append((wifiList.get(i)).BSSID);
				sb.append("\n");
				sb.append("Capabilities:").append(
						(wifiList.get(0)).capabilities);
				sb.append("\n");
				sb.append("Frequency:").append((wifiList.get(i)).frequency);
				sb.append("\n");
				sb.append("Level:").append((wifiList.get(i)).level);
				sb.append("\n\n");

				csv.append(building);
				csv.append(",");

				csv.append(room);
				csv.append(",");

				csv.append(location_x);
				csv.append(",");

				csv.append(location_y);
				csv.append(",");
				// SSID
				csv.append((wifiList.get(i)).SSID);
				csv.append(",");
				// BSSID
				csv.append((wifiList.get(i)).BSSID);
				csv.append(",");
				// frequency
				csv.append((wifiList.get(i)).frequency);
				csv.append(",");
				// level
				csv.append((wifiList.get(i)).level);
				csv.append(",");
			}
			unregisterReceiver(receiverWifi);

			mainText.setText(sb.toString());
			String method = "register";
			BackgroundTask backgroundTask = new BackgroundTask(this);
			String result;
			backgroundTask.execute(method, csv.toString());
		}
	}
}