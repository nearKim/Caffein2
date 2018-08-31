$(function () {

  $("#fileupload").fileupload({
    dataType: 'json',
    done: function (e, data) {
      if (data.result.is_valid) {
        $("#gallery tbody").prepend(
          "<tr><td><a href=\"" + data.result.absolute_url + "\"><img src=\"" + data.result.thumb_url + "\" alt=\"thumbnail\" style=\"border: 1px solid #ccc; margin: 20px;\"></a><a href='" + data.result.url + "'>" + data.result.name + "</a><a class=\"btn btn-danger\" style=\"float: right;\" href=\" /photo_album/delete-photo/" + data.result.id + "\">delete</a></td></tr>"
        )
      }
    }
  });

});
