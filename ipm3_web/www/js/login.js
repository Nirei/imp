var loginModule = ( function () {
    
    var ajax = ajaxModule;
    
    var serverUrl = "http://localhost:8080/"
    var modelUrl = serverUrl + "cgi-bin/model.py";
    var appUrl = serverUrl + "ipmdb.html";
        
	var dom = {
	    loginButton 	: document.querySelector("#loginButton"),
	};
    
    function init() {
        bindUIActions();
    }
    
    function bindUIActions() {
        dom.loginButton.onclick = doLogin;
    }
    
    function doLogin() {
        console.log("Doing login");
        goToApp();
    }
    
    function checkSession() {
        ajax.get(modelUrl + "?action=session", sessionCallback);
    }
    
    function sessionCallback(response) {
        var objectJSON = JSON.parse(responseText);
        if( objectJSON['result'] ) {
            goToApp();
        }
    }
    
    function goToApp() {
        window.location = appUrl;
    }
    
    return {
        init: init
    };

})();

loginModule.init();
