function changeAnswerType(value) {
    if (value === 'В' || value === 'B') {

    } else if (value === 'С' || value === 'C') {

    }
}

function showResult(value, resultBlockId) {
    let resultBloc = document.getElementById(resultBlockId);

    resultBloc.innerText = value;
    MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
}


function addQuestionNumbersForCreateForm(baseUrl) {
    let subject = document.getElementById('subject_select')
    fetch(baseUrl + '/subject/' + subject.value)
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            let select = document.getElementById("number");
            select.innerHTML = "";
            for (let i = 1; i <= data; i++) {
                let option = document.createElement("option");
                option.text = i;
                option.value = i;
                select.add(option);
            }
        });
}
