var PushPlayer = (function () {

	var player = null;

	function new_player() {
		console.log("onYouTubeIframeAPIReady");
		player = new YT.Player('yt-player', {
    		height: '640',
			width: '390',
			videoId: 'YD9SEtaVKgA',
			events: {
				'onReady': onPlayerReady
			}
 	 	});
	}

	function onPlayerReady(event) {
		console.log("onPlayerReady");
	}
	
    function play() {
        player.playVideo();
    }
    
    function pause() {
        player.pauseVideo();
    }
    
    function load(id) {
        player.cueVideoById(id);
	player.playVideo()
    }

	return {
		new_player  : new_player,
        play        : play,
        pause       : pause,
        load        : load,
	}

})();

window.onYouTubeIframeAPIReady = PushPlayer.new_player;
