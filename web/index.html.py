<!DOCTYPE html>
<html>
<head>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
</head>
<body style="background:#111;color:white;text-align:center">

<h1>🎰 PLINKO</h1>

<input id="bet" placeholder="Ставка"><br><br>
<button onclick="play()">Грати</button>

<p id="result"></p>

<script>
function play(){
let bet=document.getElementById("bet").value;

fetch("/plinko",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
bet:bet,
user_id:Telegram.WebApp.initDataUnsafe.user?.id
})
})
.then(r=>r.json())
.then(d=>{
document.getElementById("result").innerText="x"+d.mult+" → "+d.win+"$";
});
}
</script>

</body>
</html>