$(document).ready(function () {

  // ==================================================
  // TEXTILLATE
  // ==================================================

  $('.text').textillate({
    loop: true,
    speed: 1500,
    sync: true,
    in: {
      effect: "bounceIn"
    },
    out: {
      effect: "bounceOut"
    },
  });


  $('.siri-message').textillate({
    loop: true,
    speed: 1500,
    sync: true,
    in: {
      effect: "fadeInUp",
      sync: true,
    },
    out: {
      effect: "fadeOutUp",
      sync: true,
    },
  });


  // ==================================================
  // SIRI WAVE
  // ==================================================

  var siriWave = new SiriWave({
    container: document.getElementById("siri-container"),
    width: 940,
    style: "ios9",
    amplitude: "1",
    speed: "0.30",
    height: 200,
    autostart: true,
    waveColor: "#ff0000",
    waveOffset: 0,
    rippleEffect: true,
    rippleColor: "#ffffff",
  });


  // ==================================================
  // CHAT HISTORY
  // ==================================================

  const chatHistory = document.getElementById("chatHistory");


  function saveChat(sender, message) {

    console.log("SAVING CHAT:", sender, message);

    if (!message || message.trim() === "") {
        console.log("Empty message - not saved");
        return;
    }

    let chats =
      JSON.parse(localStorage.getItem("jarvisChats")) || [];

    chats.push({
      sender: sender,
      message: message,
      time: new Date().toLocaleTimeString()
    });

    localStorage.setItem(
      "jarvisChats",
      JSON.stringify(chats)
    );

    displayChat(sender, message);
  }


  // Display chat in sidebar
  function displayChat(sender, message) {

    if (!chatHistory) {
      console.log("chatHistory element not found");
      return;
    }

    const messageBox = document.createElement("div");

    if (sender === "YOU") {

      messageBox.className =
        "jarvis-chat-message user-message";

      messageBox.innerHTML = `
        <div class="message-title">
          <i class="bi bi-person"></i> YOU
        </div>

        <div class="message-text">
          ${escapeHTML(message)}
        </div>
      `;

    } else {

      messageBox.className =
        "jarvis-chat-message jarvis-message";

      messageBox.innerHTML = `
        <div class="message-title">
          <i class="bi bi-robot"></i> JARVIS
        </div>

        <div class="message-text">
          ${escapeHTML(message)}
        </div>
      `;
    }

    chatHistory.appendChild(messageBox);

    // Scroll to latest message
    const sidebarBody =
      document.querySelector(".jarvis-sidebar-body");

    if (sidebarBody) {
      sidebarBody.scrollTop =
        sidebarBody.scrollHeight;
    }
  }


  // Security: prevent HTML inside messages
  function escapeHTML(text) {

    return $("<div>")
      .text(text)
      .html();

  }


  // Load previous chats
  function loadChatHistory() {

    if (!chatHistory) {
      console.log("Chat history element not found.");
      return;
    }

    let chats =
      JSON.parse(localStorage.getItem("jarvisChats")) || [];

    chatHistory.innerHTML = "";

    chats.forEach(function (chat) {

      displayChat(
        chat.sender,
        chat.message
      );

    });

  }


  // Load chats when page starts
  loadChatHistory();


  // ==================================================
  // MICROPHONE BUTTON
  // ==================================================

  $("#MicBtn").click(function () {

    eel.play_assistant_sound();

    $("#Oval").attr("hidden", true);
    $("#SiriWave").attr("hidden", false);

    // FIXED
    eel.takeAllCommands();

  });


  // ==================================================
  // KEYBOARD SHORTCUT
  // ==================================================

  function doc_keyUp(e) {

    if (e.key === "j" && e.metaKey) {

      eel.play_assistant_sound();

      $("#Oval").attr("hidden", true);
      $("#SiriWave").attr("hidden", false);

      // FIXED
      eel.takeAllCommands();

    }

  }

  document.addEventListener(
    "keyup",
    doc_keyUp,
    false
  );


  // ==================================================
  // PYTHON -> JAVASCRIPT
  // ==================================================

  eel.expose(senderText);

  function senderText(message) {

    $(".sender_message").text(message);

  }


 // ==================================================
// JARVIS RESPONSE FROM PYTHON
// ==================================================

eel.expose(jarvisResponse);

function jarvisResponse(message) {

    console.log("=================================");
    console.log("JARVIS RESPONSE RECEIVED:");
    console.log(message);
    console.log("=================================");

    if (!message) {
        console.log("Empty JARVIS response");
        return;
    }

    saveChat("JARVIS", message);
}


  // ==================================================
  // SEND MESSAGE
  // ==================================================

  function PlayAssistant(message) {

    if (message != "") {

      // Save USER message
      saveChat(
        "YOU",
        message
      );


      $("#Oval").attr(
        "hidden",
        true
      );

      $("#SiriWave").attr(
        "hidden",
        false
      );


      // Send to Python
      eel.takeAllCommands(message);


      // Clear input
      $("#chatbox").val("");


      $("#MicBtn").attr(
        "hidden",
        false
      );

      $("#SendBtn").attr(
        "hidden",
        true
      );

    } else {

      console.log(
        "Empty message, nothing sent."
      );

    }

  }


  // ==================================================
  // SHOW / HIDE SEND BUTTON
  // ==================================================

  function ShowHideButton(message) {

    if (message.length == 0) {

      $("#MicBtn").attr(
        "hidden",
        false
      );

      $("#SendBtn").attr(
        "hidden",
        true
      );

    } else {

      $("#MicBtn").attr(
        "hidden",
        true
      );

      $("#SendBtn").attr(
        "hidden",
        false
      );

    }

  }


  // ==================================================
  // CHATBOX INPUT
  // ==================================================

  $("#chatbox").keyup(function () {

    let message =
      $("#chatbox").val();

    console.log(
      "Current chatbox input:",
      message
    );

    ShowHideButton(message);

  });


  // ==================================================
  // SEND BUTTON
  // ==================================================

  $("#SendBtn").click(function () {

    let message =
      $("#chatbox").val();

    PlayAssistant(message);

  });


  // ==================================================
  // ENTER KEY
  // ==================================================

  $("#chatbox").keypress(function (e) {

    if (e.which == 13) {

      let message =
        $("#chatbox").val();

      PlayAssistant(message);

    }

  });

  // ==================================================
// VOICE COMMAND FROM PYTHON
// ==================================================

eel.expose(userChatMessage);

function userChatMessage(message) {

    console.log("VOICE MESSAGE RECEIVED:", message);

    if (!message || message.trim() === "") {
        return;
    }

    saveChat("YOU", message);
}

});