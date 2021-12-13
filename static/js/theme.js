function readClick(materialId, baseLink, subject_id, theme_id) {
    let cb = document.getElementById("materialCB" + materialId);
    url = baseLink + "/subject/" + subject_id + "/theme/" + theme_id + "/material/" + materialId;
    let response = fetch(url);
}