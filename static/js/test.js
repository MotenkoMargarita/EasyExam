let timeSeconds;

function start() {
    let time_input = document.getElementById("time");
    timeSeconds = parseInt(time_input.value) * 60;
    setInterval(clock, 1000);
    clock();
}

function clock() {
    let seconds = timeSeconds % 60
    let minutes = timeSeconds / 60 % 60
    let hour = timeSeconds / 60 / 60 % 60
    if (timeSeconds <= 0) {
        document.getElementById('test').submit();
    } else {
        let clockDiv = document.getElementById('clock');
        let timeLeft = document.getElementById('timeLeft');
        if (timeLeft !== null) {
            timeLeft.value = timeSeconds;
        }

        clockDiv.innerHTML = "Осталось времени: " +
            (Math.trunc(hour) >= 10 ? Math.trunc(hour) : '0' + Math.trunc(hour)) +
            ':' + (Math.trunc(minutes) >= 10 ? Math.trunc(minutes) : '0' + Math.trunc(minutes)) +
            ':' + (seconds >= 10 ? seconds : '0' + seconds);
    }
    --timeSeconds;
    // timeSeconds -= 60*5;
}

function checkInputFile(input) {

    let requiredExtensions = ['txt', 'pdf', 'docx', 'jpeg', 'jpg', 'gif', 'tiff', 'png', 'bmp', 'svg', 'WebP']

    let file = input.files[0];

    let extension = file.name.split('.').pop();

    if (requiredExtensions.includes(extension)) {
    } else {
        alert("Данный формат файла не поддерживаеться для ответа. Выберите другой файл. Используйте файл с расширением:" + requiredExtensions);
        input.value = "";
    }

}
