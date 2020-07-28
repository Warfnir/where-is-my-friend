
function openLoginWindow(){
    let login_popup = document.getElementById('loginPopup')
    if(login_popup.style.display === "none"){
        login_popup.style.display = "block"
    }
    else{
        login_popup.style.display = "none"
    }

}