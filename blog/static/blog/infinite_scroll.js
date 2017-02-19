$(document).ready(function() {
	var win = $(window);
	var page_num=1;
	var current_page=1;
	
	$(win).scroll(function(){

		if (page_num === current_page){
		if ($(document).height() - win.scrollTop() <= win.height()+400) {
		page_num+=1
		var URI = window.location.pathname.split( '/' )
		if(URI[1] === 'page' || URI[1] === ''){
		$.ajax({
                url: '/page/'+page_num,
                dataType: 'html',
                success: function(html) {
                	if (html === ''){
                		$('#post_list').append('End of posts');
                	}
                	else{
                		$('#post_list').append(html);
                		current_page+=1;
                	}

                }
            });
		}
		else if(URI[1] === 'tagged'){			
				var request_url = '/tagged/'+URI[2]+'/page/'+page_num;
				$.ajax({
                url: request_url,
                dataType: 'html',
                success: function(html) {
                	if (html === ''){
                		$('#post_list').append('End of posts');
                	}
                	else{
                		$('#post_list').append(html);
                		current_page+=1;
                	}

                }
            });
		  }
          else{
                var request_url = '/author/'+URI[2]+'/page/'+page_num;
                $.ajax({
                url: request_url,
                dataType: 'html',
                success: function(html) {
                    if (html === ''){
                        $('#post_list').append('End of posts');
                    }
                    else{
                        $('#post_list').append(html);
                        current_page+=1;
                    }

                }
            });
          }
	}}
})
})