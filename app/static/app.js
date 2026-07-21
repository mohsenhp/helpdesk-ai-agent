console.log("HelpDesk AI Chat loaded");

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

                role:
                    message.classList.contains("user")
                        ? "user"
                        : "assistant",

                text:
                    message.querySelector(".bubble").textContent

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
        role === "assistant"
            ? "🤖"
            : "🧑";


    const bubble = document.createElement("div");

    bubble.className = "bubble";


    if (role === "assistant") {

        bubble.innerHTML =
            marked.parse(text);

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


    input.value = "";


    setThinking(true);
    addTypingIndicator();


    try {

        const response =
            await fetch("/ask", {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    question: question,

                    conversation_id:
                        conversationId

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


    } catch(error) {

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

    addMessage(
        "assistant",
        "Hello! 👋 I am your HelpDesk AI assistant. Ask me about tickets, incidents, or knowledge base articles."
    );

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
