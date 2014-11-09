var loginModule = ( function () {
    
    var ajax = ajaxModule;
    
    var serverUrl = "http://localhost:8080/"
    var modelUrl = serverUrl + "cgi-bin/model.py";
    var appUrl = serverUrl + "ipmdb.html";
        
	var dom = {
	    loginButton 	: document.querySelector("#loginButton"),
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
    
    // CASOS DE USO
    
    function doLogin() {
        var user = "test1";
        var pass = "test1";
        ajax.post(modelUrl + "?action=login", "user=" + user + "&pass=" + pass, sessionCallback);
        // En principio login y session comparten el callback porque hace lo mismo, ya veremos
    }
    
    function checkSession() {
        ajax.get(modelUrl + "?action=session", sessionCallback);
    }
    
    // CALLBACKS
    
    function sessionCallback(response) {
        var objectJSON = JSON.parse(responseText);
        if( objectJSON['result'] ) {
            goToApp();
        }
    }
    
    return {
        init: init
    };

})();

loginModule.init();
