function AddNewRole(group_name, add_user, change_user, delete_user, add_group, change_group, delete_group){
    content = {
        group_name : group_name,
        add_user : add_user,
        change_user : change_user,
        delete_user : delete_user,
        add_group : add_group,
        change_group : change_group,
        delete_group : delete_group
    }

    $.ajax({
        url : "addgroup",
        method : "POST",
        data : JSON.stringify(content),
        contentType : "application/json",
        dataType : "text",
        async : false,
        success : function(jsonData){
            parsed_jsondata = JSON.parse(jsonData)
            window.location.href = '/dashboard'
            alert(parsed_jsondata.message)
            // window.location.reload();
        },
        error: function(xhr, status, error) {
            parsed_jsondata = JSON.parse(xhr.responseText)
            alert(parsed_jsondata.message)
          }
    })
}

function NewRoleValidation(){
    group_name = $('#group_name').val();
    add_user = $('#AddUserCheckbox').is(':checked'); 
    change_user = $('#EditUserCheckbox').is(':checked'); 
    delete_user = $('#DeleteUserCheckbox').is(':checked'); 
    add_group = $('#AddGroupCheckbox').is(':checked'); 
    change_group = $('#EditGroupCheckbox').is(':checked'); 
    delete_group = $('#DeleteGroupCheckbox').is(':checked');

    if(group_name == ''){
        alert('Please enter group')
    }
    else{
        AddNewRole(group_name, add_user, change_user, delete_user, add_group, change_group, delete_group)
    }
}