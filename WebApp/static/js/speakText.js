function speakText(){
    var text = document.getElementById('summaryContent').innerHTML;
    responsiveVoice.speak(text);
    
}


function stopSpeech(){
    responsiveVoice.pause();    
}


function resumeSpeech(){
    responsiveVoice.resume();
}