$( document ).ready(function() {
    $('.roleListDiv').hide();
    $('#PermissionEditDiv').hide();
    $('#saveRoleEditedInfo').hide();

    add_role_flag = window.localStorage.getItem('add_role')
    edit_role_flag = window.localStorage.getItem('edit_role')
    delete_role_flag = window.localStorage.getItem('delete_role')


    if(add_role_flag == (false || 'false')){
        $('#AddRoleDiv').hide();
    }

    if(edit_role_flag == (false || 'false')){
        $('#EditRoleDiv').hide();
    }

    if(delete_role_flag == (false || 'false')){
        $('#DeleteRoleDiv').hide();
    }
});

function GetRoleList(){
    isAccessTokenIsRefresh = window.localStorage.getItem('isAccessTokenIsRefresh')
    if(isAccessTokenIsRefresh == false || 'false'){
        chekcAccessTokenValidity()
    }
    
    $.ajax({
        url : 'role',
        method : 'GET',
        dataType : 'text',
        headers: {"Authorization": "Bearer " + window.localStorage.getItem('access_token')},
        async : false,
        success : function(JsonData){

            parsed_json = JSON.parse(JsonData)
            console.log(parsed_json)
            $('.roleListDiv').empty();

            if(parsed_json.length == 0){
                alert('No role found in database')
            }  
            
            for(i=0; i < parsed_json.length ; i++){
                temp = '<p>'+parsed_json[i].predefine_roles+'</p>'
                $('.roleListDiv').append(temp)
                $('.roleListDiv').show();
            }
        },
        error: function(error, xhr, status) {
        }
    })
}

function AddPermissionToRole(id){
    
    adduser = $('#addUserCheckbox').is(":checked")
    edituser = $('#editUserCheckbox').is(":checked")
    deleteuser = $('#deleteUserCheckbox').is(":checked")
    addrole = $('#addRoleCheckbox').is(":checked")
    editrole = $('#editRoleCheckbox').is(":checked")
    deleterole = $('#deleteRoleCheckbox').is(":checked")
    isAccessTokenIsRefresh = window.localStorage.getItem('isAccessTokenIsRefresh')
    if(isAccessTokenIsRefresh == false || 'false'){
        chekcAccessTokenValidity()
    }
    content = {
        "role" :id,
        "add_user" : adduser,
        "edit_user" : edituser,
        "delete_user" : deleteuser,
        "add_role" : addrole,
        "edit_role" : editrole,
        "delete_role" : deleterole
    }
    $.ajax({
        url : 'permission/',
        method : 'POST',
        data : JSON.stringify(content),
        contentType : "application/json",
        dataType : "text",
        headers: {"Authorization": "Bearer " + window.localStorage.getItem('access_token')},
        async : false,
        success : function(JsonData){
            // alert(JsonData)
        }
    })

}

function AddNewRole(){
    isAccessTokenIsRefresh = window.localStorage.getItem('isAccessTokenIsRefresh')
    if(isAccessTokenIsRefresh == false || 'false'){
        chekcAccessTokenValidity()
    }
    predefine_roles = $('#roleName').val()

    content = {
        predefine_roles : predefine_roles,
    }
    
    $.ajax({
        url : 'role',
        method : 'POST',
        data : JSON.stringify(content),
        contentType : "application/json",
        dataType : 'text',
        headers: {"Authorization": "Bearer " + window.localStorage.getItem('access_token')},
        async : false,
        success : function(JsonData){
            // alert(JsonData)
            parsed_json = JSON.parse(JsonData)
            // alert(parsed_json.id)
            id = parsed_json.id
            alert('New Role Added')
            GetRoleListPreLoad()
            AddPermissionToRole(id)
        },
        error: function(error, xhr, status) {
            alert('Role already in database')
        }
    })
}


function AddNewRoleValidation(){
    rolename = $('#roleName').val()

    if(rolename == ''){
        alert('Please enter role')
    }
    else{
        AddNewRole()
    }
}





function GetRoleListPreLoad(){
    isAccessTokenIsRefresh = window.localStorage.getItem('isAccessTokenIsRefresh')
    if(isAccessTokenIsRefresh == false || 'false'){
        chekcAccessTokenValidity()
    }
    $('#deleteRole').empty();
    $.ajax({
        url : 'role',
        method : 'GET',
        dataType : 'text',
        headers: {"Authorization": "Bearer " + window.localStorage.getItem('access_token')},
        async : false,
        success : function(JsonData){
            parsed_json = JSON.parse(JsonData)
            console.log(parsed_json)
            for(i=0; i< parsed_json.length ;i++){
                temp = '<option class=delete_user_options value = '+parsed_json[i].id+'>'+parsed_json[i].predefine_roles+'</option>'
                $('#deleteRole').append(temp)
                temp = '<option class=edit_user_options value = '+parsed_json[i].id+'>'+parsed_json[i].predefine_roles+'</option>'
                $('#editRoleDropdown').append(temp)
            }
        },
        error: function(error, xhr, status) {
        }
    })
}

