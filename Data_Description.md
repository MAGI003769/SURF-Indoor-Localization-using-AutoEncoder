<p class="normal"><b>Abstract</b>: The UJIIndoorLoc is a Multi-Building Multi-Floor indoor localization database to test Indoor Positioning System that rely on WLAN/WiFi fingerprint.</p>
     </td>
     <td> </td>
   </tr></table>

<table border=1 cellpadding=6>
	<tr>
		<td bgcolor="#DDEEFF"><p class="normal"><b>Data Set Characteristics:&nbsp;&nbsp;</b></p></td>
		<td><p class="normal">Multivariate</p></td>
		<td bgcolor="#DDEEFF"><p class="normal"><b>Number of Instances:</b></p></td>
		<td><p class="normal">21048</p></td>
		<td bgcolor="#DDEEFF"><p class="normal"><b>Area:</b></p></td>
		<td><p class="normal">Computer</p></td>
	</tr>

	<tr>
		<td bgcolor="#DDEEFF"><p class="normal"><b>Attribute Characteristics:</b></p></td>
		<td><p class="normal">Integer, Real</p></td>
		<td bgcolor="#DDEEFF"><p class="normal"><b>Number of Attributes:</b></p></td>
		<td><p class="normal">529</p></td>
		<td bgcolor="#DDEEFF"><p class="normal"><b>Date Donated</b></p></td>
		<td><p class="normal">2014-09-18</p></td>
	</tr>
	
	<tr>
		<td bgcolor="#DDEEFF"><p class="normal"><b>Associated Tasks:</b></p></td>
		<td><p class="normal">Classification, Regression</p></td>
		<td bgcolor="#DDEEFF"><p class="normal"><b>Missing Values?</b></p></td>
		<td><p class="normal">N/A</p></td>
		<td bgcolor="#DDEEFF"><p class="normal"><b>Number of Web Hits:</b></p></td>
		<td><p class="normal">36684</p></td>
	</tr>
<table>


<br />

<p class="small-heading"><b>Source:</b></p>
<p class="normal">Donors/Contact <br>Joaquín Torres-Sospedra jtorres +@+ uji.es <br>Raul Montoliu montoliu +@+ uji.es <br>Adolfo Martínez-Usó admarus +@+ upv.es <br>Joaquín Huerta huerta +@+ uji.es <br>UJI - Institute of New Imaging Technologies, Universitat Jaume I, Avda. Vicente Sos Baynat S/N, 12071, Castellón, Spain. <br>UPV - Departamento de Sistemas Informáticos y Computación, Universitat Politècnica de València, Valencia, Spain. <br><br>Creators <br>Joaquín Torres-Sospedra, Raul Montoliu, Adolfo Martínez-Usó, Tomar J. Arnau, Joan P. Avariento, Mauri Benedito-Bordonau, Joaquín Huerta, Yasmina Andreu, óscar Belmonte, Vicent Castelló, Irene Garcia-Martí, Diego Gargallo, Carlos Gonzalez, Nadal Francisco, Josep López, Ruben Martínez, Roberto Mediero, Javier Ortells, Nacho Piqueras, Ianisse Quizán, David Rambla, Luis E. Rodríguez, Eva Salvador Balaguer, Ana Sanchís, Carlos Serra, and Sergi Trilles.</p>

<br />

<p class="small-heading"><b>Data Set Information:</b></p>
<p class="normal">Many real world applications need to know the localization of a user in the world to provide their services. Therefore, automatic user localization has been a hot research topic in the last years. Automatic user localization consists of estimating the position of the user (latitude, longitude and altitude) by using an electronic device, usually a mobile phone. Outdoor localization problem can be solved very accurately thanks to the inclusion of GPS sensors into the mobile devices. However, indoor localization is still an open problem mainly due to the loss of GPS signal in indoor environments. Although, there are some indoor positioning technologies and methodologies, this database is focused on WLAN fingerprint-based ones (also know as WiFi Fingerprinting).
<br>
<br>Although there are many papers in the literature trying to solve the indoor localization problem using a WLAN fingerprint-based method, there still exists one important drawback in this field which is the lack of a common database for comparison purposes. So, UJIIndoorLoc database is presented to overcome this gap. We expect that the proposed database will become the reference database to compare different indoor localization methodologies based on WiFi fingerprinting.
<br>
<br>The UJIIndoorLoc database covers three buildings of Universitat Jaume I with 4 or more floors and almost 110.000m2. It can be used for classification, e.g. actual building and floor identification, or regression, e.g. actual longitude and latitude estimation. It was created in 2013 by means of more than 20 different users and 25 Android devices. The database consists of 19937 training/reference records (trainingData.csv file) and 1111 validation/test records (validationData.csv file).
<br>
<br>The 529 attributes contain the WiFi fingerprint, the coordinates where it was taken, and other useful information.
<br>
<br>Each WiFi fingerprint can be characterized by the detected Wireless Access Points (WAPs) and the corresponding Received Signal Strength Intensity (RSSI). The intensity values are represented as negative integer values ranging -104dBm (extremely poor signal) to 0dbM. The positive value 100 is used to denote when a WAP was not detected. During the database creation, 520 different WAPs were detected. Thus, the WiFi fingerprint is composed by 520 intensity values.
<br>
<br>Then the coordinates (latitude, longitude, floor) and Building ID are provided as the attributes to be predicted. 
<br>
<br>Additional information has been provided.
<br>
<br>The particular space (offices, labs, etc.) and the relative position (inside/outside the space) where the capture was taken have been recorded. Outside means that the capture was taken in front of the door of the space.
<br>
<br>Information about who (user), how (android device & version) and when (timestamp) WiFi capture was taken is also recorded.
<br>
<br>
<br>
<br></p>

