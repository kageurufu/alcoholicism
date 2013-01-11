$(function() {
	$("select").each(function(id, elem) {
		console.log(elem);
		$(elem).children().each(function(id, elem) {
			if ($(elem).attr('value') == $(elem).parent().attr('data')) {
				$(elem).attr('selected', 'true');

			};
		});
	});
});