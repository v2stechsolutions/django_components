function AddNewUser(first_name, last_name, username, password, email, role_id){
    content = {
        first_name : first_name,
        last_name : last_name,
        username : username,
        password : password,
        email : email,
        role_id : role_id
    }
    $.ajax({
        url : "adduser",
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

function IsEmail(email) {
    var regex = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;

    if(!regex.test(email)) {
        return false;
    }
    else{
         return true;
    }
}

function NewUserValidation(){
    first_name = $('#first_name').val();
    last_name = $('#last_name').val();
    username = $('#username').val();
    password = $('#password').val();
    email = $('#email').val();
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
            AddNewUser(first_name, last_name, username, password, email, role_id)
        }
        else{
            alert('Please enter valid email')
        }
    }
}



function getGroupsFromDatabase(){
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
                $('#RolesDropdown').append(temp)
            }

        },
        error : function(xhr, status, error){
            alert('error')
        }
    })
}

getGroupsFromDatabase()