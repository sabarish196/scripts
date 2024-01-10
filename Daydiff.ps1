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


$day1 = [System.DayOfWeek]::Friday  # Replace with your first day
$day2 = [System.DayOfWeek]::Monday  # Replace with your second day

if ($day1 -eq $day2) {
    Write-Host "Both days are the same: $day1."
} elseif ($day1 -lt $day2) {
    Write-Host "$day1 comes earlier in the week than $day2."
} else {
    Write-Host "$day1 comes later in the week than $day2."
}



# Get the current date and time
$currentDateTime = Get-Date

# Determine the starting day (any day from today to Saturday)
$startDay = ($currentDateTime.DayOfWeek.value__ + 1) % 7  # Adjust for Sunday as the starting point
$startDateTime = $currentDateTime.AddDays($startDay - $currentDateTime.DayOfWeek.value__).Date.AddHours(16)

# Determine the ending day (any day from tomorrow to Sunday)
$endDay = ($startDay + 1) % 7
$endDateTime = $startDateTime.AddDays(1).Date.AddHours(8)

# Calculate the time difference
$timeDifference = $endDateTime - $startDateTime

# Display the result
Write-Host "Time difference between 16:00 of this week and 08:00 of next week:"
Write-Host "Days: $($timeDifference.Days), Hours: $($timeDifference.Hours), Minutes: $($timeDifference.Minutes)"


# User inputs
$startDay = "Monday"
$stopDay = "Friday"
$startHour = 8
$stopHour = 16

$currentTime = Get-Date
$dayOfWeek = $currentTime.DayOfWeek
$hour = $currentTime.Hour

# Check if the current day is within the specified range and the current time is between startHour and stopHour
if (($dayOfWeek -ge $startDay -and $dayOfWeek -le $stopDay) -and ($hour -ge $startHour -and $hour -lt $stopHour)) {
    # Your code to run during this timeframe
    Write-Host "Executing the task during the specified timeframe."
}
else {
    Write-Host "Not within the specified timeframes."
}

function GetDaysBetweenTwoDays {
    param(
        [string]$startDay,
        [string]$endDay
    )

    $daysOfWeek = [System.DayOfWeek] | Get-Member -Static -MemberType Properties | Select-Object -ExpandProperty Name

    $startIndex = $daysOfWeek.IndexOf($startDay)
    $endIndex = $daysOfWeek.IndexOf($endDay)

    if ($startIndex -eq $endIndex) {
        Write-Output "The start and end days are the same."
        return
    }

    if ($startIndex -lt $endIndex) {
        $result = $daysOfWeek[($startIndex + 1)..($endIndex - 1)]
    } else {
        $result = $daysOfWeek[($startIndex + 1)..($endIndex + 5) % 7]
    }

    Write-Output $result
}

# Example usage:
GetDaysBetweenTwoDays -startDay "Friday" -endDay "Monday"




$startDate = "Friday"
$endDate = "Monday"

$daysOfWeek = [System.DayOfWeek] | Get-Member -Static -MemberType Properties | Select-Object -ExpandProperty Name

$startIndex = $daysOfWeek.IndexOf($startDate)
$endIndex = $daysOfWeek.IndexOf($endDate)

if ($startIndex -lt $endIndex) {
    $result = $daysOfWeek[$startIndex + 1..($endIndex - 1)]
} else {
    $result = $daysOfWeek[($startIndex + 1)..($endIndex + 6)]
}

Write-Output $result



function GetDaysBetweenTwoDays {
    param(
        [string]$startDay,
        [string]$endDay
    )

    $daysOfWeek = [System.DayOfWeek] | Get-Member -Static -MemberType Properties | Select-Object -ExpandProperty Name

    $startIndex = $daysOfWeek.IndexOf($startDay)
    $endIndex = $daysOfWeek.IndexOf($endDay)

    if ($startIndex -eq $endIndex) {
        Write-Output "The start and end days are the same."
        return
    }

    $result = @()

    $currentDayIndex = $startIndex

    while ($currentDayIndex -ne $endIndex) {
        $result += $daysOfWeek[$currentDayIndex]
        $currentDayIndex = ($currentDayIndex + 1) % 7
    }

    Write-Output $result
}

# Example usage:
GetDaysBetweenTwoDays -startDay "Friday" -endDay "Monday"

# Find the current day of the week
$currentDayOfWeek = (Get-Date).DayOfWeek

# Find the days between Friday and Monday
$daysBetween = @()
$daysBetween += $currentDayOfWeek
$currentDayIndex = [Array]::IndexOf([System.DayOfWeek]::GetValues([System.DayOfWeek]), $currentDayOfWeek)

while ($daysBetween[-1] -ne 'Monday') {
    $currentDayIndex = ($currentDayIndex + 1) % 7
    $daysBetween += [System.DayOfWeek]::GetNames([System.DayOfWeek])[$currentDayIndex]
}

Write-Output $daysBetween



function GetDaysBetweenTwoDays {
    param(
        [string]$startDay,
        [string]$endDay
    )

    $daysOfWeek = [System.DayOfWeek]::GetValues([System.DayOfWeek])

    $startIndex = [array]::IndexOf($daysOfWeek, $startDay)
    $endIndex = [array]::IndexOf($daysOfWeek, $endDay)

    if ($startIndex -eq $endIndex) {
        Write-Output "The start and end days are the same."
        return
    }

    $result = @()

    $currentDayIndex = $startIndex

    while ($currentDayIndex -ne $endIndex) {
        $result += $daysOfWeek[$currentDayIndex]
        $currentDayIndex = ($currentDayIndex + 1) % 7
    }

    # Include the end day
    $result += $daysOfWeek[$endIndex]

    Write-Output $result
}

# Example usage:
GetDaysBetweenTwoDays -startDay "Thursday" -endDay "Tuesday"



function GetDaysBetweenTwoDays {
    param(
        [string]$startDay,
        [string]$endDay
    )

    $daysOfWeek = [System.DayOfWeek]::GetValues([System.DayOfWeek])

    $startIndex = [array]::IndexOf($daysOfWeek, $startDay)
    $endIndex = [array]::IndexOf($daysOfWeek, $endDay)

    if ($startIndex -eq $endIndex) {
        Write-Output "The start and end days are the same."
        return
    }

    $result = @()

    $currentDayIndex = $startIndex

    while ($currentDayIndex -ne $endIndex) {
        $result += $daysOfWeek[$currentDayIndex]
        $currentDayIndex = ($currentDayIndex + 1) % 7
    }

    # Include the end day
    $result += $daysOfWeek[$endIndex]

    # Convert to a more human-readable format
    $result = $result | ForEach-Object { [System.DayOfWeek]::$_ }

    Write-Output $result
}

# Example usage:



GetDaysBetweenTwoDays -startDay "Thursday" -endDay "Tuesday"


// Replace these variables with user inputs or dynamic values
$startDay = "Saturday";
$startTime = 12; // 24-hour format
$endDay = "Monday";
$endTime = 4; // 24-hour format

// Current date and time
$currentDay = date("l");
$currentHour = date("G");

// Convert start and end days to timestamp
$startTimestamp = strtotime("next $startDay $startTime:00");
$endTimestamp = strtotime("next $endDay $endTime:00");

// Current timestamp
$currentTimestamp = time();

// Check if current timestamp is within the specified range
if ($currentTimestamp >= $startTimestamp && $currentTimestamp <= $endTimestamp) {
    echo "It's within the specified time range.";
} else {
    echo "It's outside the specified time range.";
}
