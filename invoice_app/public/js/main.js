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

const urlParams = new URLSearchParams(window.location.search);
const startDateQuery = urlParams.get('start_date')
const endDateQuery = urlParams.get('end_date')
let endDate = endDateQuery ? endDateQuery: null
let startDate;
if (endDate) {
  startDate  = startDateQuery ? startDateQuery: new Date(endDate.setMonth(endDate.getMonth()-1));
} else {
  const date_today = new Date()
  startDate  = startDateQuery ? startDateQuery: new Date(date_today.setMonth(date_today.getMonth()-1));
}
const picker = new Litepicker({
  element: document.getElementById("litepicker"),
  singleMode: false,
  numberOfMonths: 2,
  numberOfColumns: 2,
  inlineMode: true,
  startDate: startDate,
  endDate: endDate ? endDate: new Date()
});
picker.show();

const filterByDate = () => {
  start = picker.getStartDate()
  end = picker.getEndDate()

  window.location.href = window.location.origin + `/dev?start_date=${start.getTime()}&end_date=${end.getTime()}`
}

calendarButton = document.getElementById('filter-by-date')
calendarButton.addEventListener("click", filterByDate)

