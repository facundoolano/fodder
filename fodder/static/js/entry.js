function get_entries() {

	$.get('/entries/', function(data) {
		load_template('entrylist.html', data, function(html) {
			$('#inner-container').html(html);
			$("time.timeago").timeago();
		});
	}, 'json')

}

function add_entry(data) {
	var context = {
		entries : [data]
	};
	load_template('entrylist.html', context, function(html) {
		$('#inner-container').prepend(html);
		$("time.timeago").timeago();
	});
}

function show_entryform(){
	replace_template('entryform.html', {}, '#submit-container');
	
	$('#entry_form').submit(function() {
		if ($('#entry_form textarea').val()) {
			$.post('/entries/', {
				entry : $('#entry_form textarea').val()
			}, function() {
				$('#entry_form textarea').val('');
			}, 'json')
		}

		return false;
	});	
}

$(function() {
	
	//TODO if logged in show form
	
	get_entries();
	
	//build entry list with infinite scroll
	$('#inner-container').infinitescroll({
		dataType : 'json',
		appendCallback : false,

		navSelector : "div.navigation",
		// selector for the paged navigation (it will be hidden)

		nextSelector : "div.navigation a:first",
		// selector for the NEXT link (to page 2)

		itemSelector : "#inner-container",
		// selector for all items you'll retrieve
		
	}, function(data, opts) {
		
		if (data.entries.length === 0) {
			opts.state.isDone = true;
			return;
		}
				
		load_template('entrylist.html', data, function(html) {
			$('#inner-container').append(html);
			$("time.timeago").timeago();
		});
	});
	
	$('#inner-container').infinitescroll('retrieve');
	
	
	//listens to add new entries
	sse_subscribe('entry', add_entry);

}); 