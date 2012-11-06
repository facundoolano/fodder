
/**
 * Makes this clients subscribe to the given channel, and execute
 * the given handler with each json message than arrives.
 */
function sse_subscribe(channel, message_handler){
	if (!!window.EventSource) {
		var source = new EventSource('/entry_stream');
	} else {
		// Result to xhr polling :(
	}

	source.addEventListener('message', function(e) {
		var data = JSON.parse(e.data);
		message_handler(data);
	}, false);
	
	
	//Needed?
	
	source.addEventListener('open', function(e) {
		// Connection was opened.
	}, false);

	source.addEventListener('error', function(e) {
		if (e.readyState == EventSource.CLOSED) {
			// Connection was closed.
		}
	}, false);	
}


