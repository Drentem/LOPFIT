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
  folders_HTML = JSON.parse(send2API(folder_API, "GET"));
  folderDropdown.innerHTML = folders_HTML['folders_HTML'];
}
function resetPhraseList () {
  var phraseList = document.getElementById('Phrase_List');
  phraseList_HTML = JSON.parse(send2API(phrase_API, "GET"));
  phraseList.innerHTML = "";
  phraseList.innerHTML = phraseList_HTML['phraseList_HTML'];
  console.log(phraseList_HTML['phraseList_HTML'])
  // set Remove button status
  var removeButton = document.getElementById('Remove');
  var move_button = document.getElementById('Move');
  removeButton.disabled = false;
  removeButton.classList.remove("disabled")
  move_button.disabled=false;
  move_button.classList.remove("disabled");

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
      if (treeitem.classList.contains("doc")){
        loadPhrase(treeitem.id)
      }
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
  var removeButton = document.getElementById('Remove');
  var move_button = document.getElementById('Move');
  if (document.querySelectorAll('[role="treeitem"]').length >0){
    removeButton.disabled = false;
    removeButton.classList.remove("disabled")
    move_button.disabled=false;
    move_button.classList.remove("disabled");
  } else {
    removeButton.disabled = true;
    removeButton.classList.add("disabled")
    move_button.disabled=true;
    move_button.classList.add("disabled");
  }
}
function loadPhrase(id) {
  var p_name = document.getElementById('pname');
  var p_trigger = document.getElementById('ptrigger');
  var p_folder = document.getElementById('pfolder');
  var p_text = document.getElementById('Phrase_Text').childNodes[0];
  var phrase = document.getElementById('Phrase');
  var id = id.split('-')[1];

  p = JSON.parse(send2API(phrase_API + id.toString(), "GET"));
  p_name.value = p['name'];
  p_trigger.value = p['cmd'];
  p_text.innerText = p['phrase'];
  phrase.style.display= "block";
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
  var newPhrase_close = document.getElementById('New_Phrase_Dialog-close');
  newPhrase_close.onclick = function() {
    modalConatiner.style.display = "none";
    modalConatiner.innerHTML = "";
  }
  var newPhrase_ok = document.getElementById('New_Phrase_Dialog-ok');
  newPhrase_ok.onclick = function() {
    var pfolder = document.getElementById('pfolder').value;
    modalConatiner.style.display = "none";
    data = JSON.stringify({
      id: "new",
      name: "New Phrase",
      cmd: "NewPhrase",
      folder_id: pfolder
    })
    data = JSON.parse(send2API(phrase_API, "POST", data));
    resetPhraseList();
    modalConatiner.innerHTML = "";
    var p_name = document.getElementById('pname');
    var p_trigger = document.getElementById('ptrigger');
    var p_text = document.getElementById('Phrase_Text').childNodes[0];
    var phrase = document.getElementById('Phrase');
    p_name.value = "New Phrase";
    p_trigger.value = "";
    p_text.innerText = "";
    phrase.style.display="block";
  }
}

// Move Dialog
function moveDialog (modalConatiner){
  // Get item
  var selection = document.querySelectorAll('[selected="yes"]')[0];
  info = selection.id.split('-');
  var child = selection.firstElementChild;
  label = child ? child.innerText : selection.innerText;

  // Display Dialog
  move_HTML = '<div id="Move_Dialog" class="ModalDialog">'
  move_HTML += '<span id="Move_Dialog-close" class="close">&times;</span>'
  move_HTML += '<h2 id="Move_Dialog-header">Move ' + info[0].charAt(0).toUpperCase() + info[0].slice(1) + '</h2><div>';
  move_HTML += '<div>'
  move_HTML += '<span>New Location: </span><select id="pfolder" name="pfolder"></select><br/>'
  move_HTML += '<button id="Move_Dialog-ok">OK</button>'
  move_HTML += '</div></div>'
  modalConatiner.innerHTML = move_HTML;
  resetFolderDropdown('pfolder');
  modalConatiner.style.display = "block";

  // Handle Dialog Elements
  var newPhrase_close = document.getElementById('Move_Dialog-close');
  newPhrase_close.onclick = function() {
    modalConatiner.style.display = "none";
    modalConatiner.innerHTML = "";
  }
  var newPhrase_ok = document.getElementById('Move_Dialog-ok');
  newPhrase_ok.onclick = function() {
    modalConatiner.style.display = "none";
    var pfolder = document.getElementById('pfolder').value;
    if (info[0] == "folder") {
      data = JSON.stringify({
        folder_id: info[1],
        parent_folder_id: pfolder
      });
      send2API(folder_API, "POST", data);
      resetPhraseList();
    } else if (info[0] == "phrase") {
      var p_name = document.getElementById('pname');
      var p_trigger = document.getElementById('ptrigger');
      var p_text = document.getElementById('Phrase_Text').childNodes[0];
      var phrase = document.getElementById('Phrase');
      p_name.value = "New Phrase";
      p_trigger.value = "";
      p_text.innerText = "";
      phrase.style.display="none";
      send2API(phrase_API+id.toString(), "POST");
      resetPhraseList();
    }
  }
}

