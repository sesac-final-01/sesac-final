function displayPopup(message) {
    const modal = document.createElement('div');
    modal.classList.add('modal');

    const messageElement = document.createElement('div');
    messageElement.textContent = message;

    modal.appendChild(messageElement);

    document.body.appendChild(modal);

    const closeButton = document.createElement('button');
    closeButton.textContent = '닫기';
    closeButton.addEventListener('click', () => {
        modal.remove();
    });

    modal.appendChild(closeButton);
}

function handleResponse(response) {
    displayPopup(response);
}

function account_signup(event) {
    const studentId = document.getElementById("student-id").value;
    const password = document.getElementById("password").value;

    fetch("http://127.0.0.1:8000/accounts/signup/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            student_id: studentId,
            password: password
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 201) {
                console.log("회원가입 성공", data.status);
                window.location.href = "signin.html";
            } else {
                console.log("회원가입 실패", data.status);
                document.getElementById("student-id").value = "";
                document.getElementById("password").value = "";
                handleResponse(data.message);
            }

        })
        .catch(error => {
            console.error("회원가입 오류:", data);
        });
}


function account_signin() {
    const studentId = document.getElementById("student-id").value;
    const password = document.getElementById("password").value;

    // 로그인 API에 POST 요청을 보냅니다.
    fetch("http://127.0.0.1:8000/accounts/signin/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            student_id: studentId,
            password: password
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            if (data.status === 200) {
                console.log("로그인 성공");
                window.location.href = "lecture_list.html?student_id=" + studentId;
            } else if(data.status === 406) {
                console.log("로그인 실패 - 비밀번호를 다시 입력해주세요.",);
                handleResponse(data.message)
            } else{
                console.log("로그인 실패 - 해당 학번의 사용자가 존재하지 않습니다.")
                handleResponse(data.message)
            }

        })
        .catch(error => {
            console.error("로그인 오류:", data);
        });
}
