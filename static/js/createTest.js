let auto;
let baseUrl;

function automatic(link) {
    auto = true;
    baseUrl = link;
    createQuestion();
}

function manual(link) {
    auto = false;
    baseUrl = link;
    createQuestion();
}

function createQuestion() {

    markButtonAsPressed();

    let questions = document.getElementById('questions');

    questions.innerHTML = "";

    getQuestionCount().then((data) => {
        for (let i = 1; i < parseInt(data) + 1; i++) {

            let currentDiv = document.createElement("div");
            currentDiv.className = "row mb-3";

            let questionNumberDiv = createNumberDiv(i);
            currentDiv.appendChild(questionNumberDiv);

            createSelectDiv(i, currentDiv);



            questions.appendChild(currentDiv);
        }
    });
}

function markButtonAsPressed() {
    let autoButton = document.getElementById("autoBtn");
    let manualButton = document.getElementById("manualBtn");

    if (auto) {
        autoButton.className = "btn btn-success col-5";
        manualButton.className = "btn btn-outline-warning col-5";
    } else {
        autoButton.className = "btn btn-outline-success col-5";
        manualButton.className = "btn btn-warning col-5";
    }
}

function getQuestionCount() {
    let subject = document.getElementById('subject_select')

    return fetch(baseUrl + '/subject/' + subject.value)
        .then((response) => {
            return response.json();
        })
        .then((data) => {
                return data;
            }
        );
}

function createNumberDiv(number) {
    let questionNumberDiv = document.createElement("div");
    questionNumberDiv.className = "col-1";
    let questionNumber = document.createElement("input");
    questionNumber.type = "text";
    questionNumber.value = number;
    questionNumber.disabled = true;
    questionNumber.className = "form-control-plaintext";
    questionNumber.name = "number" + number;
    questionNumberDiv.appendChild(questionNumber);
    return questionNumberDiv;
}

function createSelectDiv(number, row) {

    let selectDiv = document.createElement("div");
    selectDiv.className = "col-9";
    let select = document.createElement("select");
    select.className = "form-select";
    select.name = "question" + number;
    select.innerHTML = "";

    select.onchange = function() {
        let infoDiv = document.getElementById("info" + number);
        infoDiv.href = baseUrl + "/question/" + select.value;
    }

    let infoButtonDiv = document.createElement("div");



    feelSelect(number, select, infoButtonDiv);
    // fillInfoButtonDiv(number, infoButtonDiv);

    selectDiv.appendChild(select);

    row.appendChild(selectDiv);
    row.appendChild(infoButtonDiv);

    // return selectDiv;
}

function feelSelect(number, select,infoButtonDiv) {
    let subject = document.getElementById('subject_select')

    fetch(baseUrl + '/subject/' + subject.value + '/question/' + number)
        .then((response) => {
            return response.json();
        })
        .then((data) => {
                for (let key in data) {
                    let option = document.createElement("option");
                    option.text = data[key];
                    option.value = key;
                    select.add(option);
                }
                if (auto) {
                    select.selectedIndex = Math.floor(Math.random() * Object.keys(data).length);
                    fillInfoButtonDiv(select.value, infoButtonDiv, number);
                } else {
                    fillInfoButtonDiv(select.value, infoButtonDiv, number);
                    let option = document.createElement("option");
                    option.text = "Выберите вопрос";
                    option.value = "0";
                    option.selected = true;
                    select.add(option);
                }
            }
        );
}

function fillInfoButtonDiv(number, infoButtonDiv, currNum) {
    infoButtonDiv.className = "col-2";
    let infoLink = document.createElement("a");
    infoLink.id = "info" + currNum;
    infoLink.href = baseUrl + "/question/" + number;
    infoLink.target = "_blank"
    infoLink.className = "btn btn-outline-info";
    infoLink.innerText = "инфо"

    infoButtonDiv.appendChild(infoLink);
    return infoButtonDiv;
}