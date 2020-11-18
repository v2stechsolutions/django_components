function DeleteGroup(selected_group_id){
    url = 'deletegroup/'+selected_group_id+''
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

function DeleteGroupValidation(){
    selected_group_id = $('#EditGroupDropdown').val();
    // alert(selected_group_id)
    if(selected_group_id == null){
        alert('Please select group to delete')
    }
    else{
        DeleteGroup(selected_group_id)
    }
}
