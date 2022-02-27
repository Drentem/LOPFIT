window.addEventListener('load', function () {

  // Modal Dialog
  var modal = document.getElementById('ModalConatiner');

  // New Folder Dialog
  var new_folder_dialog = document.getElementById('New_Folder_Dialog');
  var new_folder_dialog_folder_name = document.getElementById('folder_name');
  var new_folder_dialog_parent_folder = document.getElementById('New_Folder_Dialog-pfolder');
  var new_folder_dialog_close_button = document.getElementById('New_Folder_Dialog-close');
  var new_folder_dialog_ok_button = document.getElementById('New_Folder_Dialog-ok');
  var new_folder_button = document.getElementById('New_Folder').onclick = function() {
    modal.style.display = "block";
    new_folder_dialog.style.display = "block";
  }
  new_folder_dialog_close_button.onclick = function() {
    modal.style.display = "none";
    new_folder_dialog.style.display = "none";
  }
  // New Phrase Handler
  var new_phrase = document.getElementById('New_Phrase').onclick = function() {

  }
  // Object Deletion Handler
  var remove_dialog = document.getElementById('Remove_Dialog');
  var remove_dialog_item = document.getElementById('Item');
  var remove_dialog_close_button = document.getElementById('Remove_Dialog-close');
  var remove_dialog_no_button = document.getElementById('Remove_Dialog-no');
  var remove_dialog_yes_button = document.getElementById('Remove_Dialog-yes');
  var remove_dialog_button = document.getElementById('Remove').onclick = function() {
    modal.style.display = "block";
    remove_dialog.style.display = "block";
  }
  remove_dialog_close_button.onclick = function() {
    modal.style.display = "none";
    remove_dialog.style.display = "none";
  }
});
