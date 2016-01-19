<?php
date_default_timezone_set("America/Los_Angeles");
$now = date("Y-m-d H:i:s");
$epoch = time();
$temp = exec('sudo python /home/pi/temperature/readtemp.py');

$log = '/home/pi/temperature/temperature.csv';

if (file_exists($log))
{
	$fname = fopen($log,'a');
	$update = array($now,$epoch,$temp);
	fputcsv($fname,$update);
#        echo "Temperature " . $temp . " logged at " . $now. "\n";
}
else
{
	$fname = fopen($log,'w');
	$headers = array("DateTime","EpochTime","TemperatureF");
	fputcsv($fname,$headers);

	$update = array($now,$epoch,$temp);
	fputcsv($fname,$update);
}

?>
