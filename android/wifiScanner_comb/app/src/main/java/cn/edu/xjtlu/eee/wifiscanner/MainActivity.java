package cn.edu.xjtlu.eee.wifiscanner;

import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
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
	EditText Building, Floor, Location_x, Location_y;
	String building, floor, location_x, location_y, okSSID1 = "XJTLU", okSSID2 = "eduroam", okSSID3 = "CMCC-EDU", okSSID4 = "iOffice";

	Button send;
	TextView mainText;
	WifiManager mainWifi;
	WifiReceiver receiverWifi;
	List<ScanResult> wifiList;
	//StringBuffer csv = new StringBuffer();
	StringBuilder sb = new StringBuilder();
	StringBuilder csv = new StringBuilder();
	boolean scanFinished = false;


	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);

		Building = (EditText) findViewById(R.id.Building);
		Floor = (EditText) findViewById(R.id.Floor);
		Location_x = (EditText) findViewById(R.id.Location_x);
		Location_y = (EditText) findViewById(R.id.Location_y);

		send = (Button) findViewById(Send);
		mainText = (TextView) findViewById(R.id.mainText);
		mainWifi = (WifiManager) getApplicationContext().getSystemService(Context.WIFI_SERVICE);
		send.setOnClickListener(this);

		receiverWifi = new WifiReceiver();
		registerReceiver(receiverWifi, new IntentFilter(
				WifiManager.SCAN_RESULTS_AVAILABLE_ACTION));
		mainWifi.startScan();
		mainText.setText("Press \"Send\" update...\n");
	}

	public boolean onCreateOptionsMenu(Menu menu) {
		menu.add(0, 0, 0, "Refresh");
		menu.add(0, 1, 1, "Finish");
		return super.onCreateOptionsMenu(menu);
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
	}

	class WifiReceiver extends BroadcastReceiver {
		public void onReceive(Context c, Intent intent) {
			/*sb = new StringBuilder();
			csv = new StringBuilder();
			wifiList = mainWifi.getScanResults();

			// prepare text for display and CSV table
			sb.append("Number of APs Detected: ");
			sb.append((Integer.valueOf(wifiList.size())).toString());
			sb.append("\n\n");
			for (int i = 0; i < wifiList.size(); i++) {
				// sb.append((Integer.valueOf(i + 1)).toString() + ".");
				// SSID
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

				csv.append((wifiList.get(i)).SSID);
				csv.append(",");
				csv.append((wifiList.get(i)).BSSID);
				csv.append(",");
				csv.append((wifiList.get(i)).frequency);
				csv.append(",");
				csv.append((wifiList.get(i)).level);
				csv.append("\n");
			}
			mainText.setText(sb);
*/
			// notify that Wi-Fi scan has finished
			scanFinished = true;
		}
	}

	public void onClick(View view)
	{

		building = Building.getText().toString();
		floor = Floor.getText().toString();
		location_x = Location_x.getText().toString();
		location_y = Location_y.getText().toString();

		registerReceiver(receiverWifi, new IntentFilter(
				WifiManager.SCAN_RESULTS_AVAILABLE_ACTION));
		if (building.length() == 0 || floor.length() == 0 || location_x.length() == 0 || location_y.length() == 0) {
			Toast.makeText(this, "Incomplete input, try again..", Toast.LENGTH_SHORT).show();
			return;
		}
		else
		{
			mainWifi.startScan();
			//mainWifi
            /*Intent scanResults = new Intent();
            scanResults.putExtra("AP_LIST", csv.toString());
            setResult(RESULT_OK, scanResults);
            finish();*/

			//csv = new StringBuilder();

			wifiList = mainWifi.getScanResults();
			sb.append("Number of APs Detected: ");
			sb.append((Integer.valueOf(wifiList.size())).toString());
			sb.append("\n\n");
			// SSID
			for (int i = 0; i < wifiList.size(); i++) {
				// sb.append((Integer.valueOf(i + 1)).toString() + ".");
				// prepare text for display and CSV table

				if (!((wifiList.get(i)).SSID.equals(okSSID1)) && !((wifiList.get(i)).SSID.equals(okSSID2)) && !((wifiList.get(i)).SSID.equals(okSSID3)) && !((wifiList.get(i)).SSID.equals(okSSID4))) {
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

				csv.append(floor);
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

			//char[] array = params[2].toCharArray();
			//byte[] array = params[2].getBytes();
			//String login_url = "http://192.168.43.222ebapp/login.php";
			//String[] arrays = params[2].split(",");
			//String DATA = params[2].replace(" ", "");

			//String[] xxx = csv.toString().split(",");
			//String a = xxx[0] +" "+ xxx[1] +" "+ xxx[2] +" "+ xxx[3] +" "+ xxx[4] +" "+ xxx[5];

			mainText.setText(sb.toString());
			String method = "register";
			BackgroundTask backgroundTask = new BackgroundTask(this);
			backgroundTask.execute(method, csv.toString());
		}
	}

}