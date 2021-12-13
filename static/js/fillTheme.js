let counterQuestion = 0;
let baseUrl;
let questionCountInSubject

function addQuestion(link) {
    baseUrl = link
    let questions = document.getElementById('questions');
    questions.appendChild(createQuestion())
}

function createQuestion() {
    counterQuestion++;
    let maxQuestionCount = document.getElementById('maxQuestionCount');
    maxQuestionCount.value = counterQuestion;

    let questionDiv = document.createElement('div');
    questionDiv.className = "mb-3"
    questionDiv.id = 'qd' + counterQuestion;


    questionDiv.appendChild(createLabelForQuestionNumberSelect("Номер вопроса"));
    questionDiv.appendChild(createQuestionNumberSelect());
    questionDiv.appendChild(createLabelForQuestionNumberSelect("Вопрос"));
    questionDiv.appendChild(createQuestionSelect());
    questionDiv.appendChild(createDeleteButtonDiv());

    return questionDiv;
}

function createLabelForQuestionNumberSelect(text) {
    let label = document.createElement('label');
    label.innerHTML = text;
    label.className = "form-label";
    return label;
}


function createQuestionNumberSelect() {
    let questionCount = document.getElementById('questionCount')
    let select = document.createElement("select");
    select.id = "qns" + counterQuestion;
    select.className = "form-select mb-3";
    select.innerHTML = "";
    select.onchange = function () {
        feelSelect(select.value, document.getElementById('qs' + select.id.slice(3)));
    }
    let option = document.createElement("option");
    option.text = "Выберите номер вопроса";
    option.value = "-1";
    select.add(option);
    for (let i = 1; i <= questionCount.value; i++) {
        let option = document.createElement("option");
        option.text = i;
        option.value = i;
        select.add(option);
    }

    return select;
}

function createQuestionSelect() {
    let select = document.createElement("select");
    select.id = "qs" + counterQuestion;
    select.name = "qs" + counterQuestion;
    select.className = "form-select mb-3";
    select.innerHTML = "";
    let option = document.createElement("option");
    option.text = "Сначала выберите номер вопроса";
    option.value = "-1";
    select.add(option);
    return select;
}

function createDeleteButtonDiv() {
    let btnDiv = document.createElement("div");
    btnDiv.className = 'd-grid gap-3';

    btnDiv.appendChild(createDeleteButton());

    return btnDiv;
}

function createDeleteButton() {
    let btn = document.createElement("a");
    btn.id = "b" + counterQuestion
    btn.className = "btn btn-outline-danger"
    btn.innerHTML = "Удалить вопрос"
    btn.type = "button";
    btn.onclick = function () {
        let div = document.getElementById('qd' + btn.id.slice(1));
        div.remove();
    }
    return btn;
}


function feelSelect(number, select) {
    let subject = document.getElementById('subject_id')
    let subject_id = subject.value;

    fetch(baseUrl + '/subject/' + subject_id + '/question/' + number)
        .then((response) => {
            return response.json();
        })
        .then((data) => {
                select.innerHTML = "";
                let option = document.createElement("option");
                option.text = "Выберите вопрос";
                option.value = "0";
                option.selected = true;
                select.add(option);
                for (let key in data) {
                    let option = document.createElement("option");
                    option.text = data[key];
                    option.value = key;
                    select.add(option);
                }
            }
        );
}