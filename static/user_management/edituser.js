$('#EditUserFormDiv').hide();

function AddEditedUser(first_name, last_name, username, password, email, role_id){
    content = {
        first_name : first_name,
        last_name : last_name,
        username : username,
        password : password,
        email : email,
        role_id : role_id
    }
    get_edited_user_id = window.localStorage.getItem('edited_user_id')
    url = 'edituser/'+get_edited_user_id+''
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

function EditedUserValidation(){
    first_name = $('#first_name_edit').val();
    last_name = $('#last_name_edit').val();
    username = $('#username_edit').val();
    password = $('#password_edit').val();
    email = $('#email_edit').val();
    role_id = $('#RolesDropdown').val()
    
    if(first_name == ''){
        alert('Please enter first name')
    }
    else if(last_name == ''){
        alert('Please enter last name')
    }
    else if(username == ''){
        alert('Please enter user name')
    }
    else if(password == ''){
        alert('Please enter password')
    }
    else if(email == ''){
        alert('Please enter email')
    }
    else if(role_id == null){
        alert('Please select role')
    }
    else{
        var is_email_valid = IsEmail(email)

        if (is_email_valid == true){
            AddEditedUser(first_name, last_name, username, password, email, role_id)
        }
        else{
            alert('Please enter valid email')
        }
    }
}

function GetUserInfoUsingId(user_id){
        // alert(user_id)
        url = 'edituser/'+user_id+''
        $.ajax({
            url : url,
            method : 'GET',
            dataType : 'text',
            async : false,
            success : function(jsonData){
                // alert(jsonData)
                parsed_jsondata = JSON.parse(jsonData)
                console.log(parsed_jsondata)
                // alert(parsed_jsondata.message.length)
                $('#EditUserDiv').hide();
                $('#EditUserFormDiv').show();
                for(i=0;i<parsed_jsondata.message.length;i++){
                    
                    group_id = parsed_jsondata.message[i].group_id
                    first_name = parsed_jsondata.message[i].first_name
                    last_name = parsed_jsondata.message[i].last_name
                    username = parsed_jsondata.message[i].username
                    email = parsed_jsondata.message[i].email

                    $('#first_name_edit').val(first_name)
                    $('#last_name_edit').val(last_name)
                    $('#username_edit').val(username)
                    $('#email_edit').val(email)

                }
    
            },
            error : function(xhr, status, error){
                alert('error')
            }
        })
}

function EditUserValidation(){
    user_id = $('#EditUserDropdown').val();
    if(user_id == null){
        alert('Please select user to edit')
    }
    else{
        window.localStorage.setItem('edited_user_id', user_id)
        GetUserInfoUsingId(user_id)
    }
}

function GetUserList(){
    $.ajax({
        url : 'getuser',
        method : 'GET',
        dataType : 'text',
        async : false,
        success : function(jsonData){
            parsed_jsondata = JSON.parse(jsonData)
            console.log(parsed_jsondata)
            for(i=0; i<parsed_jsondata.message.length; i++){
                temp = '<option value='+parsed_jsondata.message[i].id+'>'+parsed_jsondata.message[i].username+'</option>'
                $('#EditUserDropdown').append(temp)
            }

        },
        error : function(xhr, status, error){
            alert('error')
        }
    })
}

GetUserList()