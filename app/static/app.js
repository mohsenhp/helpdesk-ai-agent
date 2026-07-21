const chat = document.getElementById("chat");
const input = document.getElementById("question");
const button = document.getElementById("send-button");

const newChatButton =
    document.getElementById("new-chat-button");


let conversationId =
    localStorage.getItem("conversation_id");


if (!conversationId) {

    conversationId =
        crypto.randomUUID();

    localStorage.setItem(
        "conversation_id",
        conversationId
    );

}

function resetConversation() {

    conversationId =
        crypto.randomUUID();


    localStorage.setItem(
        "conversation_id",
        conversationId
    );

    localStorage.removeItem(
        "chat_history"
    );


    chat.innerHTML = "";


    addMessage(
        "assistant",
        "Hello! 👋 I started a new conversation. How can I help you?"
    );

}

function saveChatHistory() {

    const messages =
        Array.from(
            document.querySelectorAll(".message")
        )
        .map(message => {

            return {

                role: message.classList.contains("user") ?
                    "user" :
                    "assistant",

                text: message.querySelector(".bubble").textContent

            };

        });


    localStorage.setItem(
        "chat_history",
        JSON.stringify(messages)
    );

}



function loadChatHistory() {

    const history =
        localStorage.getItem(
            "chat_history"
        );


    if (!history) {

        return false;

    }


    const messages =
        JSON.parse(history);


    messages.forEach(message => {

        addMessage(
            message.role,
            message.text
        );

    });


    return true;

}


function addMessage(role, text) {

    const message = document.createElement("div");

    message.className =
        `message ${role}`;


    const avatar = document.createElement("div");

    avatar.className = "avatar";

    avatar.textContent =
        role === "assistant" ?
        "🤖" :
        "🧑";


    const bubble = document.createElement("div");

    bubble.className = "bubble";


    if (role === "assistant") {

        bubble.innerHTML =
            marked.parse(text);

        const copyButton = document.createElement("button");

        copyButton.className = "copy-button";

        copyButton.innerHTML = "📋 Copy";


        copyButton.addEventListener(
            "click",
            async () => {

                await navigator.clipboard.writeText(text);

                copyButton.innerHTML = "✅ Copied";

                setTimeout(() => {

                    copyButton.innerHTML = "📋 Copy";

                }, 2000);

            }
        );


        bubble.appendChild(copyButton);


    } else {

        bubble.textContent =
            text;

    }


    if (role === "assistant") {

        message.appendChild(avatar);
        message.appendChild(bubble);

    } else {

        message.appendChild(bubble);
        message.appendChild(avatar);

    }


    chat.appendChild(message);


    chat.scrollTop =
        chat.scrollHeight;
}


function setThinking(state) {

    if (state) {

        button.disabled = true;
        button.textContent = "Thinking...";

    } else {

        button.disabled = false;
        button.textContent = "Send";

    }

}


async function askQuestion() {

    const question =
        input.value.trim();


    if (!question)
        return;


    addMessage(
        "user",
        question
    );

    const welcome =
        document.getElementById("welcome-screen");


    if (welcome) {

        welcome.remove();

    }


    input.value = "";


    setThinking(true);
    addTypingIndicator();


    try {

        const response =
            await fetch("/ask", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    question: question,

                    conversation_id: conversationId

                })

            });


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Something went wrong"
            );

        }


        removeTypingIndicator();

        addMessage(
            "assistant",
            data.answer
        );


    } catch (error) {

        removeTypingIndicator();

        addMessage(
            "assistant",
            "⚠️ " + error.message
        );

    } finally {

        setThinking(false);

        input.focus();

    }

}



button.addEventListener(
    "click",
    askQuestion
);


input.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            askQuestion();

        }

    }
);



const hasHistory =
    loadChatHistory();


if (!hasHistory) {
    showWelcomeScreen();
}

function addTypingIndicator() {

    const message = document.createElement("div");

    message.id = "typing";

    message.className =
        "message assistant";


    const bubble =
        document.createElement("div");


    bubble.className =
        "bubble typing";


    bubble.innerHTML =
        `
        <span></span>
        <span></span>
        <span></span>
        `;


    message.appendChild(bubble);

    chat.appendChild(message);


    chat.scrollTop =
        chat.scrollHeight;
}


function showWelcomeScreen() {

    const welcome = document.createElement("div");

    welcome.id = "welcome-screen";

    welcome.innerHTML = `

        <div class="welcome-icon">
            🤖
        </div>


        <h2>
            Welcome to HelpDesk AI
        </h2>


        <p>
            Your enterprise AI assistant for
            tickets, incidents, and knowledge base support.
        </p>


        <div class="welcome-features">

            <div>
                🎫
                <span>
                    Analyze tickets
                </span>
            </div>


            <div>
                📚
                <span>
                    Search knowledge base
                </span>
            </div>


            <div>
                🚨
                <span>
                    Investigate incidents
                </span>
            </div>


            <div>
                🔧
                <span>
                    Troubleshoot issues
                </span>
            </div>

        </div>


        <p class="welcome-hint">
            Try asking:
            <br>
            "How many critical VPN tickets are open?"
        </p>

    `;


    chat.appendChild(welcome);

}


function removeTypingIndicator() {

    const typing =
        document.getElementById("typing");


    if (typing) {

        typing.remove();

    }

}

document
    .querySelectorAll(".suggestions button")
    .forEach(button => {

        button.addEventListener(
            "click",
            () => {

                input.value =
                    button.textContent;

                askQuestion();

            }
        );

    });


newChatButton.addEventListener(
    "click",
    resetConversation
);
