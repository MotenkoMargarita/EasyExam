let loadedDataArray = [];
let minToMax = false;
let currSortFunction = GetSortOrderByIntValueFromMaxToMin;

function loadData(baseUrl) {

    let region = document.getElementById('region_select').value;
    let city = document.getElementById('city_select').value;

    // let tableBody = document.getElementById("ratingTableBody");
    // tableBody.innerHTML = "";
    fetch(baseUrl + '/get-rating?region=' + region + "&city=" + city)
        .then((response) => {
            return response.json();
        })
        .then((data) => {
                console.log(data)

                let result = [];
                for (let i in data) {
                    result.push(data[i]);
                }
                loadedDataArray = result;
                // result.sort(GetSortOrderByIntValueFromMaxToMin('score'))
                //
                // for (let item in result) {
                //     let tr = document.createElement("tr");
                //     let curr_user_data = result[item];
                //
                //     tr.appendChild(createTd(curr_user_data["first_name"]));
                //     tr.appendChild(createTd(curr_user_data["last_name"]));
                //     tr.appendChild(createTd(curr_user_data["region"]));
                //     tr.appendChild(createTd(curr_user_data["city"]));
                //     tr.appendChild(createTd(curr_user_data["score"]));
                //
                //     tableBody.appendChild(tr);
                // }
            }
        ).then(() => placeData());
}

function changeSortFunctionScore() {
    let scoreIcon = document.getElementById('scoreIcon');
    if (minToMax) {
        minToMax = !minToMax;
        currSortFunction = GetSortOrderByIntValueFromMaxToMin;
        scoreIcon.className = "bi bi-chevron-down"
    } else {
        minToMax = !minToMax;
        currSortFunction = GetSortOrderByIntValueFromMinToMax;
        scoreIcon.className = "bi bi-chevron-up"
    }
    placeData();
}

function placeData() {

    let tableBody = document.getElementById("ratingTableBody");
    tableBody.innerHTML = "";

    loadedDataArray.sort(currSortFunction())

    for (let item in loadedDataArray) {
        let tr = document.createElement("tr");
        let curr_user_data = loadedDataArray[item];

        tr.appendChild(createTd(curr_user_data["first_name"]));
        tr.appendChild(createTd(curr_user_data["last_name"]));
        tr.appendChild(createTd(curr_user_data["region"]));
        tr.appendChild(createTd(curr_user_data["city"]));
        tr.appendChild(createTd(curr_user_data["score"]));

        tableBody.appendChild(tr);
    }
}

function createTd(text) {
    let td = document.createElement("td");
    td.innerHTML = text;
    return td;
}

function GetSortOrderByIntValueFromMaxToMin() {
    return function (a, b) {
        let prop = 'score'
        if (parseInt(a[prop]) < parseInt(b[prop])) {
            return 1;
        } else if (parseInt(a[prop]) > parseInt(b[prop])) {
            return -1;
        }
        return 0;
    }
}

function GetSortOrderByIntValueFromMinToMax() {
    return function (a, b) {
        let prop = 'score'
        if (parseInt(a[prop]) > parseInt(b[prop])) {
            return 1;
        } else if (parseInt(a[prop]) < parseInt(b[prop])) {
            return -1;
        }
        return 0;
    }
}
