function loadXMLDoc(url, cfunc)
{
	if (window.XMLHttpRequest)
	{
		xmlhttp=new XMLHttpRequest();
	}
	else
	{
		xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	}
	xmlhttp.onreadystatechange=cfunc;
	xmlhttp.open("GET",url,true);
	xmlhttp.send();
}

function show_ping(row_id)
{
	ip=document.getElementById(row_id).childNodes[3].innerText;
	url="/ping/"+ip+"/";
	loadXMLDoc(url, function()
	{
  		if (xmlhttp.readyState==4 && xmlhttp.status==200)
    	{
    		document.getElementById(row_id).childNodes[7].innerText=xmlhttp.responseText;
    	}
	});
}

function mouse_over(row_id)
{
	show_ping(row_id);
	color=document.getElementById(row_id).style.background;
	if(color!="rgb(100, 149, 237)")
	{
		document.getElementById(row_id).style.background="#e0ffff";
	}
}

function fade_out(row_id)
{
	color=document.getElementById(row_id).style.background;
	if(color!="rgb(100, 149, 237)")
	{
		document.getElementById(row_id).style.background="#ffffff";
	}
}

function select_item(row_id, enter_it)
{
	ip=document.getElementById(row_id).childNodes[3].innerText;
	url="/select/"+ip+"/"+enter_it+"/";
	loadXMLDoc(url, function()
	{
		if(xmlhttp.readyState==4 && xmlhttp.status==200)
		{
			res_text = xmlhttp.responseText;
			if(res_text == "Selected")
				document.getElementById(row_id).childNodes[7].innerHTML = "<span style='color:#00FF00'>"+xmlhttp.responseText+"</span>";
			else
				document.getElementById(row_id).childNodes[7].innerHTML = "<span style='color:#FF4500'>"+xmlhttp.responseText+"</span>";
			document.getElementById(row_id).style.background="#6495ed";
		}
	});
	
	if(window.last_selected==null)
	{
		window.last_selected=row_id;
	}
	else
	{
		//show_ping(window.last_selected);
		document.getElementById(window.last_selected).style.background="#ffffff";
		
	}
	window.last_selected = row_id;
}