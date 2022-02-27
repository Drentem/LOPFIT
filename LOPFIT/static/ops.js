window.addEventListener('load', function () {
  var modal = document.getElementById('ModalConatiner');
  var new_folder_dialog = document.getElementById('New_Folder_Dialog');
  var modal_header = document.getElementById('modal-header');
  var modal_content = document.getElementById('modal-content');
  var new_folder_dialog_close_button = document.getElementById('New_Folder_Dialog-close');

  new_folder_dialog_close_button.onclick = function() {
    modal.style.display = "none";
  }
  // New Phrase Handler
  var new_phrase = document.getElementById('New_Phrase').onclick = function() {
    modal_header.innerHTML = "New Phrase";

    modal_content.innerHTML = "New Phrase Clicked";


    modal.style.display = "block";
  }
  // New Folder Handler
  var new_folder = document.getElementById('New_Folder').onclick = function() {

    modal.style.display = "block";
  }
  // Object Deletion Handler
  var remove = document.getElementById('Remove').onclick = function() {
    alert("Clicked Remove!")
  }
});
