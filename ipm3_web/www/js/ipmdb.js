var ipmdbModule = ( function () {
    
    var app = appModule;
    var page = 1;

    var loginUrl = "/login.html";
        
	var dom = {
	    logoutButton 	: document.querySelector("#logout-button"),
	    movieList       : document.querySelector("#movie-list"),
  	    prevPage        : document.querySelector("#btn-backward"),
   	    nextPage        : document.querySelector("#btn-forward"),
   	    pageIndex       : document.querySelector("#page-index"),
   	    movieId         : document.querySelector("#movie-id"),
   	    movieTitle      : document.querySelector("#movie-title"),
   	    movieYear       : document.querySelector("#movie-year"),
   	    movieGenre      : document.querySelector("#movie-genre"),
   	    movieSynopsis   : document.querySelector("#movie-synopsis"),
   	    movieUser       : document.querySelector("#movie-user"),
   	    favStatus       : document.querySelector("#fav-status"),
	};
    
    function init() {
        app.checkSession(sessionCallback);
        bindUIActions();
    }
    
    function bindUIActions() {
        dom.logoutButton.onclick = logout;
        dom.prevPage.onclick = prevPage;
        dom.nextPage.onclick = nextPage;
        dom.favStatus.onclick = changeFavStatus;
    }
    
    function goToLogin() {
        window.location = loginUrl;
    }
    
    function displayError(msg) {
        dom.errorMessage.innerHTML = msg;
        dom.errorDisplay.style.visibility = "visible";
    }
    
    function displayPage(data) {
        dom.movieList.innerHTML = '';
        for(var i in data) {
            var li = document.createElement("li");
            var a = document.createElement("a");
            a.href = '#'
            a.id = 'movie-' + data[i].id;
            a.innerHTML = data[i].title;
            a.onclick = movieClicked
            li.appendChild(a);
            dom.movieList.appendChild(li);
            
        }
    }
    
    function displayMovie(data) {
        dom.movieId.innerHTML         = data.id
        dom.movieTitle.innerHTML      = data.title
        dom.movieYear.innerHTML       = data.year
        dom.movieGenre.innerHTML      = data.category
        dom.movieSynopsis.innerHTML   = data.synopsis
        dom.movieUser.innerHTML       = data.username
    }
    
    function logout() {
        app.doLogout(logoutCallback);
    }
    
    function getFav(id) {
        app.getFav(id, getFavCallback);
    }
    
    function loadPage() {
        dom.pageIndex.innerHTML = page;
        app.getPage(page, pageCallback);
    }
    
    function prevPage() {
        if(page != 1) {
            page -= 1;
            loadPage();
        }
    }
    
    function nextPage() {
        page += 1;
        loadPage();
    }
    
    function movieClicked() {
        app.getMovie(this.id.substr(this.id.indexOf('-')+1), movieCallback);
    }
    
    function setFavIconStatus(status) {
        if(status == "true") {
            dom.favStatus.className = "fav-icon-true";
        } else {
            dom.favStatus.className = "fav-icon-false";
        }
    }
    
    function changeFavStatus() {
        if(dom.favStatus.className == "fav-icon-true") {
            app.setFav(dom.movieId.innerHTML, false, setFavCallback);
        } else {
            app.setFav(dom.movieId.innerHTML, true, setFavCallback);
        }
    }
    
    ///////////////
    // CALLBACKS //
    ///////////////
    
    function sessionCallback(response) {
        var json = JSON.parse(response);
        if( json.hasOwnProperty('error') ) {
            displayError(json['error']);
        }
        
        if( json.hasOwnProperty('result') && json['result'] == 'failure' ) {
            goToLogin();
        } else {
            loadPage();
        }
    }
    
    function logoutCallback(response) {
        goToLogin();
    }
    
    function pageCallback(response) {
        var json = JSON.parse(response);
        if( json['result'] == 'success' ) {
            app.getMovie(json['data'][0].id, movieCallback);
            displayPage(json['data']);
        } else {
            // Chapuza
            prevPage();
        }
        
    }
    
    function movieCallback(response) {
        var json = JSON.parse(response);
        
        if( json.hasOwnProperty('error') ) {
            displayError(json['error']);
        } else if( json['result'] == 'success' ) {
            getFav(json['data'].id);
            displayMovie(json['data']);
        }
    }
    
    function getFavCallback(response) {
        var json = JSON.parse(response);
        
        console.log(json);
        if( json.hasOwnProperty('error') ) {
            displayError(json['error']);
        } else if( json['result'] == 'success' ) {
            setFavIconStatus(json['data']);
        }
    }
    
    function setFavCallback(response) {
        var json = JSON.parse(response);
        
        console.log(json);
        if( json.hasOwnProperty('error') ) {
            displayError(json['error']);
        } else if( json['result'] == 'success' ) {
            getFav(dom.movieId.innerHTML);
        }
    }
    
    return {
        init: init
    };

})();

ipmdbModule.init();

