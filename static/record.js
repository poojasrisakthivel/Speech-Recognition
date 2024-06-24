// static/record.js
function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            const mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();

            const audioChunks = [];
            mediaRecorder.addEventListener("dataavailable", event => {
                audioChunks.push(event.data);
            });

            mediaRecorder.addEventListener("stop", () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const audioUrl = URL.createObjectURL(audioBlob);
                const audio = new Audio(audioUrl);
                const audioInput = document.getElementById('audio');
                const file = new File([audioBlob], "audio.wav", { type: 'audio/wav' });

                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(file);
                audioInput.files = dataTransfer.files;

                document.querySelector('form').submit();  // Automatically submit the form after recording
            });

            setTimeout(() => {
                mediaRecorder.stop();
            }, 5000);  // Stop recording after 5 seconds
        });
}
