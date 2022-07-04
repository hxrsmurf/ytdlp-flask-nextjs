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
    "https://www.youtube.com/c/Woolie"
)

$API_URL = 'http://127.0.0.1:5000/'

forEach ($channel in $channels){
    $query = $API_URL + 'channels?search=' + $channel
    Invoke-WebRequest -Uri $query -METHOD GET
}