<HTML>
<HEAD>
<?php  
$STAT=strtoupper(htmlspecialchars($_GET['STAT'])) ; if (!$STAT){ $STAT="EAS"; }
date_default_timezone_set('UTC');
$yr=htmlspecialchars($_GET['yr']) ; if (!$yr){ $yr=date(Y); } 
$mo=htmlspecialchars($_GET['mo']) ; if (!$mo){ $mo=date(m); } 
$dy=htmlspecialchars($_GET['dy']) ; if (!$dy){ $dy=date(d); } 
$hr=htmlspecialchars($_GET['hr']) ; if (!$hr){ $hr=date(H)-1;} 
if( $hr < "0" ){$hr=23;$dy=sprintf("%02d",$dy-1);};
$yr=sprintf("%04d", $yr); 
$mo=sprintf("%02d", $mo); 
$dy=sprintf("%02d", $dy); 
$hr=sprintf("%02d", $hr); 
?>
<TITLE>Seismogram Search </TITLE>
<?php include("../GTEQheader.html"); ?>
<form action="<?php $PHP_SELF; ?>" method="get">
<ul> <li>  Station: <select name="STAT" >
	  <optgroup label="select"  >
		<?php 
	            echo "<option value=\"$STAT\">$STAT</option>\n"; //print the default (or previously chosen) option first
		    $statfile="stations.xml" ; //xml file that contains station info
		     if (file_exists("$statfile")){ //only work if file exists
		        $fh=fopen("$statfile","r"); //open file for reading
		        #$filetext=fread($fh, filesize($statfile)); // reads in whole thing
		        while ($filetext=fgets($fh)){ //gets one line
		             if ($aa=strpos($filetext, "ntwk=\"GT\"")  && $bb=strpos($filetext, "op=\"OL\"")){ //if GT net and online
		           	 $namepos=strpos($filetext, "name=");  //position of name field 
		           	 $STATLONG=substr($filetext,$namepos+6,6); //get long name that has 6 characters
		           	 $nametailpos=strpos($STATLONG,"\"");  //find where tailing " sits
		           	 $STATname=substr($STATLONG,0,$nametailpos); //remove tail from " position
		           	 if ( "$STATname" != "$STAT" ){  // if not the default station, add to option list
		           	     echo "		<option value=\"$STATname\">$STATname</option>\n";
		           	 }
		           	 # print($STATname);
		           	 #print($filetext);
		             }
		         }
		     }else {echo "$statfile doesn't exist";}
		 ?>
	   </optgroup>
         </select>
	year:     <input type="text" size=3 name="yr" value="<?php echo $yr ?>" />
	month:    <input type="text" size=1 name="mo" value="<?php echo $mo ?>" />
	day:      <input type="text" size=1 name="dy" value="<?php echo $dy ?>" />
	hour(UTC):<input type="text" size=1 name="hr" value="<?php echo $hr ?>" />
	<input type="submit" value="view data" /></ul>
</form>
<?php 
$filebig="rt${STAT}.${yr}${mo}${dy}.${hr}.png" ;
$filesmall="rt${STAT}_sm.${yr}${mo}${dy}.${hr}.png";
/* below YEARMO directory structure added by AVN 4/25/2020 */
$YEARMO="${yr}/${mo}";
if (file_exists("old/$YEARMO/$filesmall")) {
     echo "<a href=RTNET/old/$YEARMO/$filebig><img src=RTNET/old/$YEARMO/$filesmall border=0></a>";
} else { 
     echo "Sorry, the file $filesmall does not exist.  The station may have been down.";
}
?>
<table border=0 cellspacing=0 cellpadding=0 width=100%><TR>
<td ><a href=RTNET/waveformsearch.php?<?php if( $hr > "0" ){$hrm1=sprintf("%02d",$hr-1);$dym1=$dy;}else{$hrm1=23;$dym1=sprintf("%02d",$dy-1);}; echo("STAT=$STAT&yr=$yr&mo=$mo&dy=$dym1&hr=$hrm1"); ?>>previous hour</a></td>
<td><center><h3><?php echo "$yr/$mo/$dy ${hr}hr" ?></h3></center></td>
<td align=right><a href=RTNET/waveformsearch.php?<?php if ( $hr < "23" ){sprintf("%02d",$hrp1=$hr+1);$dyp1=$dy;}else{$hrp1="00";$dyp1=sprintf("%02d",$dy+1);}; echo("STAT=$STAT&yr=$yr&mo=$mo&dy=$dyp1&hr=$hrp1"); ?>>next hour</a></td>
</tr></table>


<center>
  <table border=0 cellspacing=0 cellpadding=0><TR><td width=700>
    <?php echo "$DEFAULTLINE" ?>
    <br> <b> Archived waveform <i>images</i> for station <?php echo $STAT ?></b>
    <br>
    Note: spectrogram is unfiltered.
    <br>
    <ul><b> More Data</b>
    <li> <A href=RTNET/last24.php?STAT=<?php echo $STAT ?>>Last 24 hours of data for station <?php echo $STAT ?>.</a>
	<li> <A href=Stations/>Station locations and data for available Georgia stations</a>
    </ul>
  </td></tr></table>
</center>

<?php include("../GTEQfooter.html"); ?>
