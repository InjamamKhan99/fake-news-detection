document.addEventListener("DOMContentLoaded", function () {
    function showLoading(state) {
        document.getElementById("loading").style.display = state ? "block" : "none";
    }

    async function detectFakeNews() {
        const news = document.getElementById("newsInput").value.trim();
        if (!news) {
            alert("Please enter some text.");
            return;
        }
        showLoading(true);
        document.getElementById("result").innerText = "";

        const response = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ news_text: news })
        });

        const data = await response.json();
        const resultText = data.fake ? "Fake News" : "Real News";
        document.getElementById("result").innerText = "Prediction: " + resultText;
        document.getElementById("result").style.color = data.fake ? "red" : "green";
        document.getElementById("feedbackSection").style.display = "block";
        showLoading(false);
    }

    async function factCheckNews() {
        const news = document.getElementById("newsInput").value.trim();
        if (!news) {
            alert("Please enter some text.");
            return;
        }
        showLoading(true);
        document.getElementById("result").innerText = "";

        const response = await fetch("/fact-check", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ news_text: news })
        });

        const data = await response.json();
        document.getElementById("result").innerText = "Fact-Check Result: " + data.result;
        document.getElementById("result").style.color = "blue";
        showLoading(false);
    }

    async function sendFeedback(isCorrect) {
        const news = document.getElementById("newsInput").value;
        await fetch("/feedback", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ news_text: news, correct: isCorrect })
        });
        alert("Feedback submitted. Thank you!");
    }

    document.getElementById("checkBtn").addEventListener("click", detectFakeNews);
    document.getElementById("factBtn").addEventListener("click", factCheckNews);
});

