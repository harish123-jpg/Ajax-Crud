<script type="text/javascript">
  const csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value
  var update_id;
    function edit(id){
        let name = $(`#row-${id} .student_name`).text();
        let lastname = $(`#row-${id} .student_lastname`).text();
        let phone = $(`#row-${id} .student_phone`).text();
        let email = $(`#row-${id} .student_email`).text();

        $('#id_name').val(name);
        $('#id_lastname').val(lastname);
        $('#id_phone').val(phone);
        $('#id_email').val(email);
        update_id = id;

    }
    function saveStudent() {
        var data = {
                    name: $('#id_name')[0].value,
                    lastname: $('#id_lastname')[0].value,
                    phone: $('#id_phone')[0].value,
                    email: $('#id_email')[0].value,
                    'csrfmiddlewaretoken': csrf_token,
                    'update': update_id
             };
        $.ajax({
            url: '{% url 'home' %}',
            type: 'POST',
            data: data,
            datatype: 'json',
            success: function(response){
            if (update_id){
                $(`#row-${update_id}`).html(response)
                console.log(response)
            }
            else{
                $('tbody').append(response);
                console.log(response)
            }
            update_id = null;
            $('#id_name').val('');
            $('#id_lastname').val('');
            $('#id_phone').val('');
            $('#id_email').val('');
             }
    });
}
  function deleteStudent(id){
    var data ={
                'csrfmiddlewaretoken': csrf_token , 'id':id}
        $.ajax({
            url: 'delete/'+id,
            type: 'POST',
            data: data,
            datatype: 'json',
            success: function(response){
            console.log(response)
            $("#row-"+response.id).remove();
            }
        });
   }

        var PAGE = 1;
    function searchButton(){
    console.log('alskjda')
    PAGE = 1;
    let query = document.getElementById("query").value;
    $.ajax({
        url: `{% url 'home' %}?page=${PAGE}&query=${query}`,
        success: function (response){
             $("tbody").html(response["html"]);
                if (!response["has_next"]){
                        $("#loadmoreBtn").remove();
               }
        }
    })
  }

  $(document).ready(function(){
      $("#loadmoreBtn").on('click',function(){
      PAGE += 1;
       var _currentResult=$(".post-box").length;
        let query = document.getElementById("query").value;
    $.ajax({
        url: `{% url 'home' %}?page=${PAGE}&query=${query}`,
            success:function(response){
                $("tbody").append(response["html"]);
                if (!response["has_next"]){
                        $("#loadmoreBtn").remove();
               }
            }
        });
     });
  });
</script>
<script src="https://code.jquery.com/jquery-3.6.1.js"
        integrity="sha256-3zlB5s2uwoUzrXK3BT7AX3FyvojsraNFxCc2vC/7pNI=" crossorigin="anonymous"></script>
<script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js'></script>
<script src='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js'></script>