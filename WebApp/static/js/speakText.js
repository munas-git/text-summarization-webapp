function speakText(){
    var text = document.getElementById('summaryContent').innerHTML;
    responsiveVoice.speak(text);
    
}


function stopSpeech(){
    const test = responsiveVoice.pause();  
    console.log(test)  
}


function resumeSpeech(){
    responsiveVoice.resume();
}