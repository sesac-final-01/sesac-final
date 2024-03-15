// URL에서 쿼리 매개변수를 추출
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const studentId = urlParams.get('student_id');


// fetch(`https://k8s-default-sesacalb-3d8710ab4e-27414001.ap-northeast-2.elb.amazonaws.com/lectures/my-lectures?student_id=${studentId}`)
fetch(`https://api.sugangwhatever.shop:8000/lectures/my-lectures?student_id=${studentId}`)
    .then(response => response.json())
    .then(data => {
        console.log('학생 정보:', data.student);
        console.log('서버에서 받은 강의 목록:', data.my_lectures);

        document.getElementById("student-id").textContent = data.student.student_id;
        document.getElementById("student-name").textContent = data.student.student_name;
        document.getElementById("student_grade").textContent = data.student.student_grade;
        document.getElementById("major").textContent = data.student.major;
        document.getElementById("max_credit").textContent = data.student.max_credit;
        document.getElementById("applied_credit").textContent = data.student.applied_credit;

        displayMyLectures(data.my_lectures);
    })
    .catch(error => {
        console.error('서버에서 강의 목록을 불러오는 중 오류 발생:', error);
    })


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

// 각각의 Response에 대한 팝업을 띄우는 함수
function handleResponse(response) {
    displayPopup(response);
}

function cancelLecture(event) {
    // 클릭된 버튼의 부모 노드(tr 요소)를 찾습니다.
    const row = event.target.closest('tr');
    // const studentId = document.getElementById('student-id').textContent;
    const lectureCode = row.querySelector('td:first-child').textContent;
    const lectureName = row.querySelector('td:nth-child(2)').textContent;
    // const url = `https://k8s-default-sesacalb-3d8710ab4e-27414001.ap-northeast-2.elb.amazonaws.com/lectures/cancel/`;
    const url = `https://api.sugangwhatever.shop:8000/lectures/cancel/`;

    console.log("cancelLecture")

    fetch(url, {
        method: 'PUT',
        body: JSON.stringify({}), // 요청 바디는 비어있을 수 있습니다.
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            student_id: studentId,
            lec_id: lectureCode
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log('data:', data.my_lectures)
            document.getElementById("applied_credit").textContent = data.applied_credit;
            displayMyLectures(data.my_lectures)
            handleResponse(`${lectureName} 수강이 취소되었습니다.`); // Response를 처리하는 함수 호출
        })
        .catch(error => {
            console.error('신청 중 오류 발생:', error);
            handleResponse("취소 중 오류가 발생했습니다. 다시 시도해주세요.");
        });
}

function addClickEventToButtons() {
    const buttons = document.querySelectorAll('.delete-button');
    buttons.forEach(button => {
        button.addEventListener('click', cancelLecture);
    });
}


function displayMyLectures(lectures) {
    document.getElementById('my-lecture-list').innerHTML = '';

    const myLectureList = document.getElementById('my-lecture-list');

    lectures.forEach(lecture => {
        console.log('강의정보:', lecture);

        const row = document.createElement('tr');

        const lec_code_cell = document.createElement('td');
        lec_code_cell.textContent = lecture.lec_id;

        const lec_name_cell = document.createElement('td');
        lec_name_cell.textContent = lecture.lec_name;

        const professor_name_cell = document.createElement('td');
        professor_name_cell.textContent = lecture.professor_name;

        const major_cell = document.createElement('td');
        major_cell.textContent = lecture.major;

        const lec_room_cell = document.createElement('td');
        lec_room_cell.textContent = lecture.lec_room;

        const lec_quota_cell = document.createElement('td');
        lec_quota_cell.textContent = lecture.lec_quota;

        const credit_cell = document.createElement('td');
        credit_cell.textContent = lecture.credit;

        const lec_schedule_cell = document.createElement('td');
        lec_schedule_cell.textContent = lecture.lec_schedule;

        const delete_button_cell = document.createElement('td'); // 새로운 셀 생성
        const delete_button = document.createElement('button'); // 버튼 생성
        delete_button.textContent = "취소"; // 버튼 텍스트 설정
        delete_button.classList.add('delete-button');
        delete_button_cell.appendChild(delete_button); // 버튼을 셀에 추가

        row.appendChild(lec_code_cell);
        row.appendChild(lec_name_cell);
        row.appendChild(professor_name_cell);
        row.appendChild(major_cell);
        row.appendChild(lec_room_cell);
        row.appendChild(lec_quota_cell);
        row.appendChild(credit_cell);
        row.appendChild(lec_schedule_cell);

        row.appendChild(delete_button_cell); // 셀 추가

        myLectureList.appendChild(row);
    });
    addClickEventToButtons();
}