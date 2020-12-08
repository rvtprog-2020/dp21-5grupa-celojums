let isTrue1 = false;
let isTrue2 = false;
let isTrue3 = false;
let isTrue4 = false;
let isTrue5 = false;
let isTrue6 = false;
let botton = document.getElementById("botton");

window.addEventListener("load", function(){
    var username = document.getElementById("username");
    var name = document.getElementById("name");
    var lastName = document.getElementById("last-name");
    var password = document.getElementById("password");
    var passwordConfirm = document.getElementById("password-confirm");
    var robot = document.getElementById("robot");

    username.addEventListener("keyup", function(){
        if (username.value.length >= 2) {
            document.getElementById("username").style.cssText = "border-bottom: 1px solid green";
            isTrue1 = true;
        } else {
            document.getElementById("username").style.cssText = "border-bottom: 1px solid rgba(255, 0, 0, 0.5)";
            isTrue1 = false;
        }
        submit()
    })
    name.addEventListener("keyup", function(){
        if (name.value.length >= 2) {
            document.getElementById("name").style.cssText = "border-bottom: 1px solid green";
            isTrue2 = true;
        } else {
            document.getElementById("name").style.cssText = "border-bottom: 1px solid rgba(255, 0, 0, 0.5)";
            isTrue2 = false;
        }
        submit()
    })
    lastName.addEventListener("keyup", function(){
        if (lastName.value.length >= 2) {
            document.getElementById("last-name").style.cssText = "border-bottom: 1px solid green";
            isTrue3 = true;
        } else {
            document.getElementById("last-name").style.cssText = "border-bottom: 1px solid rgba(255, 0, 0, 0.5)";
            isTrue3 = false;
        }
        submit()
    })
    password.addEventListener("keyup", function(){
        if (password.value.length >= 6) {
            document.getElementById("password").style.cssText = "border-bottom: 1px solid green";
            isTrue4 = true;
        } else {
            document.getElementById("password").style.cssText = "border-bottom: 1px solid rgba(255, 0, 0, 0.5)";
            isTrue4 = false;
        }
        submit()
    })
    passwordConfirm.addEventListener("keyup", function(){
        if (passwordConfirm.value == password.value) {
            document.getElementById("password-confirm").style.cssText = "border-bottom: 1px solid green";
            isTrue5 = true;
        } else {
            document.getElementById("password-confirm").style.cssText = "border-bottom: 1px solid rgba(255, 0, 0, 0.5)";
            isTrue5 = false;
        }
        submit()
    })

    robot.addEventListener("change",function() {
        if (robot.checked == true) {
            isTrue6 = true
        } else {
            isTrue6 = false
        }
        submit()
    })

})

function submit() {
    if (isTrue1 == true && isTrue2 == true && isTrue3 == true && isTrue4 == true && isTrue5 == true && isTrue6 == true) {
        button.disabled = false
        button.style.cssText = "background-color: #0071f0; cursor: pointer;";
    } else {
        button.style.cssText = "background-color: rgba(0, 113, 240, 0.7); cursor: default;";
        button.disabled = true
    }
}