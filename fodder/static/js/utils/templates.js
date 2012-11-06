
/**
 * Compiles the handlebars template at the given path, evaluates it with the
 * given context and passes it to the callback.
 * 
 * The path should be relative to the handlebars templates directory
 */
function load_template(path, context, callback){
	var template, html;
		
	// get the template
	$.ajax({
        url: '/static/templates/' + path,
            cache: false, //true,
            
            success: function(data) {
                template = Handlebars.compile(data);
                html = template(context)
                
                callback(html);
            }
    });
	
}

/**
 * Loads the template with the given context, and replaces the result in the
 * container.
 */
function replace_template(path, context, container_id) {
	load_template(path, context, function(html){
		$(container_id).html(html);
	});
}

/*** Handlebars.js Helper functions ***/ 