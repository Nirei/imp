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
   	    movieTitle      : document.querySelector("#movie-title"),
   	    movieYear       : document.querySelector("#movie-year"),
   	    movieGenre      : document.querySelector("#movie-genre"),
   	    movieSynopsis   : document.querySelector("#movie-synopsis"),
   	    movieUser       : document.querySelector("#movie-user"),
	};
    
    function init() {
        app.checkSession(sessionCallback);
        bindUIActions();
    }
    
    function bindUIActions() {
        dom.logoutButton.onclick = logout;
        dom.prevPage.onclick = prevPage;
        dom.nextPage.onclick = nextPage;
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
        dom.movieTitle.innerHTML      = data.title
        dom.movieYear.innerHTML       = data.year
        dom.movieGenre.innerHTML      = data.category
        dom.movieSynopsis.innerHTML   = data.synopsis
        dom.movieUser.innerHTML       = data.username
    }
    
    function logout() {
        app.doLogout(logoutCallback);
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
            displayMovie(json['data']);
        } 
    }
    
    return {
        init: init
    };

})();

ipmdbModule.init();

