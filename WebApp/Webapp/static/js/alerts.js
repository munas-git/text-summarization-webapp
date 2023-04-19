if (document.getElementById("alert").textContent == "invalid"){
    const alert_message = "Ensure text is long enough and contains valid characters or check file format."
    alert(alert_message)
}


// Alert function for textarea max length.
function lengthCheck(){
    text = document.getElementById("summary-text-area").value
    var count = 0;
    var split = text.split(' ');

    for (var i = 0; i < split.length; i++) {
        if (split[i] != "") {
            count ++;
        }
    }
    if (count >= 1500) {
        characters_length = text.length
        alert("You have exceeded 1,500 words, only the first 1,500 will be considered.");
    }
}

// Get all inputs that have a word limit
// document.querySelectorAll('textarea[data-max-words]').forEach(input => {
//     // Remember the word limit for the current input
//     let maxWords = parseInt(input.getAttribute('data-max-words') || 0)
//     // Add an eventlistener to test for key inputs
//     input.addEventListener('keydown', e => {
//       let target = e.currentTarget
//       // Split the text in the input and get the current number of words
//       let words = target.value.split(/\s+/).length
//       // If the word count is > than the max amount and a space is pressed
//       // Don't allow for the space to be inserted
//       if (!target.getAttribute('data-announce'))
//         // Note: this is a shorthand if statement
//         // If the first two tests fail allow the key to be inserted
//         // Otherwise we prevent the default from happening
//         words >= maxWords && e.keyCode == 32 && e.preventDefault()
//       else
//         words >= maxWords && e.keyCode == 32 && (e.preventDefault() || alert('Word Limit Reached'))
//     })
//   })