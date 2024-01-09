function ConvertToFullDayName($dayAbbreviation) {
    switch -Wildcard ($dayAbbreviation.ToLower()) {
        'sun*' { return 'Sunday' }
        'mon*' { return 'Monday' }
        'tue*' { return 'Tuesday' }
        'wed*' { return 'Wednesday' }
        'thu*' { return 'Thursday' }
        'fri*' { return 'Friday' }
        'sat*' { return 'Saturday' }
        default { return 'Invalid Day Abbreviation' }
    }
}

# Example usage:
$dayAbbreviation = "fri"
$fullDay = ConvertToFullDayName $dayAbbreviation
Write-Host "Full Day: $fullDay"


$currentDay = (Get-Date).DayOfWeek
$currentHour = (Get-Date).Hour

# Define your specific days and times
$startDay = 'Thursday'
$startTime = 18  # 6:00 PM
$endDay = 'Tuesday'
$endTime = 8    # 8:00 AM

if (
    ($currentDay -eq $startDay -and $currentHour -ge $startTime) -or
    ($currentDay -eq $endDay -and $currentHour < $endTime) -or
    ($currentDay -gt $startDay -and $currentDay -lt $endDay)
) {
    Write-Host "Yes"
}
