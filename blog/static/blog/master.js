$(document).ready(function() {
	var win = $(window);
	var page_num=1;
	var current_page=1;
	$(win).scroll(function(){
		if (page_num === current_page){
		if ($(document).height() - win.scrollTop() <= win.height()+400) {
		page_num+=1
		console.log(page_num);
		$.ajax({
                url: '/page/'+page_num,
                dataType: 'html',
                success: function(html) {
                	$('#post_list').append(html);
                	current_page+=1;
                	console.log(html)
                }
            });
	}}
})
})