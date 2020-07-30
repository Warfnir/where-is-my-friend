// INITIALIZATION
window.onload = function () {
    gapi.load('auth2', function () {
        gapi.load('auth2', function () {
            auth2 = gapi.auth2.init({
                client_id: '931998872424-krno4hbjj52c73v9d4t2k35qma4rhh3b.apps.googleusercontent.com',
                // Scopes to request in addition to 'profile' and 'email'
                //scope: 'additional_scope'
            })
        })
    })
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function openLoginWindow() {
    let login_popup = document.getElementById('loginPopup')
    if (login_popup.style.display === "none") {
        login_popup.style.display = "block"
    }
    else {
        login_popup.style.display = "none"
    }

}

function onSignIn(googleUser) {
    var id_token = googleUser.getAuthResponse().id_token;
    var csrf_token = getCookie('csrftoken')

    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://localhost:8000/google_login/');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.setRequestHeader('X-CSRFToken', csrf_token)
    xhr.onload = function () {
        console.log(xhr.responseText, xhr.status);
        // window.location.reload()
    };
    xhr.send('idtoken=' + id_token);
}


var googleUser = {}
var startApp = function () {
    gapi.load('auth2', function () {
        // Retrieve the singleton for the GoogleAuth library and set up the client.
        auth2 = gapi.auth2.init({
            client_id: '931998872424-krno4hbjj52c73v9d4t2k35qma4rhh3b.apps.googleusercontent.com',
            cookiepolicy: 'single_host_origin',
            // Request scopes in addition to 'profile' and 'email'
            //scope: 'additional_scope'
        });
        attachSignin(document.getElementById('customBtn'))
    });
};

function attachSignin(element) {
    console.log(element.id)
    auth2.attachClickHandler(element, {},
        function (googleUser) {
            onSignIn(googleUser)
        }, function (error) {
            alert(JSON.stringify(error, undefined, 2))
        })
}

function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
        console.log('User signed out.')
    })
}


window.onload = startApp()