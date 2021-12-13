let hidden = true;

function passwordLogin(iconId, inputId) {
    let icon = document.getElementById(iconId)
    let input = document.getElementById(inputId)
    if (hidden) {
        icon.className = "bi bi-eye";
        input.type = 'text'
        hidden = !hidden;
    } else {
        icon.className = "bi bi-eye-slash";
        input.type = 'password'
        hidden = !hidden;
    }
}

let hiddenReg = true;

function passwordRegistration(iconId, inputId) {
    let icon1 = document.getElementById(iconId + '1');
    let icon2 = document.getElementById(iconId + '2');
    let input1 = document.getElementById(inputId + '1');
    let input2 = document.getElementById(inputId + '2');
    if (hiddenReg) {
        icon1.className = "bi bi-eye";
        icon2.className = "bi bi-eye";
        input1.type = 'text'
        input2.type = 'text'
        hiddenReg = !hiddenReg;
    } else {
        icon1.className = "bi bi-eye-slash";
        icon2.className = "bi bi-eye-slash";
        input1.type = 'password'
        input2.type = 'password'
        hiddenReg = !hiddenReg;
    }
}

function checkPassword(inputId, feedbackId) {
    let input1 = document.getElementById(inputId + '1');
    let input2 = document.getElementById(inputId + '2');
    let feedbackElement = document.getElementById(feedbackId)

    if (input1.value  === input2.value) {
        feedbackElement.style.display = 'none'
        input2.className = "form-control is-valid";
    } else {
        feedbackElement.style.display = 'block'
        input2.className = "form-control is-invalid";
    }

}