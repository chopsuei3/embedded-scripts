<?php
#date_default_timezone_set("America/Los_Angeles");


$fname = "/home/pi/temperature.rrd";

$opts = array("-s", "300",
"DS:temp:GAUGE:600:U:U",
"RRA:MAX:0.5:1:600",
"RRA:MAX:0.5:6:700",
"RRA:MAX:0.5:24:775",
"RRA:MAX:0.5:288:797"
);



if (file_exists($fname)) 
{
	$datenow = date('U');
	$temp = exec('sudo python /home/pi/readtemp.py');
	$updatevalue = array($datenow . ":" . $temp);
	$ret = rrd_update($fname, $updatevalue);
	if( $ret == 0 )
	{	
		$err = rrd_error();
		echo "ERROR occurred: $err\n";
	}
	else {
	echo "Temperature " . $temp . " logged at " . $datenow;
	}

} 
else 
{
$ret = rrd_create($fname, $opts);
	if( $ret == 0 )
	{
	$err = rrd_error();
	echo "Create error: $err\n";
	} else
	{
	echo "Tempearture database created";
	}
}

?>  
