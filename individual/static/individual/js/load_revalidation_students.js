document.addEventListener("DOMContentLoaded", (event) => {
    $("#id_department").change(function () {
        var url = $("#flex_form").attr("revalidation-students-url");
        var department_name = $(this).val();

        $.ajax({
          url: url,
          data: {
              department: department_name
          },
            success: function (data) {
              $("#id_student").html(data);
            }
        });
    });
});
