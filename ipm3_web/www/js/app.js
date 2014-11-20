var appModule = ( function () {
    
    var ajax = ajaxModule;
    var modelUrl = "/cgi-bin/model.py";

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
    
    function getPage(page, callback) {
        ajax.get(modelUrl + "?action=movie_list&page=" + page, callback);
    }
    
    function getMovie(id, callback) {
        ajax.get(modelUrl + "?action=movie_data&movie_id=" + id, callback);
    }
    
    function getFav(id, callback) {
        ajax.get(modelUrl + "?action=get_fav&movie_id=" + id, callback);
    }
    
    function setFav(id, status, callback) {
        ajax.post(modelUrl + "?action=set_fav", "movie_id=" + id + "&mark=" + status, callback);
    }

    function getComments(id, page, callback) {
        ajax.get(modelUrl + "?action=get_comments&movie_id=" + id + "&page=" + page, callback);
    }
    
    function sendComment(id, comment, callback) {
        ajax.post(modelUrl + "?action=new_comment", "movie_id=" + id + "&comment=" + comment, callback);
    }
    
    function deleteComment(movie, comment, callback) {
        console.log(movie + " " + comment);
        ajax.post(modelUrl + "?action=del_comment", "movie_id=" + movie + "&comment_id=" + comment, callback);
    }

    return {
        doLogin: doLogin,
        checkSession: checkSession,
        doLogout: doLogout,
        getPage: getPage,
        getMovie: getMovie,
        getFav: getFav,
        setFav: setFav,
        getComments: getComments,
        sendComment: sendComment,
        deleteComment: deleteComment,
    };

})();
