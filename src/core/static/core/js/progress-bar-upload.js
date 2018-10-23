$(function () {

  $(".js-upload-photos").click(function () {
    $("#fileupload").click();
  });

  $("#fileupload").fileupload({
    dataType: 'json',
    sequentialUploads: true,

    start: function (e) {
      $("#modal-progress").modal("show");
    },

    stop: function (e) {
      $("#modal-progress").modal("hide");
    },

    progressall: function (e, data) {
      var progress = parseInt(data.loaded / data.total * 100, 10);
      var strProgress = progress + "%";
      $(".progress-bar").css({"width": strProgress});
      $(".progress-bar").text(strProgress);
    },

    done: function (e, data) {
      if (data.result.is_valid) {
        $("#gallery tbody").prepend(
          "<tr><td><a href=\"" + data.result.absolute_url + "\"><img src=\"" + data.result.thumb_url + "\" alt=\"thumbnail\" style=\"border: 1px solid #ccc; margin: 20px;\"></a><a href='" + data.result.url + "'>" + data.result.name + "</a><a class=\"btn btn-danger\" style=\"float: right;\" href=\"/photo_albums/delete-photo/"+ data.result.id + "\">삭제</a></td></tr>"
        )
      }
    }

  });

});
