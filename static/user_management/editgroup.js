$('#EditGroupFormDiv').hide();

function SaveEditGroup(group_name, add_user, change_user, delete_user, add_group, change_group, delete_group){
    content = {
        group_name : group_name,
        add_user : add_user,
        change_user : change_user,
        delete_user : delete_user,
        add_group : add_group,
        change_group : change_group,
        delete_group : delete_group
    }

    edited_group_id = window.localStorage.getItem('edited_group_id')
    url = 'editgroup/'+edited_group_id+''

    $.ajax({
        url : url,
        method : "PUT",
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


function EditedGroupValidation(){
    edited_group_name = $('#group_name_edit').val();
    add_user = $('#AddUserCheckboxForEditGroup').is(':checked'); 
    change_user = $('#EditUserCheckboxForEditGroup').is(':checked'); 
    delete_user = $('#DeleteUserCheckboxForEditGroup').is(':checked'); 
    add_group = $('#AddGroupCheckboxForEditGroup').is(':checked'); 
    change_group = $('#EditGroupCheckboxForEditGroup').is(':checked'); 
    delete_group = $('#DeleteGroupCheckboxForEditGroup').is(':checked');

    // alert(edited_group_name)
    if(edited_group_name == null){
        alert('Please enter group name')
    }
    else{
        SaveEditGroup(edited_group_name, add_user, change_user, delete_user, add_group, change_group, delete_group)
    }


}


function EditGroup(selected_group_id){
    url = 'editgroup/'+selected_group_id+''
    $.ajax({
        url : url,
        method : 'GET',
        dataType : 'text',
        async : false,
        success : function(jsonData){
            // alert(jsonData)
            console.log(jsonData)
            parsed_jsondata = JSON.parse(jsonData)
            console.log(parsed_jsondata)
            console.log(parsed_jsondata.message)
            console.log(parsed_jsondata.message.length)
            
            $('#EditGroupFormDiv').show();
            $('#EditGroupDiv').hide();

            for(i=0; i<parsed_jsondata.message.length;i++){

                group_name = parsed_jsondata.message[i].name
                perm_list = parsed_jsondata.message[i].perms
                
                add_user_flag = perm_list.includes('add_user')
                change_user_flag = perm_list.includes('change_user')
                delete_user_flag = perm_list.includes('delete_user')
                add_group_flag = perm_list.includes('add_group')
                change_group_flag = perm_list.includes('change_group')
                delete_group_flag = perm_list.includes('delete_group')

                $('#group_name_edit').val(group_name)

                if(add_user_flag == true){
                    $('#AddUserCheckboxForEditGroup').prop('checked', true);
                }
                if(change_user_flag == true){
                    $('#EditUserCheckboxForEditGroup').prop('checked', true)
                }
                if(delete_user_flag == true){
                    $('#DeleteUserCheckboxForEditGroup').prop('checked', true)
                }
                if(add_group_flag == true){
                    $('#AddGroupCheckboxForEditGroup').prop('checked', true)
                }
                if(change_group_flag == true){
                    $('#EditGroupCheckboxForEditGroup').prop('checked', true)
                }
                if(delete_group_flag == true){
                    $('#DeleteGroupCheckboxForEditGroup').prop('checked', true)
                }



                
            }

        },
        error : function(xhr, status, error){
            alert('error')
        }
    })
}

function EditGroupValidation(){
    selected_group_id = $('#EditGroupDropdown').val();
    // alert(selected_group_id)
    if(selected_group_id == null){
        alert('Please enter group to edit')
    }
    else{
        window.localStorage.setItem('edited_group_id', selected_group_id)
        $('#AddUserCheckboxForEditGroup').prop('checked', false);
        $('#EditUserCheckboxForEditGroup').prop('checked', false)
        $('#DeleteUserCheckboxForEditGroup').prop('checked', false)
        $('#AddGroupCheckboxForEditGroup').prop('checked', false)
        $('#EditGroupCheckboxForEditGroup').prop('checked', false)
        $('#DeleteGroupCheckboxForEditGroup').prop('checked', false)
        EditGroup(selected_group_id)
    }
}

function GetGroupList(){
    $.ajax({
        url : 'getgroup',
        method : 'GET',
        dataType : 'text',
        async : false,
        success : function(jsonData){
            parsed_jsondata = JSON.parse(jsonData)
            console.log(parsed_jsondata)
            for(i=0; i<parsed_jsondata.message.length; i++){
                temp = '<option value='+parsed_jsondata.message[i].id+'>'+parsed_jsondata.message[i].name+'</option>'
                $('#EditGroupDropdown').append(temp)
            }
        },
        error : function(xhr, status, error){
            alert('error')
        }
    })
}

GetGroupList()