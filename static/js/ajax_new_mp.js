
  $(document).ready(function(){

      //работа со всплывающим окном
          //открыть и получить текст о событии
      var myModal = new bootstrap.Modal(document.getElementById('new_modal'));
      media_url='/static/media/'
      $('.list-group-item').click(function() {
                                            let subj_id=$(this).attr('id');
                                            let title=$(this).find('b').text()
                                            $('.modal-title').html(title);
                                            $.getJSON('/ajaxnewinfo',{id:subj_id}, function(data) {
                                                                                        $('.exponate_text').html(data['desc']);
                                                                                        ArrayPhoto=$(data['photo_urls']);
                                                                                        photo_num=0;
                                                                                        $('.modal-body').find('iframe').attr('src',data['video']);
                                                                                        $('.modal-body').find('img').attr('src',media_url+ArrayPhoto[0]);

                                                                                        });


                                            myModal.show()
                                                                });

      $('.close_exh').click(function () {
        myModal.hide()
                            });

      $('#next_photo').click(function(){

        if (  photo_num<ArrayPhoto.length-1) {
          photo_num+=1;
          new_url=ArrayPhoto[photo_num];
          let image=$('.modal-body').find('img');
          image.fadeOut(600,()=>image.attr('src',media_url+new_url));
          image.fadeIn(600);

          };
        });

        $('#prev_photo').click(function(){

          if (  photo_num>=1) {
            photo_num-=1;
            new_url=ArrayPhoto[photo_num];
            let image=$('.modal-body').find('img');
            image.fadeOut(600,()=>image.attr('src',media_url+new_url));
            image.fadeIn(600);

          };
        });



  });
