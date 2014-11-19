var appModule = ( function () {
    
    var ajax = ajaxModule;
    
    var modelUrl = "/cgi-bin/model.py";
    
    function deleteCookie() {
        document.cookie = "ipm-db=;expires=Thu, 01 Jan 1970 00:00:01 GMT";
    }

    //////////////////    
    // CASOS DE USO //
    //////////////////
    
    function doLogin(user, pass, callback) {
        ajax.post(modelUrl + "?action=login", "username=" + user + "&passwd=" + pass, callback);
        // En principio login y session comparten el callback porque hace lo mismo, ya veremos
    }
    
    function checkSession(callback) {
        ajax.get(modelUrl + "?action=session", callback);
    }

    function doLogout(callback) {
        ajax.get(modelUrl + "?action=logout", callback);
    }

    return {
        doLogin: doLogin,
        checkSession: checkSession,
        doLogout: doLogout,
        deleteCookie: deleteCookie
    };

})();
