$(document).ready(function(){
	$('div.ip').hover(function(){
		my_element = $(this);
		$.getJSON("getinfo/"+$(this).attr("id"), function(json, status){
			if(status == "success")
				my_element.innerHTML = "<span>"+json.update_time+"</span>"
									  +"<span>"+json.port+"</span>"
									  +"<span>"+json.link_speed+"</span>"
									  +"<span>"+json.ping_ex+"</span>"
									  +"<span>"+json.ping+"</span>";
		});
	});
});