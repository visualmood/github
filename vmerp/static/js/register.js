// ajax请求验证用户名 邮件是否存在，实时显示错误信息，const变量名，不能得重名，二次密码框要用二个名字。
// 点击密码及确认密码输入框后面的图标，让密码可见或不可见。实现交互效果
// 本js共四个函数，分别是：
// 1. 监听用户名输入框的keyup事件，实时验证用户名是否存在及输入是否合法
// 2. 监听邮箱输入框的keyup事件，实时验证邮箱是否合法
// 3. 密码的隐藏显示,这个js代码是从网上找的，原作者是刘旭教授，我只是稍微修改了一下。
// 4. 确认密码的隐藏显示,这个js代码是从网上找的，原作者是刘旭教授，我只是稍微修改了一下。
// 供<register.html>|<forgot_password.html>|<reset_password.html>三个页面共同调用，在这三个页面的blockjs块中引用。


// 监听用户名输入框的keyup事件，实时验证用户名是否存在及输入是否合法
const usernameInput = document.getElementById('username');  // 获取用户名输入框，id为username，getElementById()方法
usernameInput.addEventListener('keyup', (e) => {            // 监听keyup事件，实时验证用户名是否存在

    e.target.classList.remove('is-invalid');               // 移除之前的错误提示信息  classList.remove()方法
    e.target.nextElementSibling.innerText = '';           // 移除之前的错误提示信息    nextElementSibling是当前元素的下一个兄弟元素，innerText是获取或设置元素的文本内容         

    const username = e.target.value;                      // 获取输入框的值


    fetch('/authentication/verify-registeruser',{                            // 发送ajax请求,fetch方法向url发送请求  
                                 
        method: 'POST',body: JSON.stringify({username: username})            // 请求方法为POST，请求体为JSON格式的数据
    }).then(response => response.json()).then(data => {                      // 通过response.json()方法获取服务器返回的json数据

        if (data.status=='error'){                                           // 如果服务器返回的status为error，说明用户名已存在，显示错误信息
            e.target.classList.add('is-invalid');                            // 添加is-invalid类，表示输入框输入有误 
            e.target.nextElementSibling.innerText = data.msg;                // 显示错误信息
        }
    })
});




// 监听邮箱输入框的keyup事件，实时验证邮箱是否合法
const emailInput = document.getElementById('email');            // 获取邮箱输入框，id为email 
emailInput.addEventListener('keyup', (e) => {                   // 监听keyup事件，实时验证用户名是否存在

    e.target.classList.remove('is-invalid');                    // 移除之前的错误提示信息  classList.remove()方法
    e.target.nextElementSibling.innerText = '';                 // 移除之前的错误提示信息    nextElementSibling是当前元素的下一个兄弟元素，innerText是获取或设置元素的文本内容         

    const email = e.target.value;                               // 获取输入框的值

    fetch('/authentication/verify-registeremail',{                       // 发送ajax请求,fetch方法向url发送请求  
                                 
        method: 'POST',body: JSON.stringify({email: email})              // 请求方法为POST，请求体为JSON格式的数据
    }).then(response => response.json()).then(data => {                  // 通过response.json()方法获取服务器返回的json数据

        if (data.status=='error'){                                       // 如果服务器返回的status为error，说明用户名已存在，显示错误信息，status msg 等变量是在views.py中视图函数中定义的
            e.target.classList.add('is-invalid');                        // 添加is-invalid类，表示输入框输入有误 
            e.target.nextElementSibling.innerText = data.msg;            // 显示错误信息
        }
    })
});


// 监听密码输入框的keyup事件，实时验证密码是否合法
const passwordInput = document.getElementById('password');      // 获取密码输入框，id为password
passwordInput.addEventListener('keyup', (e) => {               // 监听keyup事件，实时验证密码是否合法   

    e.target.classList.remove('is-invalid');                    // 移除之前的错误提示信息  classList.remove()方法
    e.target.nextElementSibling.innerText = '';                 // 移除之前的错误提示信息    nextElementSibling是当前元素的下一个兄弟元素，innerText是获取或设置元素的文本内容         

    const password = e.target.value;                            // 获取输入框的值

    fetch('/authentication/verify-registerpwd',{                        // 发送ajax请求,fetch方法向url发送请求  ) 
                                 
        method: 'POST',body: JSON.stringify({password: password})        // 请求方法为POST，请求体为JSON格式的数据
    }).then(response => response.json()).then(data => {                  // 通过response.json()方法获取服务器返回的json数据

        if (data.status=='error'){                                       // 如果服务器返回的status为error，说明用户名已存在，显示错误信息
            e.target.classList.add('is-invalid');                        // 添加is-invalid类，表示输入框输入有误 
            e.target.nextElementSibling.innerText = data.msg;            // 显示错误信息
        }
    })
});

