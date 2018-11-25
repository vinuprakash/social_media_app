$(document).ready(function(){

  $('#btn-comment-edit').click(function(){
    var edit_href = $(this).parent().children('.btn-edit-comment').attr('href');
    $('#comment-edit-form').attr('action',edit_href);

    var comment_text=$(this).parent().parent().children('.comment-content').html();

    $('#id_content').text(comment_text)

    var comment_div = $('#id_content').parent().children('.medium-editor-element');
    comment_div.removeClass('medium-editor-placeholder')
    comment_div.html(comment_text);
  });
  
});
