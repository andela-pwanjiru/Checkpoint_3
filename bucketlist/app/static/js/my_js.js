$(".btn-edit").on("click", function(event) {
  var dataUrl = $(this).data("url");
  $("#updateBucketList").attr('action', dataUrl);
});

$(".btn-item").on("click", function(event) {
  var dataUrl = $(this).data("url");
  $("#updateitem").attr('action', dataUrl);
});

$(".delete-item").on("click", function(event) {
      event.preventDefault();
        var a = $(this).attr('link'); 
        console.log(a); 

     swal(
         {   
            title: "Are you sure?",   
            text: "You will not be able to recover this imaginary file!",   
            type: "warning",   
            showCancelButton: true,   
            confirmButtonColor: "#c62828",   
            confirmButtonText: "Yes, delete it!",   
            cancelButtonText: "No, cancel!",   
            closeOnConfirm: false,   
            closeOnCancel: false 
        }, 
        function(isConfirm) {
            if (isConfirm) {
                $.get( a, function( data ) {
                  
                }); 
                swal("Deleted!", "Your file has been deleted.", "success");   
            } 
            else {     
                swal("Cancelled", "Your file is still safe", "error");  
             } 
            location.reload();
        });
});



