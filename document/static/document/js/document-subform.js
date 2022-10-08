// documents subform functions
/* global $ */

$(function(){
    "use strict";
    // console.log("yo");
    $('.document-row .document-delete-button').click(function(event) {
        // console.log('click delete');
        var row_idx=$(this).data('document-index');
        // console.log('  on row', row_idx, $(event.target), this);
        $('.document-row .document-row-overlay.to-delete-index-'+row_idx).removeClass("hidden");
        $('.document-row .document-undelete-button.to-delete-index-'+row_idx).removeClass("hidden");
        $('.document-row .document-delete-button.to-delete-index-'+row_idx).addClass("hidden");
        $('.document-row input.to-delete-index-'+row_idx).val(true);
    }).css('cursor', 'pointer');
    $('.document-row .document-undelete-button').click(function(event) {
        // console.log('click delete');
        var row_idx=$(this).data('document-index');
        // console.log('  on row', row_idx, $(event.target), this);
        $('.document-row .document-row-overlay.to-delete-index-'+row_idx).addClass("hidden");
        $('.document-row .document-delete-button.to-delete-index-'+row_idx).removeClass("hidden");
        $('.document-row .document-undelete-button.to-delete-index-'+row_idx).addClass("hidden");
        $('.document-row input.to-delete-index-'+row_idx).val('');
    }).css('cursor', 'pointer');

    $('.document-row').on('dragenter', function(event){
      //console.log("dragenter", this, event.target);
      this.classList.add('dragged-over');
      event.preventDefault();
    });

    $('.document-row').on('dragleave', function(event){
      //console.log("dragleave", this, event.target);
      this.classList.remove('dragged-over');
      //event.preventDefault();
    });

    $('.document-row').on('dragover', function(event){
      //console.log("dragover", this, event.target);
      this.classList.add('dragged-over');
      event.preventDefault();
    });

    $('.document-row').on('drop', function(event){
      console.log("drop", this, event);
      this.classList.remove('dragged-over');

      let ev = event.originalEvent;

      if (ev.dataTransfer.items) {
        // Use DataTransferItemList interface to access the file(s)
        for (let i = 0; i < ev.dataTransfer.items.length; i++) {
          // If dropped items aren't files, reject them
          if (ev.dataTransfer.items[i].kind === 'file') {
            var file = ev.dataTransfer.items[i].getAsFile();
            // console.log('... file[' + i + '].name = ' + file.name);
          }
        }
      } else {
        // Use DataTransfer interface to access the file(s)
        for (let i = 0; i < ev.dataTransfer.files.length; i++) {
          // console.log('... file[' + i + '].name = ' + ev.dataTransfer.files[i].name);
        }
      }
      event.preventDefault();
    });
});

function dropHandler(ev) {
    "use strict";
  // console.log('File(s) dropped');

  // Prevent default behavior (Prevent file from being opened)
  ev.preventDefault();

  if (ev.dataTransfer.items) {
    // Use DataTransferItemList interface to access the file(s)
    for (var i = 0; i < ev.dataTransfer.items.length; i++) {
      // If dropped items aren't files, reject them
      if (ev.dataTransfer.items[i].kind === 'file') {
        var file = ev.dataTransfer.items[i].getAsFile();
        console.log('... file[' + i + '].name = ' + file.name);
      }
    }
  } else {
    // Use DataTransfer interface to access the file(s)
    for (let i = 0; i < ev.dataTransfer.files.length; i++) {
      // console.log('... file[' + i + '].name = ' + ev.dataTransfer.files[i].name);
    }
  }
}

function dragOverHandler(ev) {
    "use strict";
  // console.log('File(s) in drop zone', this, ev);

  //this.addClass('file-over')

  // Prevent default behavior (Prevent file from being opened)
  ev.preventDefault();
}

// end of documents subform functions
