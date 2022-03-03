var folder_API = "/folder/"
var phrase_API = "/phrase/"
var config_API = "/config/"

// API functions
function send2API (endpoint, method, data) {
  console.log(data)
  var xhr = new XMLHttpRequest();
  xhr.open(method, endpoint, false);
  if (data) {xhr.setRequestHeader('Content-Type', 'application/json');};
  xhr.send(data);
  if (xhr.readyState === 4) {
    return xhr.response;
  }
}

// Functionality functions
function savePhrase(id) {
  var p_name = document.getElementById('pname');
  var p_trigger = document.getElementById('ptrigger');
  var p_text = document.getElementById('Phrase_Text').childNodes[0];
  data = JSON.stringify({
    name: p_name.value,
    cmd: p_trigger.value,
    phrase_html: p_text.innerHTML,
    phrase_text: p_text.innerText
  });
  send2API(phrase_API+id.toString(), "POST", data);

  var phrases_name = document.getElementById('phrase-'+id.toString());
  phrases_name.innerText=p_name.value;
}
function loadPhrase(id){
  var p_name = document.getElementById('pname');
  var p_trigger = document.getElementById('ptrigger');
  var p_folder = document.getElementById('pfolder');
  var p_text = document.getElementById('Phrase_Text').childNodes[0];
  var p_text_parent = document.getElementById('Phrase_Text');
  var phrase = document.getElementById('Phrase');
  var save_button = document.getElementById('Save');
  p = JSON.parse(send2API(phrase_API + id.toString(), "GET"));
  save_button.setAttribute('phrase_id',id)
  p_text_parent.setAttribute('dirty','loading');
  p_name.value = p['name'];
  p_trigger.value = p['cmd'];
  quill.setContents([])
  quill.clipboard.dangerouslyPasteHTML(p['phrase_html']);
  phrase.style.display= "block";
  p_text_parent.setAttribute('dirty','no');
  var dirty = document.querySelectorAll('[dirty="yes"]');
  for (let i = 0; i < dirty.length; i++){
    dirty[i].setAttribute('dirty','no')
  }
}
function resetFolderDropdown (element,exclude=false) {
  var folderDropdown = document.getElementById(element);
  if (exclude){
    folders_HTML = JSON.parse(send2API(folder_API+exclude, "GET"));
  } else {
    folders_HTML = JSON.parse(send2API(folder_API, "GET"));
  }
  folderDropdown.innerHTML = folders_HTML['folders_HTML'];
}
function resetPhraseList () {
  var phraseList = document.getElementById('Phrase_List');
  phraseList_HTML = JSON.parse(send2API(phrase_API, "GET"));
  phraseList.innerHTML = "";
  phraseList.innerHTML = phraseList_HTML['phraseList_HTML'];
  // set Remove button status
  var removeButton = document.getElementById('Remove');
  var moveEdit_button = document.getElementById('MoveEdit');
  removeButton.disabled = false;
  removeButton.classList.remove("disabled")
  moveEdit_button.disabled=false;
  moveEdit_button.classList.remove("disabled");

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
        checkPhrase(treeitem.id.split('-')[1])
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
  var moveEdit_button = document.getElementById('MoveEdit');
  if (document.querySelectorAll('[role="treeitem"]').length >0){
    removeButton.disabled = false;
    removeButton.classList.remove("disabled")
    moveEdit_button.disabled=false;
    moveEdit_button.classList.remove("disabled");
  } else {
    removeButton.disabled = true;
    removeButton.classList.add("disabled")
    moveEdit_button.disabled=true;
    moveEdit_button.classList.add("disabled");
  }
  if (selected.id.split('-')[0] == "folder") {
    moveEdit_button.classList.remove("move");
    moveEdit_button.classList.add("edit");
  } else {
    moveEdit_button.classList.remove("edit");
    moveEdit_button.classList.add("move");
  }
}
function checkPhrase(id, override=false) {
  var dirtycount = document.querySelectorAll('[dirty="yes"]').length;
  if (dirtycount > 0){
    if (!override){
      var modal = document.getElementById('ModalConatiner');
      unsavedChangesDialog(modal);
    } else {
      savePhrase(id);
      loadPhrase(id);
    }
  } else {loadPhrase(id)}
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
      send2API(folder_API+id.toString(), "POST", data);
      resetPhraseList();
    } else if (info[0] == "phrase") {
      data = JSON.stringify({
        folder_id: pfolder
      });
      send2API(phrase_API+info[1].toString(), "POST", data);
      resetPhraseList();
    }
  }
}

