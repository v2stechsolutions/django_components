function LoginUserManagement(username, password){
    console.log(username, password)
    content = {
        username : username,
        password : password
    }
    $.ajax({
        url : "token/",
        method : "POST",
        data : JSON.stringify(content),
        contentType : "application/json",
        dataType : "text",
        async : false,
        success : function(jsonData){
            parsed_jsondata = JSON.parse(jsonData)
            access_token = parsed_jsondata.access
            refresh_token = parsed_jsondata.refresh
            status = parsed_jsondata.status
            if(status != 'Please enter valid credentials'){
                window.localStorage.setItem('access_token', access_token)
                window.localStorage.setItem('refresh_token', refresh_token)
                // window.location.href = 'dashboard'
                dashboardHome()
            }
            else{
                alert('Please enter valid credentials')
            }
        }
    })
}

function LoginUserDjango(username, password){
    console.log(username, password)
    content = {
        username : username,
        password : password
    }
    $.ajax({
        url : "login/",
        method : "POST",
        data : JSON.stringify(content),
        contentType : "application/json",
        dataType : "text",
        async : false,
        success : function(jsonData){

            parsed_jsondata = JSON.parse(jsonData)
            message = parsed_jsondata.message
            console.log(message)
            add_user = message[0].add_user
            edit_user = message[0].edit_user
            delete_user = message[0].delete_user
            add_role = message[0].add_role
            edit_role = message[0].edit_role
            delete_role = message[0].delete_role
            window.localStorage.setItem('add_user',add_user)
            window.localStorage.setItem('edit_user', edit_user)
            window.localStorage.setItem('delete_user',delete_user)
            window.localStorage.setItem('add_role',add_role)
            window.localStorage.setItem('edit_role', edit_role)
            window.localStorage.setItem('delete_role',delete_role)
            
            if(message != 'Please enter valid credentials'){
                LoginUserManagement(username, password)
            }
            else{
                alert("Please enter valid credentials")
            }
        }
    })
}

function CheckLoginUserManagementValidation(){
    username = $('#userName').val()
    password = $('#passWord').val()

    if(username == '' && password == ''){
        alert('Please enter username and password')
    }
    else if(username == ''){
        alert('Please enter username')
    }
    else if(password == ''){
        alert('Please enter password')
    }
    else{
        LoginUserDjango(username, password)
    }
}