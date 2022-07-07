powershell.exe Set-ExecutionPolicy -ExecutionPolicy bypass -Scope CurrentUser

$channels = @(
    "https://www.youtube.com/c/20thCenturyStudios",
    "https://www.youtube.com/c/aliensrock",
    "https://www.youtube.com/c/AppleTV",
    "https://www.youtube.com/user/BostonDynamics",
    "https://www.youtube.com/c/NBCBrooklyn99",
    "https://www.youtube.com/c/captainmidnight",
    "https://www.youtube.com/c/CasuallyExplained",
    "https://www.youtube.com/c/ControlledPairsGaming",
    "https://www.youtube.com/c/Dave2D",
    "https://www.youtube.com/c/DougDeMuro",
    "https://www.youtube.com/c/EntertainTheElk",
    "https://www.youtube.com/c/F1",
    "https://www.youtube.com/c/Freecodecamp",
    "https://www.youtube.com/c/Garbaj",
    "https://www.youtube.com/c/GreyMrFreeze",
    "https://www.youtube.com/c/GrowlingSidewinder",
    "https://www.youtube.com/c/halfasinteresting",
    "https://www.youtube.com/user/HBO",
    "https://www.youtube.com/c/hbomax",
    "https://www.youtube.com/c/JebBrooksGreenerGrass",
    "https://www.youtube.com/c/jfavignano",
    "https://www.youtube.com/c/karmakut/videos",
    "https://www.youtube.com/c/KarstenRunquist",
    "https://www.youtube.com/c/KeepYourDaydreamTv",
    "https://www.youtube.com/c/Iliketomakestuff",
    "https://www.youtube.com/c/inanutshell",
    "https://www.youtube.com/c/lauvsongs",
    "https://www.youtube.com/c/LemursCorner",
    "https://www.youtube.com/c/Level1Techs",
    "https://www.youtube.com/c/LikeStoriesofOld",
    "https://www.youtube.com/c/LinusTechTips",
    "https://www.youtube.com/c/mkbhd",
    "https://www.youtube.com/c/marvel",
    "https://www.youtube.com/c/MattDAvella",
    "https://www.youtube.com/channel/UCL_BZpt0J9Kqwy6YPWr30ow",
    "https://www.youtube.com/c/MichelleKhare",
    "https://www.youtube.com/c/MrBeast6000",
    "https://www.youtube.com/c/MyPlayHouse",
    "https://www.youtube.com/c/NASA",
    "https://www.youtube.com/c/Nerdstalgic",
    "https://www.youtube.com/c/Netflix",
    "https://www.youtube.com/user/penguinz0",
    "https://www.youtube.com/c/RacesVideos",
    "https://www.youtube.com/c/RealCivilEngineerGaming",
    "https://www.youtube.com/c/RedKiteRender",
    "https://www.youtube.com/c/rndThursday",
    "https://www.youtube.com/c/SifdGaming",
    "https://www.youtube.com/c/Spudknocker",
    "https://www.youtube.com/c/StuffMadeHere",
    "https://www.youtube.com/c/TED",
    "https://www.youtube.com/c/TheOntarioGardener",
    "https://www.youtube.com/c/ThePrimeagen",
    "https://www.youtube.com/c/TomScottGo",
    "https://www.youtube.com/c/TorniQuetHD",
    "https://www.youtube.com/c/TradesbyMatt",
    "https://www.youtube.com/c/TraversyMedia",
    "https://www.youtube.com/c/WebDevSimplified",
    "https://www.youtube.com/c/Wendoverproductions",
    "https://www.youtube.com/c/Wirtual",
    "https://www.youtube.com/c/Woolie"
)


$API_URL = 'http://127.0.0.1:5000'

forEach ($channel in $channels){
    $query = $API_URL + '/channels/add?url=' + $channel
    Invoke-WebRequest -Uri $query -Method GET
}

$range = 1
$query2 = $API_URL + 'download/latest?range=' + $range + '&id=all'
Invoke-WebRequest -Uri  $API_URL -Method GET