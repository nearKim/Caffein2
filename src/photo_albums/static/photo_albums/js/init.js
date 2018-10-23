$(document).ready(function () {
    // 모달의 버튼을 누르면 파일선택창을 열어준다
    $(".js-upload-photos").click(function () {
        $("#input-photo-upload").click();
    });

    // 파일이 선택되면 AJAX를 사용하여 순차적으로 업로드한다.
    $("#input-photo-upload").fileupload({
        dataType: 'html',
        sequentialUploads: true,
        start: function (e) {
            $('#loader').show()
        },
        stop: function (e) {
            $('#loader').hide()
        },
        done: function (e, data) {
            // 업로드된 파일들은 각각 html 컨테이너안에 담겨 전달된다. 모달 내부에 각 html을 append한다.
            $('#modal-photo-create-container').append(data.result)
        }
    });

    // 모달에서 저장하지 않고 닫았을 경우 업로드된 사진들을 모두 삭제한다.
    $(".close").click(function () {
        // 항상 묻는 레비.
        confirm('정말 닫으시겠습니까? 데이터가 모두 손실됩니다.')

        let pks = []
        // 업로드된 사진의 PK를 모두 얻는다. 사진들의 pk는 input의 id에 담겨있다.
        $("input[name*='photo-desc']").each(function () {
            pks.push($(this).attr('id'))
        })
        // batch delete로 넘겨준다. 하나씩 deleteview를 호출하는 것 보다 효율적이겠지.
        $.ajax({
            url: $('.close').attr('delete-url'),
            method: 'post',
            data: {
                'dangling-photos-pks': pks
            },
            success: (data) => {
                console.log("success!")
                console.log(data)
            },
            fail: (data) => {
                console.log("fail")
            }
        })
    })
})