// New Folder Dialog
function editDialog (modalConatiner){
  // Display Dialog
  edit_HTML = '<div id="Edit_Dialog" class="ModalDialog">'
  edit_HTML += '<span id="Edit_Dialog-close" class="close">&times;</span>'
  edit_HTML += '<h2 id="Edit_Dialog-header">Edit Folder</h2>'
  edit_HTML += '<div>'
  edit_HTML += '<span>Folder Name: </span><input type="text" id="folder_name"></input><br/>'
  edit_HTML += '<span>Parent Folder: </span><select id="edit-pfolder" name="pfolder"></select><br/>'
  edit_HTML += '<button id="Edit_Dialog-ok">OK</button>'
  edit_HTML += '</div></div>'
  modalConatiner.innerHTML = edit_HTML;
  var selected = document.querySelectorAll('[selected="yes"]')[0];
  var folder_name = document.getElementById('folder_name');
  folder_name.value = selected.innerText
  resetFolderDropdown('edit-pfolder', selected.id.split('-')[1]);
  modalConatiner.style.display = "block";
  // Handle Dialog Elements
  var edit_close_button = document.getElementById('Edit_Dialog-close');
  edit_close_button.onclick = function() {
    modalConatiner.style.display = "none";
    modalConatiner.innerHTML = "";
  }
  var edit_ok_button = document.getElementById('Edit_Dialog-ok');
  edit_ok_button.onclick = function() {
    var folder_name = document.getElementById('folder_name').value;
    var pfolder = document.getElementById('edit-pfolder').value;
    modalConatiner.style.display = "none";
    data = JSON.stringify({
      folder_id: selected.id.split('-')[1],
      name: folder_name,
      parent_folder_id: pfolder
    })
    send2API(folder_API+id.toString(), "POST", data);
    resetPhraseList();
    modalConatiner.innerHTML = "";
  }
}

// Remove Dialog
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
      send2API(folder_API+id.toString(), "DELETE", data);
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
  settings_HTML = '<div id="Settings_Dialog" class="ModalDialog">'
  settings_HTML += '<span id="Settings_Dialog-close" class="close">&times;</span>'
  settings_HTML += '<h2 id="Settings_Dialog-header">Settings</h2>'
  settings_HTML += '<div><span>Execution key: </span>'
  settings_HTML += '<select id="execution_key" name="execution_key">'
  settings_HTML += '<option value=0>Space</option>'
  settings_HTML += '<option value=1>Tab</option>'
  settings_HTML += '<option value=2>Enter</option>'
  settings_HTML += '<option value=3>Execute Immediately</option>'
  settings_HTML += '<option value=-1>Disabled</option>'
  settings_HTML += '</select><br/>'
  settings_HTML += '<button id="Settings_Dialog-ok">OK</button>'
  settings_HTML += '</div></div>'
  modalConatiner.innerHTML = settings_HTML;
  var execution_key = document.getElementById('execution_key');
  modalConatiner.style.display = "block";
  execution_key_value = JSON.parse(send2API(config_API+"execution_key", "GET"))['value'];
  execution_key.value = execution_key_value;

  // Handle Dialog Elements
  var settings_close = document.getElementById('Settings_Dialog-close');
  settings_close.onclick = function() {
    modalConatiner.style.display = "none";
    modalConatiner.innerHTML = "";
  }
  var settings_ok = document.getElementById('Settings_Dialog-ok');
  settings_ok.onclick = function() {
    modalConatiner.style.display = "none";
    data = JSON.stringify({
      key: "execution_key",
      value: execution_key.value
    })
    data = JSON.parse(send2API(config_API+"execution_key", "POST", data));
  }
}

