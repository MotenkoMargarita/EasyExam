function getCities(baseUrl) {
    let region = document.getElementById('region_select')

    fetch(baseUrl + '/cities/' + region.value)
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            let select = document.getElementById("city_select");
            select.innerHTML = "";

            let option = document.createElement("option");
            option.text = "Выберите населенный пункт";
            option.value = "-1";
            option.selected = true;
            select.add(option);

            for (let k in data) {
                let option = document.createElement("option");
                option.text = k;
                option.value = data[k];
                select.add(option);
            }
        });

}

