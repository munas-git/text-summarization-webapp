var count = 0

function playButton(){
    if(count == 0){
        count = 1;
        var text = document.getElementById('summaryContent').innerHTML;
        responsiveVoice.speak(text);
        document.getElementById("playPause").className = "fa fa-pause"
    }
    else if(count==1){
        count = 2;
        responsiveVoice.pause();
        document.getElementById("playPause").className = "fa fa-play-circle"
    }
    else{
        count = 1;
        responsiveVoice.resume();
        document.getElementById("playPause").className = "fa fa-pause"
    }
}


function stopSpeech(){
    count = 0;
    responsiveVoice.cancel();
    document.getElementById("playPause").className = "fa fa-play-circle"
}