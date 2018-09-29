$(document).ready(function () {
    // 댓글창에서 엔터를 누르면 AJAX로 댓글을 생성하고 표시한다.
    $(':input').on('keypress', function (event) {
        // input에서 엔터키를 누른경우
        if (event.which === 13) {
            event.preventDefault()
            // 현재 input의 내용과 내용을 전달해야 하는 form의 url을 가져온다
            let content = $(this).val()
            let url = $(this).closest('form').attr('action')
            // 그 후 input을 비워준다
            $(this).val('')

            $.ajax({
                url: url,
                method: 'POST',
                data: {
                    'content': content
                },
                success: (data) => {
                    // 현재 input으로부터 가장 가까운 section을 찾고 section의 자손중 comment-container 클래스가 있는걸 찾아 내용을 교체한다.
                    $(this).closest('section').find('.comment-container').html(data)
                },
                fail: function (data) {
                    console.log("failed")
                }
            })
        }
    })
})
