/*
author = "Adrian Meyer @Animationsinstitut Filmakademie Baden-Württemberg"
copyright = "2019 All rights reserved. See LICENSE for more details."
status = "Prototype"
*/



// Playback Hotkeys (i/o/p)

var video = document.getElementById("video_player");
  	document.onkeydown = function(event) {
      	switch (event.keyCode) {
        	//time skipping "i/o"
        	case 74:
	            event.preventDefault();
	              
	            vid_currentTime = video.currentTime;
	            video.currentTime = vid_currentTime - 0.33;
	            break;
         
         	case 76:
	            event.preventDefault();
	              
	            vid_currentTime = video.currentTime;
	            video.currentTime = vid_currentTime + 0.33;
	            break;

            
            //play/stop "p"
            case 75:
            	event.preventDefault();

            	if (video.paused) {
            		video.play();
            	} else {
            		video.pause();
            	}   
	}
};




/*
// HTML5 Custom Player disbaled

window.onload = function() {

	var video = document.getElementById("video_player");
	var playButton = document.getElementById("play_pause");
	var seekBar = document.getElementById("seek_bar");


	// Event listener for the play/pause button
	playButton.addEventListener("click", function() {
		if (video.paused == true) {
			// Play the video
			video.play();

			// Update the button text to 'Pause'
			playButton.innerHTML = "Play/Pause";
		} else {
			// Pause the video
			video.pause();

			// Update the button text to 'Play'
			playButton.innerHTML = "Play/Pause";
		}
	});


	
	// Event listener for the seek bar
	seekBar.addEventListener("change", function() {
		// Calculate the new time
		var time = video.duration * (seekBar.value / 100);

		// Update the video time
		video.currentTime = time;
	});

	
	// Update the seek bar as the video plays
	video.addEventListener("timeupdate", function() {
		// Calculate the slider value
		var value = (100 / video.duration) * video.currentTime;

		// Update the slider value
		seekBar.value = value;
	});

	// Pause the video when the seek handle is being dragged
	seekBar.addEventListener("mousedown", function() {
		video.pause();
	});

}

*/