let balance = 100;
let edge = 0.5;

let player = [];
let dealer = [];

const cards = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"];

function updateBalance() {
    document.getElementById("balance").innerText = balance;
}

// 🎰 PLINKO
function playPlinko() {
    let bet = parseInt(document.getElementById("bet").value);
    if (bet > balance) return alert("Мало грошей");

    balance -= bet;

    let win = Math.random() > edge;

    let result = win ? bet * 2 : 0;
    balance += result;

    drawPlinko();

    setTimeout(() => {
        alert(win ? "Виграв " + result : "Програв");
        updateBalance();
    }, 1000);
}

function drawPlinko() {
    let canvas = document.getElementById("plinko");
    if (!canvas) {
        canvas = document.createElement("canvas");
        canvas.id = "plinko";
        canvas.width = 300;
        canvas.height = 300;
        document.getElementById("game").appendChild(canvas);
    }

    let ctx = canvas.getContext("2d");

    let x = 150;
    let y = 0;

    let interval = setInterval(() => {
        ctx.clearRect(0,0,300,300);

        y += 10;
        x += Math.random() * 20 - 10;

        ctx.beginPath();
        ctx.arc(x,y,5,0,Math.PI*2);
        ctx.fillStyle = "white";
        ctx.fill();

        if (y > 280) clearInterval(interval);
    }, 30);
}

// 🃏 BLACKJACK
function getCard() {
    return cards[Math.floor(Math.random()*cards.length)];
}

function value(c) {
    if (["J","Q","K"].includes(c)) return 10;
    if (c === "A") return 11;
    return parseInt(c);
}

function drawCards() {
    let html = "";

    player.forEach(c => {
        html += `<div style="display:inline-block;padding:10px;background:white;color:black;border-radius:5px;margin:2px">${c}</div>`;
    });

    document.getElementById("cards").innerHTML = html;
}

function startBlackjack() {
    document.getElementById("bjControls").style.display = "block";

    player = [getCard(), getCard()];
    dealer = [getCard()];

    drawCards();
}

function hit() {
    player.push(getCard());
    drawCards();

    if (sum(player) > 21) {
        alert("Програв");
        balance -= 10;
        updateBalance();
    }
}

function stand() {
    while (sum(dealer) < 17) {
        dealer.push(getCard());
    }

    let p = sum(player);
    let d = sum(dealer);

    if (d > 21 || p > d) {
        alert("Виграв!");
        balance += 20;
    } else {
        alert("Програв");
    }

    updateBalance();
}

function sum(arr) {
    return arr.reduce((a,b)=>a+value(b),0);
}

// ⚙️ ADMIN
function setEdge() {
    edge = parseFloat(document.getElementById("edge").value);
    alert("Новий шанс: " + edge);
}

// INIT
updateBalance();