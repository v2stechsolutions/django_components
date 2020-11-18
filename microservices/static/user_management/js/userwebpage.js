$( document ).ready(function() {
    $('.userListDiv').hide();
    $('#editUserDetailsDiv').hide();
    $('#saveUserEditedInfo').hide();
    window.localStorage.setItem('isAccessTokenIsRefresh',false)

    add_user_flag = window.localStorage.getItem('add_user')
    edit_user_flag = window.localStorage.getItem('edit_user')
    delete_user_flag = window.localStorage.getItem('delete_user')

    if(add_user_flag == (false || 'false')){
        $('#AddUserDiv').hide();
    }

    if(edit_user_flag == (false || 'false')){
        $('#EditUserDiv').hide();
    }

    if(delete_user_flag == (false || 'false')){
        $('#DeleteUserDiv').hide();
    }
});

function GetNewAccessToken(){
    content = {
        refresh : window.localStorage.getItem('refresh_token')
    }
    $.ajax({
        url : 'token/refresh/',
        method : 'POST',
        data : JSON.stringify(content),
        contentType : 'application/json',
        dataType : "json",
        async : false,
        success : function(JsonData){
            console.log(JsonData)
            console.log(typeof(JsonData))
            console.log(JsonData.access)
            window.localStorage.setItem('access_token', JsonData.access)
            window.localStorage.setItem('isAccessTokenIsRefresh',true)
        }
    })
}

function chekcAccessTokenValidity(){
    $.ajax({
        url : 'user',
        method : 'GET',
        dataType : 'text',
        headers: {"Authorization": "Bearer " + window.localStorage.getItem('access_token')},
        async : false,
        success : function(JsonData){
        },
        error: function(error, xhr, status) {
            GetNewAccessToken()
        }
    })
}

function GetUserList(){
    isAccessTokenIsRefresh = window.localStorage.getItem('isAccessTokenIsRefresh')
    if(isAccessTokenIsRefresh == false || 'false'){
        chekcAccessTokenValidity()
    }
    
    $.ajax({
        url : 'user',
        method : 'GET',
        dataType : 'text',
        headers: {"Authorization": "Bearer " + window.localStorage.getItem('access_token')},
        async : false,
        success : function(JsonData){

            parsed_json = JSON.parse(JsonData)
            $('.userListDiv').empty();
            if(parsed_json.length == 0){
                alert('No user found in database')
            }
            for(i=0; i < parsed_json.length ; i++){
                temp = '<p>'+parsed_json[i].username+'</p>'
                $('.userListDiv').append(temp)
                $('.userListDiv').show();
            }
        },
        error: function(error, xhr, status) {
        }
    })
}

function GetAllRolesSelect(){
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
            for(i=0; i< parsed_json.length ;i++){
                temp = '<option class=role_options value = '+parsed_json[i].id+'>'+parsed_json[i].predefine_roles+'</option>'
                $('#roles').append(temp)
                temp = '<option class=role_options value = '+parsed_json[i].id+'>'+parsed_json[i].predefine_roles+'</option>'
                $('#rolesEdit').append(temp)
            }
        },
        error: function(error, xhr, status) {
        }
    })
}

GetAllRolesSelect()

function AddNewUser(){
    isAccessTokenIsRefresh = window.localStorage.getItem('isAccessTokenIsRefresh')
    if(isAccessTokenIsRefresh == false || 'false'){
        chekcAccessTokenValidity()
    }
    username = $('#userName').val()
    role = $('#roles').val()
    first_name = $('#fullNameFirst').val()
    last_name = $('#fullNameLast').val()
    email = $('#emailAddress').val()
    password = $('#PasswordUser').val()

    content = {
        username : username,
        role : role,
        first_name : first_name,
        last_name : last_name,
        email : email,
        password : password
    }
    
    $.ajax({
        url : 'user',
        method : 'POST',
        data : JSON.stringify(content),
        contentType : "application/json",
        dataType : 'text',
        headers: {"Authorization": "Bearer " + window.localStorage.getItem('access_token')},
        async : false,
        success : function(JsonData){
            alert('New User Added')
            GetUserListPreLoad()
        },
        error: function(error, xhr, status) {
        }
    })
}


