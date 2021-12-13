function copyIdentifier() {
    let identifier = document.getElementById('ident');
    identifier.select();
    document.execCommand("copy");
}