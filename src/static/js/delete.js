const modalBtn = document.getElementById("modalBtn")
const modalText = document.getElementById("modalText")
const  buttons = document.getElementsByClassName("deleteButton")

for (var counter = 0; counter < buttons.length; counter++) {
  buttons[counter].addEventListener("click", (btn) => {
    
    const span = btn.delegateTarget.getElementsByTagName('span')
    modalBtn.href = span[0].innerHTML;
    modalText.innerText = `Once deleted, this ${span[1].innerHTML} will not be recoverable. Are you sure you want to continue?`
  });
};