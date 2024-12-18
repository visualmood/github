// 本js文件用于实现登录页面的功能，包括密码的隐藏显示、密码的验证、登录按钮的禁用和启用。
// 可以学习一些简单的js代码，比如事件监听、DOM操作等。做一些简单的动态效果。

// 实时检查用户名是否存在，并显示相应的提示信息。
const usernameInput = document.getElementById('username');  // 获取用户名输入框，id为username，getElementById()方法
usernameInput.addEventListener('keyup', (e) => {            // 监听keyup事件，实时验证用户名是否存在
    e.target.classList.remove('is-invalid');                // 移除之前的错误提示信息  classList.remove()方法
    e.target.nextElementSibling.innerText = '';             // 移除之前的错误提示信息    nextElementSibling是当前元素的下一个兄弟元素，innerText是获取或设置元素的文本内容         

    const username = e.target.value;                        // 获取输入框的值
    fetch('/authentication/verify-loginuser',{                              // 发送ajax请求,fetch方法向url发送请求  
                                 
        method: 'POST',body: JSON.stringify({username: username})            // 请求方法为POST，请求体为JSON格式的数据
    }).then(response => response.json()).then(data => {                      // 通过response.json()方法获取服务器返回的json数据

        if (data.status=='error'){                                           // 如果服务器返回的status为error，说明用户名不合法，显示错误信息
            e.target.classList.add('is-invalid');                            // 添加is-invalid类，表示输入框输入有误 
            e.target.nextElementSibling.innerText = data.msg;                // 显示错误信息
        }if (data.status=='success'){                                        // 如果服务器返回的status为success，说明用户名合法，显示成功信息
            e.target.classList.remove('is-invalid');                         // 移除is-invalid类，表示输入框输入正确
            e.target.nextElementSibling.innerText = data.msg;                // 显示成功信息
        }
    })

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


// 密码的验证，这个js代码是从网上找的，原作者是刘旭教授，我只是稍微修改了一下。
const verifyImg = document.getElementById('verify-img')
verifyImg.addEventListener('click', getVerifyCode)
function getVerifyCode() {
    fetch('/authentication/get-logincode')
        .then(response => response.arrayBuffer())
        .then(arrayBuffer => {
            console.log(arrayBuffer)
            const base64String = window.btoa(String.fromCharCode(...new Uint8Array(arrayBuffer)))
            // 更新img标签的src属性值，以显示图像
            verifyImg.src = "data:image/gif;base64, " + base64String;
        });
}
getVerifyCode();





