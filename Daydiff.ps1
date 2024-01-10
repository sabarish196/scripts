# Get user input for start day and hour
$startDayHour = Read-Host "Enter the start day and hour (e.g., Friday 08):"
$startDay, $startHour = $startDayHour -split ' '

# Get user input for end day and hour
$endDayHour = Read-Host "Enter the end day and hour (e.g., Monday 16):"
$endDay, $endHour = $endDayHour -split ' '

# Map days to numerical values
$daysOfWeek = @("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
$startDayNum = $daysOfWeek.IndexOf($startDay)
$endDayNum = $daysOfWeek.IndexOf($endDay)

# Calculate time difference in hours
$timeDifferenceInHours = ($endDayNum * 24 + [int]$endHour) - ($startDayNum * 24 + [int]$startHour)

# Display the result
Write-Output "Time difference: $timeDifferenceInHours hours"
