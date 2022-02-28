var folder_API = "/folder/"
var phrase_API = "/phrase/"

function updateSelected (id) {
  var items = document.querySelectorAll('[role="treeitem"]');
  for (var i = 0; i < items.length; i++) {
    items[i].style.color = "";
    items[i].setAttribute('selected','no');
  }
  selected = document.getElementById(id);
  selected.setAttribute('selected','yes');
}

function send2API (endpoint, method, data) {
  var xhr = new XMLHttpRequest();
  xhr.open(method, endpoint, false);
  if (data) {xhr.setRequestHeader('Content-Type', 'application/json');};
  xhr.send(data);
  if (xhr.readyState === 4) {
    return xhr.response;
  }
}
function resetFolderDropdown (json_data) {
  var folderDropdown1 = document.getElementById('pfolder');
  var folderDropdown2 = document.getElementById('New_Folder_Dialog-pfolder');
  folders = JSON.parse(send2API(folder_API, "GET"));
  folderDropdown1.innerHTML = folders['folders'];
  folderDropdown2.innerHTML = folders['folders'];
}
function resetPhraseList () {
  var phraseList = document.getElementById('Phrase_List');
  phrase_list = JSON.parse(send2API(phrase_API, "GET"));
  phraseList.innerHTML = phrase_list['phrase_list'];
  var trees = document.querySelectorAll('[role="tree"]');

  // Re-initiate the Tree functionality
  for (var i = 0; i < trees.length; i++) {
    var t = new Tree(trees[i]);
    t.init();
  }
}

// On Load setup
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
    new_folder_dialog_folder_name.value = ""
    modal.style.display = "block";
    new_folder_dialog.style.display = "block";

  }
  new_folder_dialog_close_button.onclick = function() {
    modal.style.display = "none";
    new_folder_dialog.style.display = "none";
  }
  new_folder_dialog_ok_button.onclick = function() {
    modal.style.display = "none";
    remove_dialog.style.display = "none";
    data = JSON.stringify({
      name: new_folder_dialog_folder_name.value,
      parent_folder_id: new_folder_dialog_parent_folder.value
    })
    send2API(folder_API, "POST", data);
    resetFolderDropdown();
    resetPhraseList();
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
  remove_dialog_no_button.onclick = function() {
    modal.style.display = "none";
    remove_dialog.style.display = "none";
  }
  remove_dialog_yes_button.onclick = function() {
    modal.style.display = "none";
    remove_dialog.style.display = "none";
    // TODO: Add code to send to API
    // JSON.stringify({
    //   id: stuff,
    //   name:
    // })
  }

});
