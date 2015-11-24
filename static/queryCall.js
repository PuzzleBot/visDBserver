var HTMLstring = '';

function testQuery(){
    console.log("Test begin");
    HTMLstring = HTMLstring + "Test begin.\n";
    jQuery.ajax({
                url: "http://127.0.0.1:5001/accounts/createAccount",
                type: "PUT",
                success: function(data){ console.log("Create success.\n"); HTMLstring = HTMLstring + "Create success.\n" + JSON.stringify(data, null, 4) + "\n"; document.getElementById("output").innerHTML = HTMLstring;},
                crossDomain: true,
                dataType: 'json',
                contentType: "application/json; charset=UTF-8",
                data: JSON.stringify({ username: "user1", password: "pass1", email: "user1@gmail.com", firstName: "theUser", surname: "theLast", teamCaptain: 'false', accessibility: 'false'})
                });
    
	jQuery.ajax({
                url: "http://127.0.0.1:5001/accounts/validateLogin",
                type: "PUT",
                success: function(data){ console.log("Login success: \n"); HTMLstring = HTMLstring + "Login success.\n" + JSON.stringify(data, null, 4) + "\n"; document.getElementById("output").innerHTML = HTMLstring;},
                crossDomain: true,
                dataType: 'json',
                contentType: "application/json; charset=UTF-8",
                data: JSON.stringify({ username: "user1" , password: "pass1" })
                });
    
    jQuery.ajax({
                url: "http://127.0.0.1:5001/accounts/user1/getDetails",
                type: "GET",
                success: function(data){ console.log("Get details success.\n"); HTMLstring = HTMLstring + "Get details success.\n" + JSON.stringify(data, null, 4) + "\n"; document.getElementById("output").innerHTML = HTMLstring;},
                dataType: 'json',
                crossDomain: true,
                contentType: "application/json; charset=UTF-8",
                });
    
    jQuery.ajax({
                url: "http://127.0.0.1:5001/docs/faq",
                type: "GET",
                success: function(data){ console.log("Get faq success.\n"); HTMLstring = HTMLstring + "Get faq success.\n" + JSON.stringify(data, null, 4) + "\n"; document.getElementById("output").innerHTML = HTMLstring;},
                crossDomain: true,
                dataType: 'json',
                contentType: "application/json; charset=UTF-8",
                });
    
    jQuery.ajax({
                url: "http://127.0.0.1:5001/docs/terms",
                type: "GET",
                success: function(data){ console.log("Get terms success.\n"); HTMLstring = HTMLstring + "Get terms success.\n" + JSON.stringify(data, null, 4) + "\n"; document.getElementById("output").innerHTML = HTMLstring;},
                crossDomain: true,
                dataType: 'json',
                contentType: "application/json; charset=UTF-8",
                });
}