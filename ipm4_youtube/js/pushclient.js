var PushClient = (function() {

    var app = PushPlayer;
	var ws_server_uri = "ws://localhost:8888/ws";
	
	var dom = {
		logging: document.querySelector("#log")
	};
	
	function init() {
		bindWSActions();
	}
	
	function bindWSActions() {
		var ws = new WebSocket(ws_server_uri);
    
        ws.onopen = function(e) {
        	append_log("Websocket opened");
        }
    
        ws.onclose = function(e) {
        	append_log("Websocket closed");
        }
    
        ws.onmessage = function(e) {
            handle_message(e);
		}
	}

    function handle_message(msg) {
        args = msg.data.split('=');
        action = args[0];
        if(action == "play") {
            app.play();
        } else if(action == "pause") {
            app.pause();
        } else if(action == "video") {
            app.load(args[1]);
        } else
    }
    
    return {
    	init: init
    };
      
})();

PushClient.init();
