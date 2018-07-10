
// Ajax for posting
function create_post(){
  $.ajax({
      url: $('#post-form').attr('post-url'), //endpoint
      type: "POST",
      data: $('#post-form').serialize(),

      //Successful response
      success : function(json) {
        if (json.success == 'false'){
          $('#results').html("<div class='alert'>Error, Please fill out all fields and submit again</div>");
        }
        console.log(json)
        console.log('success')
      },

      //Non success
      error : function(xhr, errmsg, err) {
        $('#results').html("<div class='alert-bix alert radius' data-alert>Error time:"+errmsg+"<a href='#' class='close'>&times;</a></div>");
        console.log(xhr.status+": " + xhr.responseText);
      }
  })

  $('#post-form')[0].reset();

};

// function update_table(){
//   $ajax({
//     url:
//     type:
//     data:
//   })
// }
// Submit post on submit
$('#post-form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    create_post();
    //update_table();
});
