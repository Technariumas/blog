$(document).ready(function() {
	var win = $(window);
	var page_num=1;
	var current_page=1;
	
	$(win).scroll(function(){

		if (page_num === current_page){
		if ($(document).height() - win.scrollTop() <= win.height()+400) {
		page_num+=1
		var URI = window.location.pathname.split( '/' )
		if(URI[2] === 'page' || URI[2] === ''){
		$.ajax({
                url: '/blog/page/'+page_num+'/',
                dataType: 'html',
                success: function(html) {
                	if (html.length < 5){ //response is empty
                		$('#post_list').append('No more posts');
                	}
                	else{
                		$('#post_list').append(html);
                		current_page+=1;
                	}

                }
            });
		}
		else if(URI[2] === 'tagged'){			
				var request_url = '/blog/tagged/'+URI[3]+'/page/'+page_num+'/';
				$.ajax({
                url: request_url,
                dataType: 'html',
                success: function(html) {
                	if (html.length < 5){ //response is empty
                		$('#post_list').append('No more posts');
                	}
                	else{
                		$('#post_list').append(html);
                		current_page+=1;
                	}

                }
            });
		  }
          else if(URI[2] === 'search'){           
                var query = window.location.search.split('/')[0];
                query = query.match(/\?q=(.+)/)[1];
                var request_url = '/blog/search/'+ query +'/page/'+page_num+'/';
                $.ajax({
                url: request_url,
                dataType: 'html',
                success: function(html) {
                    if (html.length < 5){ //response is empty
                        $('#post_list').append('No more posts');
                    }
                    else{
                        $('#post_list').append(html);
                        current_page+=1;
                    }

                }
            });
          }
          else{
                var request_url = '/blog/author/'+URI[3]+'/page/'+page_num+'/';
                $.ajax({
                url: request_url,
                dataType: 'html',
                success: function(html) {
                    if (html.length < 5){ //response is empty
                        $('#post_list').append('No more posts');
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



