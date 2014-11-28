var PushPlayer = (function () {

	var player = null;

	function new_player() {
		console.log("onYouTubeIframeAPIReady");
		player = new YT.Player('yt-player', {
    		height: '390',
			width: '640',
			videoId: 'DX_eeOZVS2o',
			events: {
				'onReady': onPlayerReady
			}
 	 	});
	}

	function onPlayerReady(event) {
		console.log("onPlayerReady");
	}
	
	
	return {
		new_player: new_player
	}
	
})();



window.onYouTubeIframeAPIReady = PushPlayer.new_player;



