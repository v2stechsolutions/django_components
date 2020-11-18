function DeleteUser(selected_user_id){
    url = 'deleteuser/'+selected_user_id+''
    $.ajax({
        url : url,
        method : 'DELETE',
        dataType : 'text',
        async : false,
        success : function(jsonData){
            parsed_jsondata = JSON.parse(jsonData)
            window.location.href = '/dashboard'
            alert(parsed_jsondata.message)
            // window.location.reload();
            
        },
        error: function(xhr, status, error) {
            parsed_jsondata = JSON.parse(xhr.responseText)
            alert('User not found')
          }
    })
}

function DeleteUserValidation(){
    selected_user_id = $('#EditUserDropdown').val();
    if(selected_user_id == null){
        alert('Please select role to delete')
    }
    else{
        DeleteUser(selected_user_id)
    }
}
