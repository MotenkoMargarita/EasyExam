let counter = 0;

function addImage(solutionImages) {
    let input = document.getElementById('inputForImage');
    let alertForImages = document.getElementById('alertForImages');

    let photo = input.files[0];

    if (photo !== undefined) {
        let formData = new FormData();

        formData.append("photo", photo);
        fetch('/upload/image', {method: "POST", body: formData})
            .then(response => response.text())
            .then(function (data) {
                if (data !== 'Проблемы при загрузке файла' && data !== 'Выбирите другой формат файла') {

                    counter++;
                    let maxImgCounter = document.getElementById('maxImageCount')
                    maxImgCounter.value = counter;

                    let img = document.createElement('img');
                    img.src = "/" + data;
                    img.className = "rounded mx-auto d-block mb-3";
                    img.id = "solutionImage" + String(counter);
                    img.style.maxWidth = "100%";
                    img.style.maxHeight = "300px";
                    img.style.minHeight = "200px";
                    let images = document.getElementById(solutionImages);
                    images.appendChild(img);

                    let hiddenInput = document.createElement("input");
                    hiddenInput.setAttribute("name", "solutionImageInput" + String(counter));
                    hiddenInput.id = "solutionImageInput" + String(counter);
                    hiddenInput.type = "hidden";
                    hiddenInput.value = data.slice(21);
                    images.appendChild(hiddenInput);

                    images.appendChild(addDeleteButton(counter));

                    input.value = "";
                } else {
                    alertForImages.style.display = 'block';
                    alertForImages.innerText = data;
                }
            });
    }
}

function addDeleteButton(count) {
    let div = document.createElement("div");
    div.className = "d-grid mb-3 gap-2";
    div.id = "deleteButtonDiv" + count;

    let button = document.createElement("button");
    button.className = "btn btn-outline-danger";
    button.textContent = "Удалить";
    button.type = "button";
    button.onclick = function () {
        deleteImage(count);
    }

    div.appendChild(button);

    return div;
}

function deleteImage(imageNumber) {
    let deleteButtonDiv = document.getElementById("deleteButtonDiv" + imageNumber);
    deleteButtonDiv.remove();

    let hiddenInput = document.getElementById("solutionImageInput" + imageNumber);
    hiddenInput.remove();

    let img = document.getElementById("solutionImage" + imageNumber);
    img.remove();
}