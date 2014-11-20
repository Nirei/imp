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
        app.doLogin(user, pass, loginCallback);
    }
    
    ///////////////
    // CALLBACKS //
    ///////////////
    
    function sessionCallback(response) {
        var json = JSON.parse(response);
        if( json.hasOwnProperty('error') ) {
            console.log(json['error']);
            displayError(json['error']);
        }
        
        if( json.hasOwnProperty('result') == json['result'] == 'success' ) {
            console.log("Logged in");
            goToApp();
        }
    }
    
    function loginCallback(response) {
        var json = JSON.parse(response);
        if( json.hasOwnProperty('error') ) {
            console.log(json['error']);
            displayError(json['error']);
        }
        
        if( json.hasOwnProperty('result') ) {
            if( json['result'] == 'success' ) {
                $('#login-form').submit();
                goToApp();
            } else if( json['result'] == 'failure' && json['reason'] == 'not found' ) {
                displayError('O usuario especificado non se atopa na base de datos');
            }
        }
    }
    
    return {
        init: init
    };

})();

loginModule.init();

