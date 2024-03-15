function account_signup(event) {
    const studentId = document.getElementById("student-id").value;
    const password = document.getElementById("password").value;

    fetch("https://k8s-default-sesacalb-3d8710ab4e-27414001.ap-northeast-2.elb.amazonaws.com/accounts/signup/", {
    // fetch("https://api.sugangwhatever.shop:8000/accounts/signup/", {
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
    fetch("https://k8s-default-sesacalb-3d8710ab4e-27414001.ap-northeast-2.elb.amazonaws.com/accounts/signin/", {
    // fetch("https://api.sugangwhatever.shop:8000/accounts/signin/", {
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
                // TODO 로그인 실패 코드 재정비, 모달 띄우기
                window.location.href = "lecture_list.html?student_id=" + studentId;
            } else if (data.status === 104) {
                console.log("로그인 실패 - 비밀번호를 다시 입력해주세요.",);
            } else {
                console.log("로그인 실패 - 해당 학번의 사용자가 존재하지 않습니다.")
            }

        })
        .catch(error => {
            console.error("로그인 오류:", data);
        });
}