GetRoleListPreLoad()


function DeleteSelectedRole(){
    isAccessTokenIsRefresh = window.localStorage.getItem('isAccessTokenIsRefresh')
    if(isAccessTokenIsRefresh == false || 'false'){
        chekcAccessTokenValidity()
    }
    id = $('#deleteRole').val()


    url = 'role/'+id+''
    $.ajax({
        url : url,
        method : 'DELETE',
        dataType : 'text',
        headers: {"Authorization": "Bearer " + window.localStorage.getItem('access_token')},
        async : false,
        success : function(JsonData){
            alert('Role Deleted')
            // GetRoleListPreLoad()
        },
        error: function(error, xhr, status) {
        }
    })

}

function DeleteSelectedRoleValidation(){
    id = $('#deleteRole').val()
    if(id == '' || id == null){
        alert('No role found in database')
    }
    else{
        DeleteSelectedRole()
    }
}

function checkEditRoleId(){
    a = $('#editRoleDropdown').val();
    // alert(a)
    roleId = $('#editRoleDropdown').val()
    edit_role_id = window.localStorage.setItem('editedRoleId', roleId)
    isAccessTokenIsRefresh = window.localStorage.getItem('isAccessTokenIsRefresh')
    if(isAccessTokenIsRefresh == false || 'false'){
        chekcAccessTokenValidity()
    }

    url = 'permission/'+roleId+''
    $.ajax({
        url : url,
        method : 'GET',
        dataType : 'text',
        headers: {"Authorization": "Bearer " + window.localStorage.getItem('access_token')},
        async : false,
        success : function(JsonData){
            // alert(JsonData)
            parsed_json = JSON.parse(JsonData)
            console.log(parsed_json)
            console.log(parsed_json.message)
            message = parsed_json.message
            add_user = message.add_user
            edit_user = message.edit_user
            delete_user = message.delete_user
            add_role =message.add_role
            edit_role = message.edit_role
            delete_role = message.delete_role
            // alert(delete_role)

            if(add_user == (true || 'true')){
                $( "#addUserCheckboxEdit" ).prop( "checked", true );
            }
            else{
                $( "#addUserCheckboxEdit" ).prop( "checked", false );
            }
            if(edit_user == (true || 'true')){
                $( "#editUserCheckboxEdit" ).prop( "checked", true );
            }
            else{
                $( "#editUserCheckboxEdit" ).prop( "checked", false );
            }
            if(delete_user == (true || 'true')){
                $( "#deleteUserCheckboxEdit" ).prop( "checked", true );
            }
            else{
                $( "#deleteUserCheckboxEdit" ).prop( "checked", false );
            }
            if(add_role == (true || 'true')){
                $( "#addRoleCheckboxEdit").prop( "checked", true );
            }
            else{
                $( "#addRoleCheckboxEdit").prop( "checked", false );
            }
            if(edit_role == (true || 'true')){
                $( "#editRoleCheckboxEdit").prop( "checked", true );
            }
            else{
                $( "#editRoleCheckboxEdit").prop( "checked", false );
            }
            if(delete_role == (true || 'true')){
                $( "#deleteRoleCheckboxEdit").prop( "checked", true );
            }
            else{
                $( "#deleteRoleCheckboxEdit").prop( "checked", false );
            }
            $('#PermissionEditDiv').show();
            $('#saveRoleEditedInfo').show();
        },
        error: function(error, xhr, status) {
        }
    })

}

function cancelEditDivRole(){
    $('#PermissionEditDiv').hide();
    $('#saveRoleEditedInfo').hide();
}

function EditRoleValidation(){
    

    isAccessTokenIsRefresh = window.localStorage.getItem('isAccessTokenIsRefresh')
    if(isAccessTokenIsRefresh == false || 'false'){
        chekcAccessTokenValidity()
    }
    adduser = $('#addUserCheckboxEdit').is(":checked")
    edituser = $('#editUserCheckboxEdit').is(":checked")
    deleteuser = $('#deleteUserCheckboxEdit').is(":checked")
    addrole = $('#addRoleCheckboxEdit').is(":checked")
    editrole = $('#editRoleCheckboxEdit').is(":checked")
    deleterole = $('#deleteRoleCheckboxEdit').is(":checked")

    edit_role_id = window.localStorage.getItem('editedRoleId')
    url = 'permission/'+edit_role_id+''
    // alert(url)
    content = {
        add_user : adduser,
        edit_user : edituser,
        delete_user : deleteuser,
        add_role : addrole,
        edit_role : editrole,
        delete_role : deleterole
    }
    
    $.ajax({
        url : url,
        method : 'PUT',
        data : JSON.stringify(content),
        contentType : "application/json",
        dataType : 'text',
        headers: {"Authorization": "Bearer " + window.localStorage.getItem('access_token')},
        async : false,
        success : function(JsonData){
            alert('Role Updated')
            // GetUserListPreLoad()
            GetRoleList()
        },
        error: function(error, xhr, status) {
        }
    })
}