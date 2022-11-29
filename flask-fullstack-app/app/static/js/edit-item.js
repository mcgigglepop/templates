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


    
// Start Custom Dropdown
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
            populatePreview(dd.parent().attr('id'), txt);
            opt.removeClass("active");
            $(this).addClass("active");
            btn.text(txt);
        });
}

function populatePreview(type, txt){
    if(type == "item_collection"){
        var split = txt.split("(");
        $("#preview-collection").text(split[0]);
        if(split[1] == "Private)"){
            $("#preview-type").text('('+split[1]);
        }
        else{
            $("#preview-type").text("(public)");
        }
        
    }else{
        
        $("#preview-category").text(txt);
    }
}