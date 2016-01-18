<html>
<body>

<h1>Flow Data</h1>

<?php

date_default_timezone_set('America/Los_Angeles');
$pulseArray = array();
$record = 0;

if (($handle = fopen("/tmp/flow.csv", "r")) !== FALSE)
	{
		while (($data = fgetcsv($handle, 1000, ",")) !== FALSE)
		{
			$recordTime = $data[0];
			$pulses = $data[2];
			$pulseArray[$record] = array($recordTime,$pulses);
			$record++;			
	//		print_r($data);
		}
		fclose($handle);
	}
	
//echo count($pulseArray);

echo "<table><tr><th align=\"center\">Date</th><th align=\"center\">Interval (secs)</th><th align=\"center\">Pulses</th></tr>";	
	
	
for ($x = 0; $x <= count($pulseArray); $x++)
{
	$intervalDatetime = strtotime($pulseArray[$x][0]);
	if($x!=0)
	{
		$y = $x - 1;
		$previousRecord = strtotime($pulseArray[$y][0]);
		
		$elapsedTime = $intervalDatetime - $previousRecord;
	}
	else
	{
		$elapsedTime = NULL;
	}
	
	$pulseCount = $pulseArray[$x][1];

echo "<tr><td align=\"center\">" . date('Y-m-d H:i:s',$intervalDatetime) . "</td><td align=\"center\">" . $elapsedTime . "</td><td align=\"center\">" . $pulseCount . "</td></tr>";
}
	
	
?>



<!--<div id="temperature" style="width: 100%; margin: 0 auto"></div>-->

</table>

</body>
</html>
