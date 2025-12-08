// static/script.js

document.addEventListener("DOMContentLoaded", () => {
    const questionInput = document.getElementById("question");
    const askBtn = document.getElementById("ask-btn");
    const answerBox = document.getElementById("answer-box");
    const statusDot = document.getElementById("status-dot");
    const statusLabel = document.getElementById("status-label");
    const statusMode = document.getElementById("status-mode");

    function setIdle() {
        statusDot.classList.remove("loading");
        statusLabel.textContent = "Waiting for your question…";
        statusMode.textContent = "Idle";
    }

    function setLoading() {
        statusDot.classList.add("loading");
        statusLabel.innerHTML =
            'Analyzing your course transcripts… <span class="loading-dots"><span></span><span></span><span></span></span>';
        statusMode.textContent = "Thinking";
    }

    async function sendQuestion() {
        const question = questionInput.value.trim();
        if (!question) {
            answerBox.innerHTML =
                '<span class="error-text">Please enter a question related to your Optical Communication course.</span>';
            statusLabel.textContent = "No question provided";
            statusMode.textContent = "Idle";
            statusDot.classList.remove("loading");
            return;
        }

        // UI: loading state
        askBtn.disabled = true;
        setLoading();
        answerBox.innerHTML =
            '<span class="answer-empty">The assistant is preparing an answer based on the most relevant video segments…</span>';

        try {
            const res = await fetch("/ask", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ question }),
            });

            const data = await res.json();

            if (!res.ok || data.error) {
                answerBox.innerHTML =
                    '<span class="error-text">Error: ' +
                    (data.error || "Something went wrong on the server.") +
                    "</span>";
                statusLabel.textContent = "Something went wrong";
                statusMode.textContent = "Error";
                statusDot.classList.remove("loading");
                return;
            }

            // Show answer
            answerBox.textContent = data.answer;
            statusLabel.textContent = "Response generated";
            statusMode.textContent = "Done";
            statusDot.classList.remove("loading");
        } catch (err) {
            console.error(err);
            answerBox.innerHTML =
                '<span class="error-text">Network error: could not reach the server.</span>';
            statusLabel.textContent = "Network error";
            statusMode.textContent = "Error";
            statusDot.classList.remove("loading");
        } finally {
            askBtn.disabled = false;
        }
    }

    askBtn.addEventListener("click", sendQuestion);

    // Ctrl+Enter to send
    questionInput.addEventListener("keydown", (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
            e.preventDefault();
            sendQuestion();
        }
    });

    // Initial state
    setIdle();
});
