let questionInfoCount = 0;

function showQuestionInfo(questionCount, questionTypes) {

    let typesJson = JSON.parse(questionTypes);

    let questionInfoDiv = document.getElementById("questionInfo");
    questionInfoDiv.innerText = "";

    for (let i = 1; i < parseInt(questionCount) + 1; i++) {
        questionInfoCount++;
        let currentDiv = document.createElement("div");
        currentDiv.className = "row mb-3";

        let questionNumberDiv = document.createElement("div");
        questionNumberDiv.className = "col-1";
        let questionNumber = document.createElement("input");
        questionNumber.type = "text";
        questionNumber.value = i;
        questionNumber.name = "number" + i;
        questionNumber.className = "form-control-plaintext";
        questionNumber.disabled = true;
        questionNumberDiv.appendChild(questionNumber);

        let markDiv = document.createElement("div");
        markDiv.className = "col-5";
        let mark = document.createElement("input");
        mark.type = "text";
        mark.name = "max_mark" + i;
        mark.id = "max_mark" + i;
        mark.placeholder = "Первичный балл";
        mark.onchange = function () {
            showFirstScore();
        }
        mark.required = true;
        mark.className = "form-control";
        markDiv.appendChild(mark);

        let selectDiv = document.createElement("div");
        selectDiv.className = "col-6";
        let select = document.createElement("select");
        select.className = "form-select";
        select.name = "questionType_id" + i;
        select.innerHTML = "";
        for (let id in typesJson) {
            let option = document.createElement("option");
            option.text = typesJson[id];
            option.value = id;
            select.add(option);
        }
        selectDiv.appendChild(select);

        currentDiv.appendChild(questionNumberDiv);
        currentDiv.appendChild(markDiv);
        currentDiv.appendChild(selectDiv);

        questionInfoDiv.appendChild(currentDiv);
    }
}

function showFirstScore() {
    if (isAllQuestionInfoFilled()) {
        let firstTestDiv = document.getElementById("firstTest");
        firstTestDiv.innerText = "";

        let max_score = calcMaxScore()

        for (let i = 0; i < max_score + 1; i++) {
            let currentDiv = document.createElement("div");
            currentDiv.className = "row mb-3";

            let questionNumberDiv = document.createElement("div");
            questionNumberDiv.className = "col-1";
            let questionNumber = document.createElement("input");
            questionNumber.type = "text";
            questionNumber.value = i;
            questionNumber.name = "test_number" + i;
            questionNumber.className = "form-control-plaintext";
            questionNumber.disabled = true;
            questionNumberDiv.appendChild(questionNumber);

            let markDiv = document.createElement("div");
            markDiv.className = "col-11";
            let mark = document.createElement("input");
            mark.type = "text";
            mark.name = "test_score" + i;
            mark.id = "test_score" + i;
            mark.placeholder = "Тестовый балл";
            mark.required = true;
            mark.className = "form-control";
            markDiv.appendChild(mark);


            currentDiv.appendChild(questionNumberDiv);
            currentDiv.appendChild(markDiv);

            firstTestDiv.appendChild(currentDiv);
        }
    }
}

function calcMaxScore() {
    let max_score = 0
    for (let i = 1; i < questionInfoCount + 1; i++) {
        max_score += parseInt(document.getElementById("max_mark" + i).value)
    }
    return max_score
}

function isAllQuestionInfoFilled() {
    for (let i = 1; i < questionInfoCount + 1; i++) {
        if (document.getElementById("max_mark" + i).value === '') {
            return false;
        }
    }
    return true;
}