var ipmdbModule = ( function () {
    
    var app = appModule;

    var loginUrl = "/login.html";
        
	var dom = {
	    logoutButton 	: document.querySelector("#logout-button")
	};
    
    function init() {
        app.checkSession(sessionCallback);
        bindUIActions();
    }
    
    function bindUIActions() {
        dom.logoutButton.onclick = logout;
    }
    
    function goToLogin() {
        window.location = loginUrl;
    }
    
    function displayError(msg) {
        dom.errorMessage.innerHTML = msg;
        dom.errorDisplay.style.visibility = "visible";
    }
      
    ///////////////////
    // FUNCTIONALITY //
    ///////////////////
    
    function logout() {
        app.doLogout(logoutCallback);
    }
    
    ///////////////
    // CALLBACKS //
    ///////////////
    
    function sessionCallback(response) {
        var objectJSON = JSON.parse(response);
        if( objectJSON.hasOwnProperty('error') ) {
            console.log(objectJSON['error']);
            displayError(objectJSON['error']);
        }
        
        console.log(objectJSON);
        if( objectJSON.hasOwnProperty('result') && objectJSON['result'] == 'failure' ) {
            goToLogin();
        }
    }
    
    function logoutCallback(response) {
        var objectJSON = JSON.parse(response);
        console.log(objectJSON);
        app.deleteCookie();
        goToLogin();
    }
    
    return {
        init: init
    };

})();

ipmdbModule.init();