<br />

<p class="small-heading"><b>Attribute Information:</b></p>
<p class="normal">Attribute 001 (WAP001): Intensity value for WAP001. Negative integer values from -104 to 0 and +100. Positive value 100 used if WAP001 was not detected.
<br>....
<br>Attribute 520 (WAP520): Intensity value for WAP520. Negative integer values from -104 to 0 and +100. Positive Vvalue 100 used if WAP520 was not detected.
<br>Attribute 521 (Longitude): Longitude. Negative real values from -7695.9387549299299000 to -7299.786516730871000
<br>Attribute 522 (Latitude): Latitude. Positive real values from 4864745.7450159714 to 4865017.3646842018.
<br>Attribute 523 (Floor): Altitude in floors inside the building. Integer values from 0 to 4.
<br>Attribute 524 (BuildingID): ID to identify the building. Measures were taken in three different buildings. Categorical integer values from 0 to 2.
<br>Attribute 525 (SpaceID): Internal ID number to identify the Space (office, corridor, classroom) where the capture was taken. Categorical integer values.
<br>Attribute 526 (RelativePosition): Relative position with respect to the Space (1 - Inside, 2 - Outside in Front of the door). Categorical integer values. 
<br>Attribute 527 (UserID): User identifier (see below). Categorical integer values. 
<br>Attribute 528 (PhoneID): Android device identifier (see below). Categorical integer values.  
<br>Attribute 529 (Timestamp): UNIX Time when the capture was taken. Integer value. 
<br>
<br>
<br>---------------------------------------------
<br>UserID Anonymized user           Height (cm)
<br>---------------------------------------------
<br>0     USER0000 (Validation User) N/A
<br>1     USER0001                   170
<br>2     USER0002                   176
<br>3     USER0003                   172
<br>4     USER0004                   174
<br>5     USER0005                   184
<br>6     USER0006                   180
<br>7     USER0007                   160
<br>8     USER0008                   176
<br>9     USER0009                   177
<br>10    USER0010                   186
<br>11    USER0011                   176
<br>12    USER0012                   158
<br>13    USER0013                   174
<br>14    USER0014                   173
<br>15    USER0015                   174
<br>16    USER0016                   171
<br>17    USER0017                   166
<br>18    USER0018                   162
<br>----------------------------------------------
<br>
<br>----------------------------------------------
<br>PhoneID  Android Device      Android Ver. UserID
<br>----------------------------------------------
<br>0        Celkon A27          4.0.4(6577)  0
<br>1        GT-I8160            2.3.6        8
<br>2        GT-I8160            4.1.2        0
<br>3        GT-I9100            4.0.4        5
<br>4        GT-I9300            4.1.2        0
<br>5        GT-I9505            4.2.2        0
<br>6        GT-S5360            2.3.6        7
<br>7        GT-S6500            2.3.6        14
<br>8        Galaxy Nexus        4.2.2        10
<br>9        Galaxy Nexus        4.3          0
<br>10       HTC Desire HD       2.3.5        18
<br>11       HTC One             4.1.2        15
<br>12       HTC One             4.2.2        0
<br>13       HTC Wildfire S      2.3.5        0,11
<br>14       LT22i               4.0.4        0,1,9,16
<br>15       LT22i               4.1.2        0
<br>16       LT26i               4.0.4        3
<br>17       M1005D              4.0.4        13
<br>18       MT11i               2.3.4        4
<br>19       Nexus 4             4.2.2        6
<br>20       Nexus 4             4.3          0
<br>21       Nexus S             4.1.2        0
<br>22       Orange Monte Carlo  2.3.5        17
<br>23       Transformer TF101   4.0.3        2
<br>24       bq Curie            4.1.1        12
<br>----------------------------------------------</p>

<br />

<p class="small-heading"><b>Relevant Papers:</b></p>
<p class="normal">Joaquín Torres-Sospedra, Raúl Montoliu, Adolfo Martínez-Usó, Tomar J. Arnau, Joan P. Avariento, Mauri Benedito-Bordonau, Joaquín Huerta <br>UJIIndoorLoc: A New Multi-building and Multi-floor Database for WLAN Fingerprint-based Indoor Localization Problems <br>In Proceedings of the Fifth International Conference on Indoor Positioning and Indoor Navigation, 2014.<br>Available at: <a href="http://www.ipin2014.org/wp/pdf/4A-3.pdf">[Web Link]</a></p>

<br />


<!-- OLD CODE:

<p class="small-heading"><b>Papers That Cite This Data Set<sup>1</sup>:</b></p>
<img src="../assets/rexa.jpg" />
<p class="normal">N/A</p>

-->



<br />

<p class="small-heading"><b>Citation Request:</b></p>
<p class="normal">Joaquín Torres-Sospedra, Raúl Montoliu, Adolfo Martínez-Usó, Tomar J. Arnau, Joan P. Avariento, Mauri Benedito-Bordonau, Joaquín Huerta <br>UJIIndoorLoc: A New Multi-building and Multi-floor Database for WLAN Fingerprint-based Indoor Localization Problems <br>In Proceedings of the Fifth International Conference on Indoor Positioning and Indoor Navigation, 2014.<br>Available at: <a href="http://www.ipin2014.org/wp/pdf/4A-3.pdf">[Web Link]</a></p>
