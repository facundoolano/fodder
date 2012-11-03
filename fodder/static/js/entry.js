function get_entries() {
	$.get('/entries', function(data) {
		replace_template('entrylist.html', data, '#inner-container');
	}, 'json')
}

function add_entry(data) {
	var context = { entries : [data]};
	load_template('entrylist.html', context, function(html){
		$('#inner-container').prepend(html);
		});
}

$(function() {
	$('#entry_form').submit(function() {
		$.post('/new_entry', {
			entry : $('#entry_form textarea').val()
		}, function(){
			$('#entry_form textarea').val('');
		}, 'json')
		return false;
	});

	get_entries();

});