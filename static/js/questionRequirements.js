let criteriaCount = 0;

function addNewCriteria() {
    criteriaCount++;
    let criteria = document.getElementById('criteria');
    let criteriaCountElement = document.getElementById('criteriaCount');
    criteriaCountElement.value = criteriaCount;

    let newCriteria = document.createElement('div');
    newCriteria.className = "card mb-3"
    newCriteria.id = "criteria" + criteriaCount;
    newCriteria.innerHTML = "" +
        "<div class=\"card-header\" id=\"head" + criteriaCount + "\">" +
        "<label class=\"form-label\">" + criteriaCount + " критерий</label>\n" +
        "</div>" +
        "<div class=\"card-body\" id=\"node" + criteriaCount + "\">\n" +
        "                            <label class=\"form-label\">Текст</label>\n" +
        "                            <textarea onkeyup=\"showResult(this.value, 'textTextAreaResult" + criteriaCount + "')\" class=\"form-control mb-3\" id=\"text" + criteriaCount + "\" aria-describedby=\"text" + criteriaCount + "\" name=\"text" + criteriaCount + "\" required></textarea>\n" +
        "<div >" +
        "<label class=\"form-label\">\n" +
        "                <a data-bs-toggle=\"collapse\" href=\"#collapseResult" + criteriaCount + "\" role=\"button\"\n" +
        "                   aria-expanded=\"false\" aria-controls=\"collapseResult" + criteriaCount + "\">\n" +
        "                    Результат\n" +
        "                </a>\n" +
        "            </label>\n" +
        "\n" +
        "            <div class=\"collapse mb-3\" id=\"collapseResult" + criteriaCount + "\">\n" +
        "                <div class=\"card card-body\">\n" +
        "                    <div id=\"textTextAreaResult" + criteriaCount + "\"></div>\n" +
        "                </div>\n" +
        "            </div>" +
        "</div>" +
        "                            <label class=\"form-label\">Балл</label>\n" +
        "                            <input type=\"text\" class=\"form-control mb-3\" id=\"value" + criteriaCount + "\" aria-describedby=\"value" + criteriaCount + "\" name=\"value" + criteriaCount + "\" required>\n" +
        "                            <div class=\"d-grid gap-3\">\n" +
        "                                <button type=\"button\" class=\"btn btn-outline-warning\" onclick=\"deleteCriteria(" + criteriaCount + ")\"><i class=\"bi bi-dash\"></i></button>\n" +
        "                            </div>\n" +
        "                        </div>";

    let newButton = document.createElement('div');
    newButton.innerHTML = "<div class=\"card mb-3\" id=\"addButtons\">\n" +
        "                <div class=\"card-body\">\n" +
        "                    <div class=\"d-grid gap-3\">\n" +
        "                        <button type=\"button\" class=\"btn btn-outline-success\" onclick=\"addNewCriteria()\"><i class=\"bi bi-plus\"></i></button>\n" +
        "                    </div>\n" +
        "                </div>\n" +
        "            </div>"

    let buttons = document.getElementById('addButtons');
    buttons.remove();

    criteria.appendChild(newCriteria);
    criteria.appendChild(newButton);

}

function deleteCriteria(index) {
    criteriaCount--;
    let criteriaToRemove = document.getElementById("criteria" + index);
    criteriaToRemove.remove();

    let criteriaCountElement = document.getElementById('criteriaCount');
    criteriaCountElement.value = criteriaCount;

    let criteria = document.getElementById('criteria');

    console.log(criteria.childNodes)

    let newCounter = 1;

    for (let child of criteria.childNodes) {
        console.log(child)
        try {
            let currNumber = child.id.replace("criteria", "");
            let currElement = document.getElementById(child.id);

            let criteriaFirstNode = document.getElementById(currElement.firstChild.id);
            criteriaFirstNode.innerText = newCounter + " критерий";

            let criteriaLastNode = document.getElementById(currElement.lastChild.id);
            for (let childOfCriteriaLastNode of criteriaLastNode.childNodes) {

                if (childOfCriteriaLastNode.id === "text" + currNumber) {
                    let textInput = document.getElementById("text" + currNumber)
                    textInput.setAttribute("name", "text" + newCounter);
                    textInput.setAttribute("aria-describedby", "text" + newCounter);
                    textInput.id = "text" + newCounter;
                }
                if (childOfCriteriaLastNode.id === "value" + currNumber) {
                    let valueInput = document.getElementById("value" + currNumber)
                    valueInput.setAttribute("name", "value" + newCounter);
                    valueInput.setAttribute("aria-describedby", "value" + newCounter);
                    valueInput.id = "value" + newCounter;
                    newCounter++;
                }
            }
        } catch (e) {
        }
    }
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

function addQuestionNumbers(baseUrl, currId) {
    let subject = document.getElementById('subject_select' + currId)
    fetch(baseUrl + '/subject/' + subject.value)
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            let select = document.getElementById("number"  + currId);
            select.innerHTML = "";
            for (let i = 1; i <= data; i++) {
                let option = document.createElement("option");
                option.text = i;
                option.value = i;
                select.add(option);
            }
        });
}

function showResult(value, resultBlockId) {
    let resultBloc = document.getElementById(resultBlockId);

    resultBloc.innerText = value;
    MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
}

function LoadNumbersAndSelectNumberOfCurrentRequirement(baseUrl, currentRequirementId, currentNumber) {
    let subject = document.getElementById("subject_select" + currentRequirementId);

    fetch(baseUrl + '/subject/' + subject.value)
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            let select = document.getElementById("number" + currentRequirementId);
            select.innerHTML = "";
            for (let i = 1; i <= data; i++) {
                let option = document.createElement("option");
                if (i === parseInt(currentNumber)) {
                    option.selected = true;
                }
                option.text = i;
                option.value = i;
                select.add(option);
            }
        });
}

function changeVisualValue(value, blockToChangeId) {
    console.log(value)
    let blockToChange = document.getElementById(blockToChangeId);
    blockToChange.innerText = value;
}