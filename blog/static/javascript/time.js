document.onload =  (function () {
	var clockElement = document.getElementById("clock");
	
	function AddZero(num) {
    	return (num >= 0 && num < 10) ? "0" + num : num + "";
	}
	
	function updateClock (clock) {
		if(clock) {
			var now = new Date();
			clock.innerHTML = AddZero(now.getDate()) + '/' 
							+ AddZero(now.getMonth() + 1) + '/' 
							+ now.getFullYear() + ' ' 
							+ AddZero(now.getHours()) + ':'
							+ AddZero(now.getMinutes()) +  ':'
							+ AddZero(now.getSeconds());
		}
	}

	setInterval(function () {
	 	updateClock( clockElement );
 	}, 1000);
}());