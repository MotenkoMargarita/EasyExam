let timeSeconds = 0;

function timeCounterStart() {
    setInterval(timeSpent, 1000);
    clock();
}

function timeSpent() {
    let timeSpent = document.getElementById('timeSpent');
    timeSpent.value = timeSeconds;

    timeSeconds++;
}

function checkInputFile(input) {

    let requiredExtensions = ['txt', 'pdf', 'docx', 'jpeg', 'jpg', 'gif', 'tiff', 'png', 'bmp', 'svg', 'WebP']

    let file = input.files[0];

    let extension = file.name.split('.').pop();

    if (requiredExtensions.includes(extension)) {
    } else {
        alert("Данный формат файла не поддерживаеться для ответа. Выбирите другой файл. Используйте файл с расширением:" + requiredExtensions);
        input.value = "";
    }

}