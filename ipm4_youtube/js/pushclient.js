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
        	console.log("Websocket opened");
        }
    
        ws.onclose = function(e) {
        	console.log("Websocket closed");
        }
    
        ws.onmessage = function(e) {
            handle_message(e);
		}
	}

    function handle_message(msg) {
        console.log("Received message: " + msg.data);

        args = msg.data.split('=');
        action = args[0];
        if(action == "play") {
            app.play();
        } else if(action == "pause" || action == "stop" ) {
            app.pause();
        } else if(action == "video") {
            app.load(args[1]);
        }
    }
    
    return {
    	init: init
    };
      
})();

PushClient.init();
