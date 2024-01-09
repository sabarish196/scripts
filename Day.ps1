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
