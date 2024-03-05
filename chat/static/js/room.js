console.log("Sanity check from room.js.");

const roomName = JSON.parse(document.getElementById('roomName').textContent);
const roomType = JSON.parse(document.getElementById('roomType').textContent);
const userName = JSON.parse(document.getElementById('userName').textContent);


let chatLog = document.querySelector("#chatLog");
let chatMessageInput = document.querySelector("#chatMessageInput");
let chatMessageSend = document.querySelector("#chatMessageSend");
let onlineUsersSelector = document.querySelector("#onlineUsersSelector");
let onlineUserList = []

// adds a new option to 'onlineUsersSelector'
function onlineUsersSelectorAdd(value) {
    // if (document.querySelector("option[value='" + value + "']")) return;
    // let newOption = document.createElement("option");
    // newOption.value = value;
    // newOption.innerHTML = value;
    // onlineUsersSelector.appendChild(newOption);
    onlineUserList.push(value)
    if (roomType == "private") {
        if (value !== userName) {
            document.querySelector(".roomonlinecount").innerHTML = `online`;
        }
    }
    else {
        if (onlineUserList.length > 1) {
            document.querySelector(".roomonlinecount").innerHTML = `${onlineUserList.length} online`
        }
        else {
            document.querySelector(".roomonlinecount").innerHTML = ``;
        }

    }

}

// removes an option from 'onlineUsersSelector'
function onlineUsersSelectorRemove(value) {
    // let oldOption = document.querySelector("option[value='" + value + "']");
    // if (oldOption !== null) oldOption.remove();

    const index = onlineUserList.indexOf(value);
    if (index > -1) { // only splice array when item is found
        onlineUserList.splice(index, 1); // 2nd parameter means remove one item only
    }
    if (onlineUserList.length > 1) {
        document.querySelector(".roomonlinecount").innerHTML = `${onlineUserList.length} online`;
    }
    else {
        document.querySelector(".roomonlinecount").innerHTML = "";
    }


}

// focus 'chatMessageInput' when user opens the page
chatMessageInput.focus();

// submit if the user presses the enter key
chatMessageInput.onkeyup = function (e) {
    if (e.keyCode === 13) {  // enter key
        chatMessageSend.click();
    }
};

// clear the 'chatMessageInput' and forward the message
chatMessageSend.onclick = function () {
    if (chatMessageInput.value.length === 0) return;
    chatSocket.send(JSON.stringify({
        "message": chatMessageInput.value,
    }));
    chatMessageInput.value = "";
};

function internalMsgSender(msg) {
    if (msg.length === 0) return;
    chatSocket.send(JSON.stringify({
        "message": msg,
    }));
}


function filterMsg(text) {
    var urlRegex = /(https?:\/\/[^\s]+)/g;
    text = text.replace(urlRegex, function (url) {
        return `<a href="${url}">${url}</a>`;
    })

    var tagRegex = /(@[^\s]+)/g;
    text = text.replace(tagRegex, function (tag) {
        let val = tag.slice(1);
        return `<a href='/chat/privatechat/${val}' class='tagtype'>${tag}</a>`;
    })

    return text;

}





let chatSocket = null;

function connect() {
    let websocketprotocol = 'ws://'
    if (window.location.protocol === 'https:') {
        websocketprotocol = 'wss://'
    }
    chatSocket = new WebSocket(websocketprotocol + window.location.host + "/ws/chat/" + roomName + "/");

    chatSocket.onopen = function (e) {
        console.log("Successfully connected to the WebSocket.");
    }

    chatSocket.onclose = function (e) {
        console.log("WebSocket connection closed unexpectedly. Trying to reconnect in 2s...");
        setTimeout(function () {
            console.log("Reconnecting...");
            connect();
        }, 2000);
    };

    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        console.log(data);
        let newchat = document.createElement("div")


        switch (data.type) {
            case "chat_message":
                newchat.classList.add("chat");

                if (userName == data.user) {
                    newchat.classList.add("mychat");
                }

                let curtime = moment().format('HH:MM D MMM, YY');

                let filteredMsg = filterMsg(data.message);
                newchat.innerHTML = `
                <div class="msgdata">
                    <span>${data.user}</span>
                    <p>${filteredMsg}</p>
                </div>
                <div class="othermsgdata">
                    <div>${curtime}</div>
                </div>
                `
                chatLog.appendChild(newchat);
                break;
            case "user_list":
                for (let i = 0; i < data.users.length; i++) {
                    onlineUsersSelectorAdd(data.users[i]);
                }
                break;
            case "user_join":
                newchat.classList.add("notification");
                newchat.innerHTML = `${data.user} joined the chat`;
                chatLog.appendChild(newchat);
                onlineUsersSelectorAdd(data.user);
                break;
            case "user_leave":
                newchat.classList.add("notification");
                newchat.innerHTML = `${data.user} left the chat`;
                chatLog.appendChild(newchat);
                onlineUsersSelectorRemove(data.user);
                break;
            case "private_message":
                newchat.classList.add("chat");
                newchat.classList.add("privatechat");

                newchat.innerHTML = `<span>PM from ${data.user}</span>${data.message}`;
                chatLog.appendChild(newchat);
                break;
            case "private_message_delivered":
                newchat.classList.add("chat");
                newchat.classList.add("mychat");
                newchat.classList.add("myprivatechat");
                newchat.innerHTML = `<span>PM from you</span>${data.message}`;
                chatLog.appendChild(newchat);
                break;
            default:
                console.error("Unknown message type!");
                break;
        }

        // scroll 'chatLog' to the bottom
        chatLog.scrollTop = chatLog.scrollHeight;
    };

    chatSocket.onerror = function (err) {
        console.log("WebSocket encountered an error: " + err.message);
        console.log("Closing the socket.");
        chatSocket.close();
    }
}
connect();

// onlineUsersSelector.onchange = function () {
//     chatMessageInput.value = "/pm " + onlineUsersSelector.value + " ";
//     onlineUsersSelector.value = null;
//     chatMessageInput.focus();
// };
