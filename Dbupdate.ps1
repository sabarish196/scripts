function Update-SqlTableWithOutputs {
    param (
        [string]$ServerName,
        [string]$DatabaseName,
        [string]$Username,
        [string]$Password,
        [string]$TableName,
        [string]$ColumnName,
        [array]$Outputs
    )

    # Construct the SQL update query
    $updateQuery = "UPDATE $TableName SET $ColumnName = @Output"

    $connectionString = "Server=$ServerName;Database=$DatabaseName;User Id=$Username;Password=$Password;"
    $connection = New-Object System.Data.SqlClient.SqlConnection
    $connection.ConnectionString = $connectionString

    try {
        $connection.Open()

        $command = $connection.CreateCommand()
        $command.CommandText = $updateQuery

        # Combine all outputs into a single string
        $combinedOutputs = $Outputs -join ', '
        $command.Parameters.AddWithValue("@Output", $combinedOutputs)

        $affectedRows = $command.ExecuteNonQuery()

        Write-Host "$affectedRows row(s) updated successfully."
    }
    catch {
        Write-Host "Error: $_"
    }
    finally {
        $connection.Close()
    }
}

# Example usage
$outputs = @(Write-Output "Output 1", Write-Output "Output 2", Write-Output "Output 3")
Update-SqlTableWithOutputs -ServerName "<YourServerName>" -DatabaseName "<YourDatabaseName>" -Username "<YourUsername>" -Password "<YourPassword>" -TableName "<YourTableName>" -ColumnName "<YourColumnName>" -Outputs $outputs


# Custom function to capture Write-Output
function Capture-Output {
    param (
        [string]$Message
    )

    $global:CapturedOutputs += $Message
    Write-Output $Message
}

# Redirect Write-Output to the custom function
$function:WriteOutput = $function:Capture-Output

# Your script logic here
Write-Output "Output 1"
Write-Output "Output 2"
Write-Output "Output 3"

# Example usage of captured outputs
Update-SqlTableWithOutputs -ServerName "<YourServerName>" -DatabaseName "<YourDatabaseName>" -Username "<YourUsername>" -Password "<YourPassword>" -TableName "<YourTableName>" -ColumnName "<YourColumnName>" -Outputs $global:CapturedOutputs