function EditUser(){
    isAccessTokenIsRefresh = window.localStorage.getItem('isAccessTokenIsRefresh')
    if(isAccessTokenIsRefresh == false || 'false'){
        chekcAccessTokenValidity()
    }
    username = $('#userNameEdit').val()
    role = $('#rolesEdit').val()
    first_name = $('#fullNameFirstEdit').val()
    last_name = $('#fullNameLastEdit').val()
    email = $('#emailAddressEdit').val()
    password = $('#PasswordUserEdit').val()

    edit_user_id = window.localStorage.getItem('editedUserId')
    url = 'user/'+edit_user_id+''

    content = {
        username : username,
        role : role,
        first_name : first_name,
        last_name : last_name,
        email : email,
        password : password
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
            alert('User Updated')
            GetUserListPreLoad()
        },
        error: function(error, xhr, status) {
        }
    })
}


function AddNewUserValidation(){
    username = $('#userName').val()
    role = $('#roles').val()
    first_name = $('#fullNameFirst').val()
    last_name = $('#fullNameLast').val()
    email = $('#emailAddress').val()
    password = $('#PasswordUser').val()


    if(username == ''){
        alert('Please enter username')
    }
    else if(role == ''){
        alert('Please select role')
    }
    else if(first_name == ''){
        alert('Please enter first name')
    }
    else if(last_name == ''){
        alert('Please enter last name')
    }
    else if(email == ''){
        alert('Please enter email')
    }
    else if(password == ''){
        alert('Please enter password')
    }
    else{
        AddNewUser()
    }
}


function EditUserValidation(){
    username = $('#userNameEdit').val()
    role = $('#rolesEdit').val()
    first_name = $('#fullNameFirstEdit').val()
    last_name = $('#fullNameLastEdit').val()
    email = $('#emailAddressEdit').val()
    password = $('#PasswordUserEdit').val()


    if(username == ''){
        alert('Please enter username')
    }
    else if(role == ''){
        alert('Please select role')
    }
    else if(first_name == ''){
        alert('Please enter first name')
    }
    else if(last_name == ''){
        alert('Please enter last name')
    }
    else if(email == ''){
        alert('Please enter email')
    }
    else if(password == ''){
        alert('Please enter password')
    }
    else{
        EditUser()
    }
}





function GetUserListPreLoad(){
    isAccessTokenIsRefresh = window.localStorage.getItem('isAccessTokenIsRefresh')
    if(isAccessTokenIsRefresh == false || 'false'){
        chekcAccessTokenValidity()
    }
    $('#deleteUser').empty();
    $.ajax({
        url : 'user',
        method : 'GET',
        dataType : 'text',
        headers: {"Authorization": "Bearer " + window.localStorage.getItem('access_token')},
        async : false,
        success : function(JsonData){
            parsed_json = JSON.parse(JsonData)
            console.log(parsed_json)
            for(i=0; i< parsed_json.length ;i++){
                temp = '<option class=delete_user_options value = '+parsed_json[i].id+'>'+parsed_json[i].username+'</option>'
                $('#deleteUser').append(temp)
                temp1 = '<option class=edit_user_options value = '+parsed_json[i].id+'>'+parsed_json[i].username+'</option>'
                $('#editUser').append(temp1)
            }
        },
        error: function(error, xhr, status) {
        }
    })
}

GetUserListPreLoad()


function DeleteSelectedUser(){
    isAccessTokenIsRefresh = window.localStorage.getItem('isAccessTokenIsRefresh')
    if(isAccessTokenIsRefresh == false || 'false'){
        chekcAccessTokenValidity()
    }
    id = $('#deleteUser').val()


    url = 'user/'+id+''
    $.ajax({
        url : url,
        method : 'DELETE',
        dataType : 'text',
        headers: {"Authorization": "Bearer " + window.localStorage.getItem('access_token')},
        async : false,
        success : function(JsonData){
            alert('User Deleted')
            GetUserListPreLoad()
        },
        error: function(error, xhr, status) {
        }
    })

}

function DeleteSelectedUserValidation(){
    id = $('#deleteUser').val()
    if(id == '' || id == null){
        alert('No user found in database')
    }
    else{
        DeleteSelectedUser()
    }
}


