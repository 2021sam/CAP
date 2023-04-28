<?php
	// echo "echo disables auto re direct !<br>";
	$file = fopen("ip.txt", "r") or die("Unable to open CAP ip file.  Call 510.246.5504");
	$ip = fgets($file);
	// echo $ip . "-" . strlen($ip) . "<br>";
	fclose($file);
	// header("Location: http://{$ip}");
	// readfile("http://{$ip}")

	
	echo "<h1><a href='http://{$ip}' target='_blank'>Credit Card Log</a></h1>";
?>
