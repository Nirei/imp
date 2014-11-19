var loginModule = ( function () {
    
    var ajax = ajaxModule;

    var modelUrl = "/cgi-bin/model.py";
    var appUrl = "/ipmdb.html";
        
	var dom = {
	    loginButton 	: document.querySelector("#loginButton"),
  	    userField    	: document.querySelector("#username"),
   	    passField    	: document.querySelector("#password"),
   	    errorDisplay    : document.querySelector("#error-display"),
   	    errorMessage    : document.querySelector("#error-message")
	};
    
    function init() {
        checkSession();
        bindUIActions();
    }
    
    function bindUIActions() {
        dom.loginButton.onclick = doLogin;
    }
    
    function goToApp() {
        window.location = appUrl;
    }
    
    function displayError(msg) {
        dom.errorMessage.innerHTML = msg;
        dom.errorDisplay.style.visibility = "visible";
    }

    //////////////////    
    // CASOS DE USO //
    //////////////////
    
    function doLogin() {
        var user = dom.userField.value;
        var pass = dom.passField.value;
        ajax.post(modelUrl + "?action=login", "user=" + user + "&pass=" + pass, sessionCallback);
        // En principio login y session comparten el callback porque hace lo mismo, ya veremos
    }
    
    function checkSession() {
        ajax.get(modelUrl + "?action=session", sessionCallback);
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
        
        if( objectJSON.hasOwnProperty('result') && objectJSON['result'] == 'success' ) {
            goToApp();
        }
    }
    
    return {
        init: init
    };

})();

loginModule.init();

