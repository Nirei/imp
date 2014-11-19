var loginModule = ( function () {

    var app = appModule;
    
    var appUrl = "/ipmdb.html";
        
	var dom = {
	    loginButton 	: document.querySelector("#loginButton"),
  	    userField    	: document.querySelector("#username"),
   	    passField    	: document.querySelector("#password"),
   	    errorDisplay    : document.querySelector("#error-display"),
   	    errorMessage    : document.querySelector("#error-message")
	};
    
    function init() {
        app.checkSession(callback);
        bindUIActions();
    }
    
    function bindUIActions() {
        dom.loginButton.onclick = app.doLogin(callback);
    }
    
    function goToApp() {
        window.location = appUrl;
    }
    
    function displayError(msg) {
        dom.errorMessage.innerHTML = msg;
        dom.errorDisplay.style.visibility = "visible";
    }
    
    ///////////////
    // CALLBACKS //
    ///////////////
    
    function callback(response) {
        var objectJSON = JSON.parse(response);
        if( objectJSON.hasOwnProperty('error') ) {
            console.log(objectJSON['error']);
            displayError(objectJSON['error']);
        }
        
        console.log(objectJSON);
        if( objectJSON.hasOwnProperty('result') && objectJSON['result'] == 'success' ) {
            console.log("Logged in");
            goToApp();
        }
    }
    
    return {
        init: init
    };

})();

loginModule.init();

