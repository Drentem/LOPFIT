var folder_API = "/folder/"
var phrase_API = "/phrase/"

// API functions
function send2API (endpoint, method, data) {
  var xhr = new XMLHttpRequest();
  xhr.open(method, endpoint, false);
  if (data) {xhr.setRequestHeader('Content-Type', 'application/json');};
  xhr.send(data);
  if (xhr.readyState === 4) {
    return xhr.response;
  }
}

// Functionality functions
function resetFolderDropdown (element) {
  var folderDropdown = document.getElementById(element);
  folders = JSON.parse(send2API(folder_API, "GET"));
  folderDropdown.innerHTML = folders['folders'];
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
function updateSelected (id) {
  var items = document.querySelectorAll('[role="treeitem"]');
  for (var i = 0; i < items.length; i++) {
    items[i].style.color = "";
    items[i].setAttribute('selected','no');
  }
  selected = document.getElementById(id);
  selected.setAttribute('selected','yes');
}

// Dialog functions
function removeDialog (modalConatiner){
  // Get item
  var selection = document.querySelectorAll('[selected="yes"]')[0];
  info = selection.id.split('-');

  // Display Dialog
  var remove_HTML = '<div id="Remove_Dialog" class="ModalDialog">';
  remove_HTML += '<span id="Remove_Dialog-close" class="close">&times;</span>';
  remove_HTML += '<h2 id="Remove_Dialog-header">Remove ' + info[0].charAt(0).toUpperCase() + info[0].slice(1) + '</h2><div>';
  remove_HTML += 'Are you sure you want to remove the following ' + info[0] + ':<br/>';
  remove_HTML += '<br/>' + selection.childNodes[0].innerHTML + '<br/><br/>';
  if (info[0] == "folder") {
    remove_HTML += "<strong>WARNING: This will remove the folder and all subfolders and phrases! THIS CANNOT BE UNDONE!</strong>";
  } else {
    remove_HTML += "<strong>WARNING: This cannot be undone!</strong>";
  };
  remove_HTML += '<button id="Remove_Dialog-no">No</button>';
  remove_HTML += '<button id="Remove_Dialog-yes">Yes</button>';
  remove_HTML += '</div></div>';
  modalConatiner.innerHTML = remove_HTML;
  modalConatiner.style.display = "block";

  // Handle Dialog Elements
  var remove_dialog_close_button = document.getElementById('Remove_Dialog-close');
  remove_dialog_close_button.onclick = function() {
    modalConatiner.style.display = "none";
    modalConatiner.innerHTML = "";
  }
  var remove_dialog_no_button = document.getElementById('Remove_Dialog-no');
  remove_dialog_no_button.onclick = function() {
    modalConatiner.style.display = "none";
    modalConatiner.innerHTML = "";
  }
  var remove_dialog_yes_button = document.getElementById('Remove_Dialog-yes');
  remove_dialog_yes_button.onclick = function() {
    var selection = document.querySelectorAll('[selected="yes"]')[0].id.split('-')[1]
    modalConatiner.style.display = "none";
    data = JSON.stringify({id: selection})
    if (info[0] == "folder") {
      send2API(folder_API, "DELETE", data);
      resetFolderDropdown();
      resetPhraseList();
    } else if (info[0] == "phrase") {
      send2API(phrase_API, "DELETE", data);
      resetPhraseList();
    }
    modalConatiner.innerHTML = "";
  }
}

// New Folder Dialog
function newFolder (modalConatiner){
  // Display Dialog
  newFolder_HTML = '<div id="New_Folder_Dialog" class="ModalDialog">'
  newFolder_HTML += '<span id="New_Folder_Dialog-close" class="close">&times;</span>'
  newFolder_HTML += '<h2 id="New_Folder_Dialog-header">New Folder</h2>'
  newFolder_HTML += '<div>'
  newFolder_HTML += '<span>Folder Name: </span><input type="text" id="folder_name"></input><br/>'
  newFolder_HTML += '<span>Parent Folder: </span><select id="new-pfolder" name="pfolder"></select><br/>'
  newFolder_HTML += '<button id="New_Folder_Dialog-ok">OK</button>'
  newFolder_HTML += '</div></div>'
  modalConatiner.innerHTML = newFolder_HTML;
  resetFolderDropdown('new-pfolder');
  modalConatiner.style.display = "block";

  // Handle Dialog Elements
  var new_folder_dialog_close_button = document.getElementById('New_Folder_Dialog-close');
  new_folder_dialog_close_button.onclick = function() {
    modalConatiner.style.display = "none";
    modalConatiner.innerHTML = "";
  }
  var new_folder_dialog_ok_button = document.getElementById('New_Folder_Dialog-ok');
  new_folder_dialog_ok_button.onclick = function() {
    var folder_name = document.getElementById('folder_name').value;
    var pfolder = document.getElementById('new-pfolder').value;
    modalConatiner.style.display = "none";
    data = JSON.stringify({
      name: folder_name,
      parent_folder_id: pfolder
    })
    send2API(folder_API, "POST", data);
    resetFolderDropdown('pfolder');
    resetPhraseList();
    modalConatiner.innerHTML = "";
  }
}

// New Phrase Dialog
function newPhrase (modalConatiner){
  // Display Dialog
  newPhrase_HTML = '<div id="New_Phrase_Dialog" class="ModalDialog">'
  newPhrase_HTML += '<span id="New_Phrase_Dialog-close" class="close">&times;</span>'
  newPhrase_HTML += '<h2 id="New_Phrase_Dialog-header">New Phrase</h2>'
  newPhrase_HTML += '<div>'
  newPhrase_HTML += '<span>Folder: </span><select id="pfolder" name="pfolder"></select><br/>'
  newPhrase_HTML += '<button id="New_Phrase_Dialog-ok">OK</button>'
  newPhrase_HTML += '</div></div>'
  modalConatiner.innerHTML = newPhrase_HTML;
  resetFolderDropdown('pfolder');
  modalConatiner.style.display = "block";

  // Handle Dialog Elements
  var new_folder_dialog_close_button = document.getElementById('New_Phrase_Dialog-close');
  new_folder_dialog_close_button.onclick = function() {
    modalConatiner.style.display = "none";
    modalConatiner.innerHTML = "";
  }
  var new_folder_dialog_ok_button = document.getElementById('New_Phrase_Dialog-ok');
  new_folder_dialog_ok_button.onclick = function() {
    var pfolder = document.getElementById('pfolder').value;
    modalConatiner.style.display = "none";
    data = JSON.stringify({
      name: "New Phrase",
      folder_id: pfolder
    })
    id = JSON.parse(send2API(phrase_API, "POST", data))['phrase_id'];
    resetPhraseList();
    modalConatiner.innerHTML = "";
    p_id.innerHTML = id;
    p_name.value = "New Phrase";
    p_trigger.value = "";
    p_folder.value = pfolder;
    p_text.innerText = "";
    phrase.style.display="block";
  }
}

// On Load setup
window.addEventListener('load', function () {
  // Grab some need IDs
  var modal = document.getElementById('ModalConatiner');
  var p_id = document.getElementById('Phrase_ID');
  var p_name = document.getElementById('pname');
  var p_trigger = document.getElementById('ptrigger');
  var p_folder = document.getElementById('pfolder');
  var p_text = document.getElementById('Phrase_Text').childNodes[0];
  var phrase = document.getElementById('Phrase');

  // Initiate remove
  var remove_dialog_button = document.getElementById('Remove');
  remove_dialog_button.onclick = function() {
    removeDialog(modal);
  }
  // New Folder Dialog
  var new_folder_button = document.getElementById('New_Folder');
  new_folder_button.onclick = function() {
    newFolder(modal);
  }

  // New Phrase Handler
  var new_phrase_button = document.getElementById('New_Phrase');
  new_phrase_button.onclick = function() {
    newPhrase(modal);
  }
});
