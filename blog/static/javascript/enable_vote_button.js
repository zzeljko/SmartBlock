function enableButton(evt, vote_button_id) {
    
    var vote_button;

    vote_button = document.getElementById("submit_vote_" + vote_button_id);
    vote_button.removeAttribute('disabled');
}