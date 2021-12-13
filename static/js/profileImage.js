function changeImage() {
    let input = document.getElementById('inputForImage');
    let hiddenInput = document.getElementById('imgSrc');
    let img = document.getElementById('profileImage');
    let alertForImages = document.getElementById('alertForImages');

    let photo = input.files[0];

    if (photo !== undefined) {
        let formData = new FormData();

        formData.append("photo", photo);
        fetch('/upload/image', {method: "POST", body: formData})
            .then(response => response.text())
            .then(function (data) {
                if (data !== 'Проблемы при загрузке файла' && data !== 'Выбирите другой формат файла') {
                    img.src = data;
                    hiddenInput.value = data.slice(21);
                } else {
                    alertForImages.style.display = 'block';
                    alertForImages.innerText = data;
                }
            });
    }
}