function DjangoLogoutUser(){
    isAccessTokenIsRefresh = window.localStorage.getItem('isAccessTokenIsRefresh')
    if(isAccessTokenIsRefresh == false || 'false'){
        chekcAccessTokenValidity()
    }
    $.ajax({
        url : 'logout',
        method : 'GET',
        dataType : 'text',
        headers: {"Authorization": "Bearer " + window.localStorage.getItem('access_token')},
        async : false,
        success : function(JsonData){
            parsed_json = JSON.parse(JsonData)
            message = parsed_json.message
            if(message == 'Logged out successfully'){
                window.location.href= ('/management/')
                window.localStorage.clear();
            }
        },
        error: function(error, xhr, status) {
        }
    })
}


function dashboardHome(){
    isAccessTokenIsRefresh = window.localStorage.getItem('isAccessTokenIsRefresh')
    if(isAccessTokenIsRefresh == false || 'false'){
        chekcAccessTokenValidity()
    }
    
    $.ajax({
        url : 'dashboard',
        method : 'GET',
        dataType : 'text',
        headers: {"Authorization": "Bearer " + window.localStorage.getItem('access_token')},
        async : false,
        success : function(JsonData){
            window.location.href = 'dashboardhtml'
        },
        error: function(error, xhr, status) {
        }
    })
}


function dashboardUser(){
    isAccessTokenIsRefresh = window.localStorage.getItem('isAccessTokenIsRefresh')
    if(isAccessTokenIsRefresh == false || 'false'){
        chekcAccessTokenValidity()
    }
    
    $.ajax({
        url : 'userwebpage',
        method : 'GET',
        dataType : 'text',
        headers: {"Authorization": "Bearer " + window.localStorage.getItem('access_token')},
        async : false,
        success : function(JsonData){
            window.location.href = 'userwebpagehtml'
        },
        error: function(error, xhr, status) {
        }
    })
}

function dashboardRoles(){
    isAccessTokenIsRefresh = window.localStorage.getItem('isAccessTokenIsRefresh')
    if(isAccessTokenIsRefresh == false || 'false'){
        chekcAccessTokenValidity()
    }
    
    $.ajax({
        url : 'rolewebpage',
        method : 'GET',
        dataType : 'text',
        headers: {"Authorization": "Bearer " + window.localStorage.getItem('access_token')},
        async : false,
        success : function(JsonData){
            window.location.href = 'rolewebpagehtml'
        },
        error: function(error, xhr, status) {
        }
    })
}

function checkEditUserID(){
    userId = $('#editUser').val()
    edit_user_id = window.localStorage.setItem('editedUserId', userId)
    isAccessTokenIsRefresh = window.localStorage.getItem('isAccessTokenIsRefresh')
    if(isAccessTokenIsRefresh == false || 'false'){
        chekcAccessTokenValidity()
    }
    url = 'user/'+userId+''
    $.ajax({
        url : url,
        method : 'GET',
        dataType : 'text',
        headers: {"Authorization": "Bearer " + window.localStorage.getItem('access_token')},
        async : false,
        success : function(JsonData){
            console.log(JsonData)
            parsed_json = JSON.parse(JsonData)
            console.log(parsed_json)
            console.log(parsed_json.username)
            username = parsed_json.username
            role = parsed_json.role_id
            first_name = parsed_json.first_name
            last_name = parsed_json.last_name
            email = parsed_json.email
            password = parsed_json.password

            // alert(JsonData)
            // GetAllRolesSelect()
            $('#selectEditUserDiv').hide()
            $('#userNameEdit').val(username)
            $('#rolesEdit').val(role)
            $('#fullNameFirstEdit').val(first_name)
            $('#fullNameLastEdit').val(last_name)
            $('#emailAddressEdit').val(email)
            $('#PasswordUserEdit').val(password)
            $('#editUserDetailsDiv').show();
            $('#saveUserEditedInfo').show();

        },
        error: function(error, xhr, status) {
        }
    })

}

function cancelEditDiv(){
    $('#editUserDetailsDiv').hide();
    $('#saveUserEditedInfo').hide();
    $('#selectEditUserDiv').show()
}