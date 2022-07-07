powershell.exe Set-ExecutionPolicy -ExecutionPolicy bypass -Scope CurrentUser

$channels = @(
    "https://www.youtube.com/c/aliensrock",
    "https://www.youtube.com/c/EntertainTheElk",
    "https://www.youtube.com/c/Nerdstalgic",
    "https://www.youtube.com/c/F1",
    "https://www.youtube.com/c/CasuallyExplained",
    "https://www.youtube.com/c/Wendoverproductions",
    "https://www.youtube.com/c/inanutshell",
    "https://www.youtube.com/user/BostonDynamics",
    "https://www.youtube.com/c/StuffMadeHere",
    "https://www.youtube.com/c/MrBeast6000",
    "https://www.youtube.com/c/SifdGaming",
    "https://www.youtube.com/c/MattDAvella",
    "https://www.youtube.com/c/Woolie",
    "https://www.youtube.com/c/TradesbyMatt",
    "https://www.youtube.com/c/LinusTechTips"
)

$API_URL = 'http://127.0.0.1:5000'

forEach ($channel in $channels){
    $query = $API_URL + '/channels/add?url=' + $channel
    Invoke-WebRequest -Uri $query -Method GET
}

$range = 1
$query2 = $API_URL + 'download/latest?range=' + $range + '&id=all'
Invoke-WebRequest -Uri  $API_URL -Method GET