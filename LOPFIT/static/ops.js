function adjustList(){
  var select = document.getElementById('Phrase_List');
  select.size = select.length;
}
window.addEventListener('resize', adjustList);
