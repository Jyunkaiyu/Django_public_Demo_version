document.getElementById("clear").onclick=function() {clear()};
function clear() {
  var checkboxes=document.getElementsByClassName("a");
  for (var i=0;i<checkboxes.length;i++) {
      checkboxes[i].checked="";
  }
}
