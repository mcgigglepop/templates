$(document).ready(function(){
    // custom drop-downs
    dropdown('#item_collection');
    dropdown('#item_category');

    function dropdown(e){
        var obj = $(e+'.dropdown');
        var btn = obj.find('.btn-selector');
        var dd = obj.find('ul');
        var opt = dd.find('li');
        
        obj.on("mouseenter", function() {
            dd.show();
            $(this).css("z-index",1000);
        }).on("mouseleave", function() {
            dd.hide();
            $(this).css("z-index","auto")
        })
        

        opt.on('touchend', function(){
            dd.hide();
            var txt = $(this).text();
            if(dd.parent().attr('id') == "item_collection"){
                document.getElementById("collection").value= txt;
            }
            if(dd.parent().attr('id') == "item_category"){
                document.getElementById("category").value= txt;
            }
            opt.removeClass("active");
            $(this).addClass("active");
            btn.text(txt);
        });

        opt.on("click", function() {
            dd.hide();
            var txt = $(this).text();
            if(dd.parent().attr('id') == "item_collection"){
                document.getElementById("collection").value= txt;
            }
            if(dd.parent().attr('id') == "item_category"){
                document.getElementById("category").value= txt;
            }
            opt.removeClass("active");
            $(this).addClass("active");
            btn.text(txt);
        });
    }
    // end custom drop-downs

    // start custom image picker
    var cdl = [];
    var cdo = {};

    // init the upload
    ImgUpload();

    var addItem = function() {
        var $input = $('#field_value').val();
        var $txt = $('#field_value_input').val();
        if ($input) {
            $('#custom-fields').append('<h5>'+$input+' <a class="field-delete"><i class="fa fa-trash"></i></a></h5><input type="text" name="item_title" id="item_title" value="'+$txt+'" class="form-control" placeholder="e.g. Crypto Funk" readonly><div class="spacer-20"></div>');
        };
        $('#field_value').val("");
        $('#field_value_input').val("");
    };

    $('#add-field').on('click', function(event){
        addItem();
        populateObj();
    });

    $('#custom-fields').on('click', '.field-delete', function(){
        $(this).parent().fadeOut(300, function(){
            $(this).next().remove();
            $(this).next().remove();
            $(this).remove();  
            populateObj();
        });
    });

    $("#item_title").keyup(function(){
        var currentText = $(this).val();
        
        $("#preview-title").text(currentText);
    });

    function populateObj(){
        var customArray = [];
        var customDict = {};
        $("#custom-fields :input, #custom-fields h5").each(function(e){	
            if (this.tagName === 'H5'){
                customDict['key'] = this.textContent;
            }
            if (this.tagName === 'INPUT'){
                customDict['value'] = this.value;
                customArray.push(customDict);   
                customDict = {};
            } 
        }); 
        hc = JSON.stringify(customArray);
        document.getElementById("hc").value = hc;
    }

    function ImgUpload() {
        var imgWrap = "";
        var imgArray = [];
        var secondArr = [];
        var innerObj = {};

        $('.upload__inputfile').each(function () {
            $(this).on('change', function (e) {
            imgWrap = $(this).closest('.upload__box').find('.upload__img-wrap');
            var maxLength = 1;

            var files = e.target.files;
            var filesArr = Array.prototype.slice.call(files);
            var iterator = 0;
            filesArr.forEach(function (f, index) {

                if (!f.type.match('image.*')) {
                return;
                }

                if (imgArray.length > maxLength) {
                return false
                } else {
                var len = 0;
                for (var i = 0; i < imgArray.length; i++) {
                    if (imgArray[i] !== undefined) {
                    len++;
                    }
                }
                if (len > maxLength) {
                    return false;
                } else {
                    imgArray.push(f);
                    
                    var reader = new FileReader();
                    reader.onload = function (e) {
                    innerObj.name = f.name;
                    innerObj.val = e.target.result;
                    secondArr.push(innerObj);
                    innerObj = {};
                    var html = "<div class='upload__img-box'><div style='background-image: url(" + e.target.result + ")' data-number='" + $(".upload__img-close").length + "' data-file='" + f.name + "' class='img-bg'><div class='upload__img-close'><input type='hidden' id='img-"+f.name+"' name='img-"+f.name+"'></div></div></div>";
                    imgWrap.append(html);
                    document.getElementById('img-'+f.name).value= e.target.result;
                    if(secondArr.length == 1){
                        document.getElementById('img-preview').children[0].remove();
                        var pop = '<h5>Preview item</h5><div class="nft__item style-2"><div class="nft__item_wrap"><a href="#"><img src="'+e.target.result+'" id="" class="lazy nft__item_preview" alt=""></a></div><div class="nft__item_info"><a href="#"><h4>Collectible Name</h4></a><span></span></div></div>';
                        document.getElementById('img-preview').innerHTML = pop;
                    }
                    
                    iterator++;
                    }
                    reader.readAsDataURL(f);
                }
                }
            });
            });
        });

        $('body').on('click', ".upload__img-close", function (e) {
            var file = $(this).parent().data("file");
            for (var i = 0; i < imgArray.length; i++) {
            if (imgArray[i].name === file) {
                imgArray.splice(i, 1);
                break;
            }
            }
            for (var i = 0; i < secondArr.length; i++) {
            if (secondArr[i].name === file) {
                secondArr.splice(i, 1);
                break;
            }
            }
            $(this).parent().parent().remove();
            document.getElementById('upload_file').value= null;
            document.getElementById('file_name').innerHTML= 'PNG, JPG, GIF, WEBP or MP4. Max 200mb.';
            document.getElementById('img-preview').children[0].remove();
            var p2 = '';
            if(secondArr.length>0){
                document.getElementById('img-preview').children[0].remove();
                p2 = '<h5>Preview item</h5><div class="nft__item style-2"><div class="nft__item_wrap"><a href="#"><img src="'+secondArr[0].val+'" id="" class="lazy nft__item_preview" alt=""></a></div><div class="nft__item_info"><a href="#"><h4>Collectible Name</h4></a><span></span></div></div>';
            }else{
                p2 = '<h5>Preview item</h5><div class="nft__item style-2"><div class="nft__item_wrap"><a href="#"><img src="../static/images/no-img.jpg" id="" class="lazy nft__item_preview" alt=""></a></div><div class="nft__item_info"><a href="#"><h4>Collectible Name</h4></a><span></span></div></div>';
            }
            document.getElementById('img-preview').innerHTML = p2;
        });
        }



});