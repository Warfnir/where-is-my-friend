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
        console.log('Signed in as: ' + xhr.responseText);
    };
    xhr.send('idtoken=' + id_token);
}


function loginWithGoogle(googleUser) {
    auth2.grantOfflineAccess().then(loginWithGoogleCallback)
}


function loginWithGoogleCallback(authResult) {
    if (authResult['code']) {
        csrf_token = jQuery("[name=csrfmiddlewaretoken]").val()
        // Send the code to the server
        $.ajax({
            type: 'POST',
            url: 'http://localhost:8000/google_login/',
            // Always include an `X-Requested-With` header in every AJAX request,
            // to protect against CSRF attacks.
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrf_token,
            },
            ContentType: 'application/octet-stream; charset=utf-8',
            success: function (result) {
                // Handle or verify the server response.
            },
            processData: false,
            data: authResult['code']
        });
    } else {
        // There was an error.
    }
}


function logout() {

}
