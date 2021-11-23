export const toggleAllCheckboxes = (e) => {
  const mainCheckbox = e.target;
  let className = mainCheckbox.classList.item(1);
  if (className.split("-")[0] == "task") {
    let temp = mainCheckbox.classList.item(2).split("-");
    temp.splice(1, 1);
    className = temp.join("-");
  }
  let checkboxList = document.getElementsByClassName(className);
  for (let checkbox of checkboxList) {
    checkbox.checked = mainCheckbox.checked;
  }
};

export const toggleInvoiceButtonDisplay = () => {
  //TODO Zoptymalizować tworzenie listy checkboxów
  const checkboxList = document.getElementsByClassName("invoice-checkbox");
  let invoiceButtonPanel = document.getElementById("invoice-button-panel");

  for (let checkbox of checkboxList) {
    if (checkbox.checked) {
      invoiceButtonPanel.classList.remove("d-none");
      return;
    }
  }
  invoiceButtonPanel.classList.add("d-none");
};