// Dialog functions
function removeDialog (modalConatiner){
  // Get item
  var selection = document.querySelectorAll('[selected="yes"]')[0];
  info = selection.id.split('-');
  var child = selection.firstElementChild;
  label = child ? child.innerText : selection.innerText;

  // Display Dialog
  var remove_HTML = '<div id="Remove_Dialog" class="ModalDialog">';
  remove_HTML += '<span id="Remove_Dialog-close" class="close">&times;</span>';
  remove_HTML += '<h2 id="Remove_Dialog-header">Remove ' + info[0].charAt(0).toUpperCase() + info[0].slice(1) + '</h2><div>';
  remove_HTML += 'Are you sure you want to remove the following ' + info[0] + ':<br/>';
  remove_HTML += '<br/>' + label + '<br/><br/>';
  if (info[0] == "folder") {
    remove_HTML += "<strong>WARNING: This will remove the folder and all subfolders and phrases! THIS CANNOT BE UNDONE!</strong>";
  } else {
    remove_HTML += "<strong>WARNING: This cannot be undone!</strong>";
  };
  remove_HTML += '<div><button id="Remove_Dialog-no">No</button>';
  remove_HTML += '<button id="Remove_Dialog-yes">Yes</button></div>';
  remove_HTML += '</div></div>';
  modalConatiner.innerHTML = remove_HTML;
  modalConatiner.style.display = "block";

  // Handle Dialog Elements
  document.getElementById('Remove_Dialog-close').onclick = function() {
    modalConatiner.style.display = "none";
    modalConatiner.innerHTML = "";
  }
  document.getElementById('Remove_Dialog-no').onclick = function() {
    modalConatiner.style.display = "none";
    modalConatiner.innerHTML = "";
  }
  document.getElementById('Remove_Dialog-yes').onclick = function() {
    modalConatiner.style.display = "none";
    if (info[0] == "folder") {
      data = JSON.stringify({id: info[1]})
      send2API(folder_API, "DELETE", data);
      resetPhraseList();
    } else if (info[0] == "phrase") {
      var p_name = document.getElementById('pname');
      var p_trigger = document.getElementById('ptrigger');
      var p_text = document.getElementById('Phrase_Text').childNodes[0];
      var phrase = document.getElementById('Phrase');
      p_name.value = "New Phrase";
      p_trigger.value = "";
      p_text.innerText = "";
      phrase.style.display="none";
      send2API(phrase_API+id.toString(), "DELETE");
      resetPhraseList();
    }
    modalConatiner.innerHTML = "";
  }
}

// Settings Dialog
function settingsDialog (modalConatiner){
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
  var newPhrase_close = document.getElementById('New_Phrase_Dialog-close');
  newPhrase_close.onclick = function() {
    modalConatiner.style.display = "none";
    modalConatiner.innerHTML = "";
  }
  var newPhrase_ok = document.getElementById('New_Phrase_Dialog-ok');
  newPhrase_ok.onclick = function() {
    var pfolder = document.getElementById('pfolder').value;
    modalConatiner.style.display = "none";
    data = JSON.stringify({
      id: "new",
      name: "New Phrase",
      cmd: "NewPhrase",
      folder_id: pfolder
    })
    data = JSON.parse(send2API(phrase_API, "POST", data));
    resetPhraseList();
    modalConatiner.innerHTML = "";
    var p_name = document.getElementById('pname');
    var p_trigger = document.getElementById('ptrigger');
    var p_text = document.getElementById('Phrase_Text').childNodes[0];
    var phrase = document.getElementById('Phrase');
    p_name.value = "New Phrase";
    p_trigger.value = "";
    p_text.innerText = "";
    phrase.style.display="block";
  }
}


// On Load setup
window.addEventListener('load', function () {
  // Grab some need IDs
  resetPhraseList()
  var modal = document.getElementById('ModalConatiner');
  var newFolder_button = document.getElementById('New_Folder');
  var newPhrase_button = document.getElementById('New_Phrase');
  var move_button = document.getElementById('Move');
  var remove_button = document.getElementById('Remove');
  var settings_button = document.getElementById('Settings');

  var selection = document.querySelectorAll('[selected="yes"]')
    if (selection.length > 0) {
      move_button.disabled=false;
      move_button.classList.remove("disabled");
      remove_button.disabled=false;
      remove_button.classList.remove("disabled");
    } else {
      move_button.disabled=true;
      move_button.classList.add("disabled");
      remove_button.disabled=true;
      remove_button.classList.add("disabled");
    }

  // On Click handlers
  newFolder_button.onclick = function() {newFolder(modal);}
  newPhrase_button.onclick = function() {newPhrase(modal);}
  move_button.onclick = function() {moveDialog(modal);}
  remove_button.onclick = function() {removeDialog(modal);}
  settings_button.onclick = function() {settingsDialog(modal);}
});
