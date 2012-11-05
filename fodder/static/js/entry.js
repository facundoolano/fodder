function get_entries() {
	
	$.get('/entries', function(data) {
		load_template('entrylist.html', data, function(html){
			$('#inner-container').html(html);
			$("time.timeago").timeago();
		});
	}, 'json')
	
}

function add_entry(data) {
	var context = { entries : [data]};
	load_template('entrylist.html', context, function(html){
		$('#inner-container').prepend(html);
		$("time.timeago").timeago();
		});
}

$(function() {
	$('#entry_form').submit(function() {
		if($('#entry_form textarea').val()) {
			$.post('/new_entry', {
				entry : $('#entry_form textarea').val()
			}, function(){
				$('#entry_form textarea').val('');
			}, 'json')
		}
		
		return false;
	});

	get_entries();
	
	//listens to add new entries
	//sse_subscribe('entry', add_entry);

});