var ipmdbModule = ( function () {
    
    var app = appModule;
    var page = 1;
    var commentPage = 0;

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
   	    movieCover      : document.querySelector("#movie-cover-img"),
   	    favStatus       : document.querySelector("#fav-status"),
   	    coverPlaceholder: document.querySelector("#movie-cover-ph"),
   	    commentSection  : document.querySelector("#comment-section"),
   	    moreComments    : document.querySelector("#more-comments"),
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
        dom.movieCover.onload = displayCover;
        dom.moreComments.onclick = moreCommentsClicked;
    }
    
    function enableMoreCommentsButton(enable) {
        if(enable) {
            dom.moreComments.style.display = "inline-block";
        } else {
            dom.moreComments.style.display = "none";
        }
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
    
    function createCommentHtml(user, email, text, date) {
        var commentDiv = document.createElement("div");
        var userDiv = document.createElement("div");
        var textDiv = document.createElement("div");
        var dateDiv = document.createElement("div");
        commentDiv.className = "comment";
        userDiv.className = "user";
        textDiv.className = "text";
        dateDiv.className = "date";
        userDiv.innerHTML = user;
        textDiv.innerHTML = text;
        dateDiv.innerHTML = date;
        commentDiv.appendChild(userDiv);
        commentDiv.appendChild(textDiv);
        commentDiv.appendChild(dateDiv);
        
        return commentDiv;
    }
    
    function displayComments(comments) {
        for(var i in comments) {
            var user = comments[i].username;
            var mail = comments[i].email;
            var text = comments[i].content;
            var date = comments[i].comment_date;
            
            dom.commentSection.appendChild(createCommentHtml(user, mail, text, date));
        }
    }
    
    function loadCommentsPage(id) {
        commentPage += 1;
        app.getComments(id, commentPage, commentsCallback);
    }
    
    function clearComments() {
        commentPage = 0;
        dom.commentSection.innerHTML = '';
    }
    
    function displayMovie(data) {
        dom.movieId.innerHTML         = data.id
        dom.movieTitle.innerHTML      = data.title
        dom.movieYear.innerHTML       = data.year
        dom.movieGenre.innerHTML      = data.category
        dom.movieSynopsis.innerHTML   = data.synopsis
        dom.movieUser.innerHTML       = data.username
        dom.movieCover.src            = data.url_image
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
        var id = this.id.substr(this.id.indexOf('-')+1);
        loadMovie(id);
    }
    
    function moreCommentsClicked() {
        enableMoreCommentsButton(false);
        loadCommentsPage(dom.movieId.innerHTML);
    }
    
    function loadMovie(id) {
        enableMoreCommentsButton(false);
        clearComments();
        dom.movieCover.style.display = "none";
        dom.coverPlaceholder.style.display = "inline";
        app.getMovie(id, movieCallback);
        app.getFav(id, getFavCallback);
        loadCommentsPage(id);
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
    
    function displayCover() {
        dom.movieCover.style.display = "inline";
        dom.coverPlaceholder.style.display = "none";
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
            loadMovie(json['data'][0].id);
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
    
    function getFavCallback(response) {
        var json = JSON.parse(response);
        
        if( json.hasOwnProperty('error') ) {
            displayError(json['error']);
        } else if( json['result'] == 'success' ) {
            setFavIconStatus(json['data']);
        }
    }
    
    function setFavCallback(response) {
        var json = JSON.parse(response);
        
        if( json.hasOwnProperty('error') ) {
            displayError(json['error']);
        } else if( json['result'] == 'success' ) {
            app.getFav(dom.movieId.innerHTML, getFavCallback);
        }
    }
    
    function commentsCallback(response) {
        var json = JSON.parse(response);
        
        if( json.hasOwnProperty('error') ) {
            displayError(json['error']);
        } else if( json['result'] == 'success' ) {
            displayComments(json['data']);
            enableMoreCommentsButton(true);
        } else {
            enableMoreCommentsButton(false);
        }
    }
    
    return {
        init: init
    };

})();

ipmdbModule.init();

