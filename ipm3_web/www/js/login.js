var loginModule = ( function () {

    var self = this;
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
        app.checkSession(sessionCallback);
        bindUIActions();
    }
    
    function bindUIActions() {
        dom.loginButton.onclick = login;
    }
    
    function goToApp() {
        window.location = appUrl;
    }
    
    function displayError(msg) {
        dom.errorMessage.innerHTML = msg;
        dom.errorDisplay.style.visibility = "visible";
    }
    
    ///////////////////
    // FUNCTIONALITY //
    ///////////////////
    
    function login() {
        var user = dom.userField.value;
        var pass = dom.passField.value;
        app.doLogin(user, pass, sessionCallback);
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
        if( objectJSON.hasOwnProperty('result') && objectJSON['result'] == 'success' ) {
            console.log("Logged in");
            // goToApp();
        }
    }
    
    return {
        init: init
    };

})();

loginModule.init();

