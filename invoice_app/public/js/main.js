const urlParams = new URLSearchParams(window.location.search);
const startDateQuery = urlParams.get("start_date");
const endDateQuery = urlParams.get("end_date");
let endDate = endDateQuery ? endDateQuery : null;
let startDate;
if (endDate) {
  startDate = startDateQuery
    ? startDateQuery
    : new Date(endDate.setMonth(endDate.getMonth() - 1));
} else {
  const date_today = new Date();
  startDate = startDateQuery
    ? startDateQuery
    : new Date(date_today.setMonth(date_today.getMonth() - 1));
}

const toggleAllCheckboxes = (e) => {
  const mainCheckbox = e.target;
  className = mainCheckbox.classList.item(1);
  if (className.split("-")[0] == "task") {
    temp = mainCheckbox.classList.item(2).split("-");
    temp.splice(1, 1);
    className = temp.join("-");
  }
  let checkboxList = document.getElementsByClassName(className);
  for (checkbox of checkboxList) {
    checkbox.checked = mainCheckbox.checked;
  }
};

const toggleInvoiceButtonDisplay = () => {
  //TODO Zoptymalizować tworzenie listy checkboxów
  const checkboxList = document.getElementsByClassName("invoice-checkbox");
  let invoiceButtonPanel = document.getElementById("invoice-button-panel");

  for (checkbox of checkboxList) {
    if (checkbox.checked) {
      invoiceButtonPanel.classList.remove("d-none");
      return;
    }
  }
  invoiceButtonPanel.classList.add("d-none");
};

// TODO Zmieniaj dynamicznie godziny po zmianie checkboxa!
const sendInvoiceMail = (e) => {
  const el = e.target;
  const companyId = el.classList.item(2).split("-").at(-1);
  const company = document.getElementById(`company-${companyId}`);
  my_date = endDate ? endDate : new Date()
  let mail = {
    name: company.children[2].innerText,
    date_start: startDate.getTime(),
    date_end: my_date.getTime(),
  };
  taskElements = document.querySelectorAll(`.tasks-${companyId} tbody tr`);
  taskList = [];
  totalBillable = 0;
  totalNonBillable = 0;
  for (element of taskElements) {
    const checkbox = element.children[0].firstChild;
    if (checkbox.checked) {
      totalBillable += parseInt(
        element.children[3].attributes["data-time"].value
      );
      totalNonBillable += parseInt(
        element.children[4].attributes["data-time"].value
      );
      taskList.push({
        name: element.children[1].innerText,
        assignee: element.children[2].innerText,
        billable: element.children[3].attributes["data-time"].value,
        non_billable: element.children[4].attributes["data-time"].value,
      });
    }
  }
  mail.tasks = taskList;
  mail.billable = totalBillable;
  mail.non_billable = totalNonBillable;
  // ! PAMIĘTAJ O /dev
  fetch(window.location.origin + "/dev/sendmail", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(mail),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.message === "success") {
        alert("Pomyślnie wysłano wiadomość!");
      }
    })
    .catch(e => {
      alert("Nie udało sie wysłać maila");
      console.log(e)
    });
};

let mainCheckbox = document
  .getElementsByClassName("invoice-main-checkbox")
  .item(0);
let mainTaskCheckboxList =
  document.getElementsByClassName("task-main-checkbox");
let checkboxList = document.getElementsByClassName("invoice-checkbox");
let toggleDateRangeButton = document.getElementById("date-range-button");
let mailSendButtons = document.getElementsByClassName("mail-sender");
for (element of mailSendButtons) {
  element.addEventListener("click", sendInvoiceMail);
}

mainCheckbox.addEventListener("change", toggleAllCheckboxes);
mainCheckbox.addEventListener("change", toggleInvoiceButtonDisplay);
for (element of checkboxList) {
  element.addEventListener("change", toggleInvoiceButtonDisplay);
}
for (mainTaskCheckbox of mainTaskCheckboxList) {
  mainTaskCheckbox.addEventListener("change", toggleAllCheckboxes);
}

toggleInvoiceButtonDisplay();

const picker = new Litepicker({
  element: document.getElementById("litepicker"),
  singleMode: false,
  numberOfMonths: 2,
  numberOfColumns: 2,
  inlineMode: true,
  startDate: startDate,
  endDate: endDate ? endDate : new Date(),
});
picker.show();

const filterByDate = () => {
  start = picker.getStartDate();
  end = picker.getEndDate();

  window.location.href =
    window.location.origin +
    `/dev?start_date=${start.getTime()}&end_date=${end.getTime()}`;
};

calendarButton = document.getElementById("filter-by-date");
calendarButton.addEventListener("click", filterByDate);