// 监听确认密码输入框的keyup事件，实时验证确认密码是否合法
const confirmPasswordInput = document.getElementById('confirm_password');      // 获取确认密码输入框，id为confirm_password
confirmPasswordInput.addEventListener('keyup', (e) => {               // 监听keyup事件，实时验证确认密码是否合法   

    e.target.classList.remove('is-invalid');                    // 移除之前的错误提示信息  classList.remove()方法
    e.target.nextElementSibling.innerText = '';                 // 移除之前的错误提示信息    nextElementSibling是当前元素的下一个兄弟元素，innerText是获取或设置元素的文本内容 
    
    const confirmPassword = e.target.value;                     // 获取输入框的值

    if (confirmPassword !== passwordInput.value){               // 如果确认密码和密码不一致，显示错误信息
        e.target.classList.add('is-invalid');                    // 添加is-invalid类，表示输入框输入有误 
        e.target.nextElementSibling.innerText = '两次密码输入不一致';  // 显示错误信息
    }
});





// 密码的隐藏显示,这个js代码是从网上找的，原作者是刘旭教授，我只是稍微修改了一下。
const eyeIcon = document.getElementById("hide-password");       // 获取眼睛图标元素  --------getElementById() 方法通过元素的 id 属性值获取元素
const pwdInput = document.getElementById("password");           // 获取密码输入框
eyeIcon.addEventListener("click", (e) => {                      // 点击眼睛图标时执行函数, --addEventListener() 方法为元素添加事件监听器  (e) => {} 是一个箭头函数，用来处理事件
    let type = pwdInput.getAttribute("type")                    //   获取密码输入框的type属性   -------- getAttribute() 方法获取元素的属性值

    if (type === "password") {                                  //   如果type属性为password，则将type属性改为text
        pwdInput.setAttribute("type", "text")                   //   将密码输入框的type属性改为text，使密码可见  --------setAttribute() 方法设置或修改元素的属性
        eyeIcon.setAttribute('src', '/static/img/eye-off.svg')  //   将眼睛图标改为关闭状态 将eyeIcon 的src属性改为'/static/img/eye-off.svg'  

    } else {                                                    //   如果type属性为text，则将type属性改为password  使密码用*号占位，不可见
        pwdInput.setAttribute("type", "password")               //   将密码输入框的type属性改为password
        eyeIcon.setAttribute('src', '/static/img/eye.svg')      //   将眼睛图标改为打开状态, 将eyeIcon 的src属性改为'/static/img/eye.svg'
    }
});



// 确认密码的隐藏显示,这个js代码是从网上找的，原作者是刘旭教授，我只是稍微修改了一下。
const eyeIcon2 = document.getElementById("hide-password2");               // 获取眼睛图标元素  --------getElementById() 方法通过元素的 id 属性值获取元素
const pwdInput2 = document.getElementById("confirm_password");           // 获取确认密码输入框
eyeIcon2.addEventListener("click", (e) => {                      // 点击眼睛图标时执行函数, --addEventListener() 方法为元素添加事件监听器  (e) => {} 是一个箭头函数，用来处理事件
    let type = pwdInput2.getAttribute("type")                    //   获取密码输入框的type属性   -------- getAttribute() 方法获取元素的属性值

    if (type === "password") {                                  //   如果type属性为password，则将type属性改为text
        pwdInput2.setAttribute("type", "text")                   //   将密码输入框的type属性改为text，使密码可见  --------setAttribute() 方法设置或修改元素的属性
        eyeIcon2 .setAttribute('src', '/static/img/eye-off.svg')  //   将眼睛图标改为关闭状态 将eyeIcon 的src属性改为'/static/img/eye-off.svg'  

    } else {                                                    //   如果type属性为text，则将type属性改为password  使密码用*号占位，不可见
        pwdInput2.setAttribute("type", "password")               //   将密码输入框的type属性改为password
        eyeIcon2.setAttribute('src', '/static/img/eye.svg')      //   将眼睛图标改为打开状态, 将eyeIcon 的src属性改为'/static/img/eye.svg'
    }
});




// 验证码刷新，调用getVerifyCode()函数，fetch()方法向/authentication/get-registercode发送请求，来获取验证码图片，并在session中保存字符串，在img标签的src属性值中显示图像。
const verifyImg = document.getElementById('verify-image')
verifyImg.addEventListener('click', getVerifyCode)
function getVerifyCode() {
    fetch('/authentication/get-registercode')
        .then(response => response.arrayBuffer())
        .then(arrayBuffer => {
            console.log(arrayBuffer)
            const base64String = window.btoa(String.fromCharCode(...new Uint8Array(arrayBuffer)))
            // 更新img标签的src属性值，以显示图像
            verifyImg.src = "data:image/gif;base64, " + base64String;
        });
}
getVerifyCode();

