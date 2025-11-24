// وقتی صفحه لود شد
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("terminal-form");
    const input = document.getElementById("command-input");
    const output = document.getElementById("terminal-output");

    // چاپ یک خط در ترمینال
    function printLine(text) {
        const p = document.createElement("p");
        p.textContent = text;
        output.appendChild(p);
        output.scrollTop = output.scrollHeight; // اسکرول خودکار پایین
    }

    // وقتی کاربر Enter می‌زند
    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const cmd = input.value.trim();
        if (!cmd) return;

        // نمایش دستور تایپ‌شده
        printLine("> " + cmd);
        input.value = "";

        try {
            // ارسال دستور به Flask
            const response = await fetch("/api/command", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ command: cmd })
            });

            const data = await response.json();

            // نمایش خروجی
            printLine(data.response);

        } catch (err) {
            printLine("ERROR: connection lost.");
        }
    });
});
