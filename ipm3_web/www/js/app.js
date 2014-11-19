var appModule = ( function () {
    
    var ajax = ajaxModule;
    
    var modelUrl = "/cgi-bin/model.py";

    //////////////////    
    // CASOS DE USO //
    //////////////////
    
    function doLogin(callback) {
        var user = dom.userField.value;
        var pass = dom.passField.value;
        ajax.post(modelUrl + "?action=login", "username=" + user + "&passwd=" + pass, callback);
        // En principio login y session comparten el callback porque hace lo mismo, ya veremos
    }
    
    function checkSession(callback) {
        ajax.get(modelUrl + "?action=session", callback);
    }

    return {
        doLogin: doLogin,
        checkSession: checkSession
    };

})();
