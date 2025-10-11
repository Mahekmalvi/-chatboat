const chat = document.getElementById("chat");
const form = document.getElementById("composer");
const input = document.getElementById("input");

let cid = localStorage.getItem("cid") || "";

function addMsg(role, text, cards=[]) {
  const div = document.createElement("div");
  div.className = "msg " + role;
  div.innerHTML = `<div class="bubble">${text}</div>`;
  chat.appendChild(div);

  if (cards.length) {
    const wrap = document.createElement("div");
    wrap.className = "cards";
    cards.forEach(c => {
      const card = document.createElement("div");
      card.className = "card";
      card.innerHTML = `
        <img src="${c.image}" alt="">
        <h3>${c.title}</h3>
        <p>${c.subtitle}</p>
        <div class="price">${c.price}</div>
        <a href="${c.url}" target="_blank">Visit</a>
        <a href="${c.pay}" target="_blank">Pay</a>
      `;
      wrap.appendChild(card);
    });
    chat.appendChild(wrap);
  }

  chat.scrollTop = chat.scrollHeight;
}

async function sendMsg(text) {
  addMsg("user", text);
  const res = await fetch("/chat", {
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body: JSON.stringify({cid, msg:text})
  });
  const data = await res.json();
  cid = data.cid;
  localStorage.setItem("cid", cid);
  addMsg("bot", data.reply, data.cards);
}

form.onsubmit = e => {
  e.preventDefault();
  if (input.value.trim()) {
    sendMsg(input.value.trim());
    input.value = "";
  }
};

window.onload = () => {
  if (!cid) {
    setTimeout(()=>addMsg("bot","Hi 👋 I’m your Muskbliss assistant! Let’s find your perfect fragrance. Please tell me your gender."),1200);
  } else {
    // restore old history
    fetch("/chat", {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({cid,msg:""})})
  }
};