// Unsaved Changes Dialog
function unsavedChangesDialog (modalConatiner){
  // Display Dialog
  unsavedChanges_HTML = '<div id="unsavedChanges_Dialog" class="ModalDialog">'
  unsavedChanges_HTML += '<span id="unsavedChanges_Dialog-close" class="close">&times;</span>'
  unsavedChanges_HTML += '<h2 id="unsavedChanges_Dialog-header">Unsaved Changes</h2>'
  unsavedChanges_HTML += '<div><span>Do you want to save your changes?</span>'
  unsavedChanges_HTML += '<div><button id="unsavedChanges_Dialog-no">No</button>';
  unsavedChanges_HTML += '<button id="unsavedChanges_Dialog-yes">Yes</button></div>';
  unsavedChanges_HTML += '</div></div>';
  modalConatiner.innerHTML = unsavedChanges_HTML;
  var execution_key = document.getElementById('execution_key');
  modalConatiner.style.display = "block";

  // Handle Dialog Elements
  var unsavedChanges_close = document.getElementById('unsavedChanges_Dialog-close');
  unsavedChanges_close.onclick = function() {
    modalConatiner.style.display = "none";
    modalConatiner.innerHTML = "";
  }
  var unsavedChanges_no = document.getElementById('unsavedChanges_Dialog-no');
  unsavedChanges_no.onclick = function() {
    modalConatiner.style.display = "none";
    modalConatiner.innerHTML = "";
    var id = document.getElementById('Save').getAttribute('phrase_id');
    loadPhrase(id)
  }
  var unsavedChanges_yes = document.getElementById('unsavedChanges_Dialog-yes');
  unsavedChanges_yes.onclick = function() {
    modalConatiner.style.display = "none";
    modalConatiner.innerHTML = "";
    var id = document.getElementById('Save').getAttribute('phrase_id');
    checkPhrase(id, true)
  }
}

// On Load setup
window.addEventListener('load', function () {
  // Grab some need IDs
  resetPhraseList()
  var modal = document.getElementById('ModalConatiner');
  var newFolder_button = document.getElementById('New_Folder');
  var newPhrase_button = document.getElementById('New_Phrase');
  var moveEdit_button = document.getElementById('MoveEdit');
  var remove_button = document.getElementById('Remove');
  var settings_button = document.getElementById('Settings');
  var save_button = document.getElementById('Save');
  var phrase_name = document.getElementById('Phrase_Name');
  var phrase_trigger = document.getElementById('Phrase_Trigger');
  var p_name = document.getElementById('pname');
  var p_trigger = document.getElementById('ptrigger');

  // On Click handlers
  newFolder_button.onclick = function() {newFolder(modal);}
  newPhrase_button.onclick = function() {newPhrase(modal);}
  moveEdit_button.onclick = function() {
    if (moveEdit_button.classList=="move"){
      moveDialog(modal);
    } else if (moveEdit_button.classList=="edit") {
      editDialog(modal);
    }
  }
  remove_button.onclick = function() {removeDialog(modal);}
  settings_button.onclick = function() {settingsDialog(modal);}
  save_button.onclick = function() {
    var id = save_button.getAttribute('phrase_id');
    savePhrase(id)
  }
  // Change handlers
  p_name.onchange = function() {phrase_name.setAttribute('dirty','yes')}
  p_trigger.onchange = function() {phrase_trigger.setAttribute('dirty','yes')}

  quill.on('text-change', function(delta, oldDelta, source) {
    var p_text = document.getElementById('Phrase_Text');
    if (p_text.getAttribute('dirty')!="loading"){
        p_text.setAttribute('dirty','yes');
    }
  });
});
