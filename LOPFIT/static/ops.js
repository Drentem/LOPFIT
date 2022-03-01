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
  phraseList.innerHTML = "";
  phraseList.innerHTML = phrase_list['phrase_list'];

  // set Remove button status
  var remove_dialog_button = document.getElementById('Remove');
  if (document.querySelectorAll('[role="treeitem"]').length >0){
    remove_dialog_button.disabled = false;
    remove_dialog_button.classList.remove("disabled")
  } else {
    remove_dialog_button.disabled = true;
    remove_dialog_button.classList.add("disabled")
  }

  // Re-initiate the Tree functionality
  var trees = document.querySelectorAll('[role="tree"]');
  for (var i = 0; i < trees.length; i++) {
    var t = new Tree(trees[i]);
    t.init();
  }

  var treeitems = document.querySelectorAll('[role="treeitem"]');
  for (var i = 0; i < treeitems.length; i++) {
    treeitems[i].addEventListener('click', function (event) {
      var treeitem = event.currentTarget;
      var label = treeitem.getAttribute('aria-label');
      if (!label) {
        var child = treeitem.firstElementChild;
        label = child ? child.innerText : treeitem.innerText;
      }
      updateSelected(treeitem.id);
      event.stopPropagation();
      event.preventDefault();
    });
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
    new_folder_dialog_folder_name.value = "";
    new_folder_dialog_parent_folder.value = 0;
  }

  // New Phrase Handler
  var new_phrase = document.getElementById('New_Phrase').onclick = function() {

  }

  // Object Deletion Handler
  var remove_dialog = document.getElementById('Remove_Dialog');
  var remove_dialog_header = document.getElementById('Remove_Dialog-header');
  var remove_dialog_type = document.getElementById('Remove_Dialog-type');
  var remove_dialog_item = document.getElementById('Remove_Dialog-item');
  var remove_dialog_warning = document.getElementById('Remove_Dialog-warning');
  var remove_dialog_close_button = document.getElementById('Remove_Dialog-close');
  var remove_dialog_no_button = document.getElementById('Remove_Dialog-no');
  var remove_dialog_yes_button = document.getElementById('Remove_Dialog-yes');
  var remove_dialog_button = document.getElementById('Remove');
  remove_dialog_button.onclick = function() {
    var selection = document.querySelectorAll('[selected="yes"]')[0];
    info = selection.id.split('-');
    remove_dialog_header.innerHTML = "Remove " + info[0].charAt(0).toUpperCase() + info[0].slice(1);
    remove_dialog_type.innerHTML = info[0];
    remove_dialog_item.innerHTML = selection.childNodes[0].innerHTML;
    if (info[0] == "folder") {
      remove_dialog_warning.innerHTML = "<strong>WARNING:</strong> This will remove the folder and all subfolders and phrases! THIS CANNOT BE UNDONE!"
    } else {
      remove_dialog_warning.innerHTML = "<strong>WARNING:</strong> This cannot be undone!"
    }
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
    var selection = document.querySelectorAll('[selected="yes"]')[0].id.split('-')[1]
    modal.style.display = "none";
    remove_dialog.style.display = "none";
    data = JSON.stringify({id: selection})
    if (info[0] == "folder") {
      send2API(folder_API, "DELETE", data);
      resetFolderDropdown();
      resetPhraseList();
    } else if (info[0] == "phrase") {
      send2API(phrase_API, "DELETE", data);
      resetPhraseList();
    }
  }
});
