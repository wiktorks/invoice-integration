const toggleAllCheckboxes = (e) => {
  const mainCheckbox = e.target;

  let checkboxList = document.getElementsByClassName("invoice-checkbox");
  for (checkbox of checkboxList) {
    checkbox.checked = mainCheckbox.checked;
  }
};

const toggleInvoiceButtonDisplay = () => {
  //TODO Zoptymalizować tworzenie listy checkboxów
  const checkboxList = document.getElementsByClassName("checkbox");
  let invoiceButtonPanel = document.getElementById("invoice-button-panel");

  for (checkbox of checkboxList) {
    if (checkbox.checked) {
      invoiceButtonPanel.classList.remove("d-none");
      return;
    }
  }
  invoiceButtonPanel.classList.add("d-none");
};

let mainCheckbox = document
  .getElementsByClassName("invoice-main-checkbox")
  .item(0);
let checkboxList = document.getElementsByClassName("invoice-checkbox");
let toggleDateRangeButton = document.getElementById("date-range-button");

mainCheckbox.addEventListener("change", toggleAllCheckboxes);
mainCheckbox.addEventListener("change", toggleInvoiceButtonDisplay);
for (element of checkboxList) {
  element.addEventListener("change", toggleInvoiceButtonDisplay);
}

toggleInvoiceButtonDisplay();

const picker = new Litepicker({
  element: document.getElementById("litepicker"),
  singleMode: false,
  numberOfMonths: 2,
  numberOfColumns: 2,
  inlineMode: true
});
picker.show();

