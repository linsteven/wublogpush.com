$(function(){
	$('button').click(function(){
		var user = $('#txtEmail').val();
		$.ajax({
			url: '/subscribe',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				alert(response);
			},
			error: function(error){

			}
		});
	});
});
