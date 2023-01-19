function speakText(){
    var text = document.getElementById('summaryContent').innerHTML;
    responsiveVoice.speak(text);
    
}