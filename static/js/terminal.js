document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("terminal-form");
    const input = document.getElementById("command-input");
    const output = document.getElementById("terminal-output");

    let traceTimer = null;
    let countdown = 5;
    let lastCommand = "";

    // -----------------------------
    // TYPEWRITER EFFECT (STORY MODE)
    // -----------------------------
    function typeLine(text, className = "") {
        return new Promise((resolve) => {
            const p = document.createElement("p");

            if (className) p.classList.add(className);

            output.appendChild(p);
            let i = 0;

            const interval = setInterval(() => {
                p.textContent += text.charAt(i);
                i++;

                output.scrollTop = output.scrollHeight;

                if (i >= text.length) {
                    clearInterval(interval);
                    resolve();
                }
            }, 14); // سرعت تایپ
        });
    }

    // multi-line typing
    async function typeBlock(block) {
        const lines = block.split("\n");
        for (let line of lines) {
            await typeLine(line);
        }
    }

    // print instantly (for user commands)
    function printInstant(text, className = "") {
        const p = document.createElement("p");
        if (className) p.classList.add(className);
        p.textContent = text;
        output.appendChild(p);
        output.scrollTop = output.scrollHeight;
    }

    // -----------------------------
    // TRACE TIMER (STORY WARNING)
    // -----------------------------
    function startTrace() {
        document.body.classList.add("trace-active");

        countdown = 5;
        printInstant(`TRACE TIMER: ${countdown} seconds`, "alert");

        traceTimer = setInterval(() => {
            countdown--;
            printInstant(`TRACE TIMER: ${countdown}...`, "alert");

            if (countdown <= 0) {
                clearInterval(traceTimer);
                traceTimer = null;
                document.body.classList.remove("trace-active");
                window.location.href = "/detected";
            }
        }, 1000);
    }

    function stopTrace() {
        if (traceTimer) {
            clearInterval(traceTimer);
            traceTimer = null;
        }
        document.body.classList.remove("trace-active");
    }

    // -----------------------------
    // HANDLE FORM SUBMISSION
    // -----------------------------
    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const command = input.value.trim();
        if (!command) return;

        lastCommand = command;

        printInstant(">> " + command);
        input.value = "";

        try {
            const response = await fetch("/api/command", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ command })
            });

            const data = await response.json();

            // story typed response
            if (data.response) {
                await typeBlock(data.response);
            }

            // trace start
            if (data.trace) {
                startTrace();
            }

            // cancel trace if disconnect
            if (command === "disconnect") {
                stopTrace();
            }

            // redirect (for endings + detected)
            if (data.redirect) {
                setTimeout(() => {
                    window.location.href = data.redirect;
                }, 600);
            }

        } catch (err) {
            printInstant("CONNECTION FAILURE. SIGNAL LOST.", "alert");
        }
    });

    // ↑ previous command
    input.addEventListener("keydown", (e) => {
        if (e.key === "ArrowUp") {
            e.preventDefault();
            input.value = lastCommand;
        }
    });

});
