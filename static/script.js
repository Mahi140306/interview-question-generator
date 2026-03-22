function startVoice(btn) {
    let recognition = new webkitSpeechRecognition();
    recognition.lang = "en-US";

    recognition.onresult = function(event) {
        let text = event.results[0][0].transcript;
        btn.previousElementSibling.value = text;
    };

    recognition.start();
}