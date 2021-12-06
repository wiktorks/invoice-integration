import {
  viewMail,
  sendInvoiceMail,
  viewMails,
  sendMails,
} from "./mailer.js";

const setCheckboxesAndMailButtonsHandlers = () => {
  const mailViewButtons = document.getElementsByClassName("mail-sender");
  const mailSendButton = document.getElementsByClassName("send-mail")[0];
  
  const multipleMailViewButtons = document.getElementsByClassName(
    "multiple-email-sender"
  );
  const multipleMailSendButton =
    document.getElementsByClassName("send-multiple-mail")[0];

  for (let element of mailViewButtons) {
    element.addEventListener("click", viewMail);
  }

  for (let element of multipleMailViewButtons) {
    element.addEventListener("click", viewMails);
  }
  mailSendButton.addEventListener("click", sendInvoiceMail);
  multipleMailSendButton.addEventListener("click", sendMails);

  const mainCheckbox = document
    .getElementsByClassName("invoice-main-checkbox")
    .item(0);
  const mainTaskCheckboxList =
    document.getElementsByClassName("task-main-checkbox");
  const checkboxList = document.getElementsByClassName("invoice-checkbox");

  mainCheckbox.addEventListener("change", toggleAllCheckboxes);
  mainCheckbox.addEventListener("change", toggleInvoiceButtonDisplay);
  for (let element of checkboxList) {
    element.addEventListener("change", toggleInvoiceButtonDisplay);
  }
  for (let mainTaskCheckbox of mainTaskCheckboxList) {
    mainTaskCheckbox.addEventListener("change", toggleAllCheckboxes);
  }
};

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

export const loadCompanyData = (picker) => {
  document.getElementById("company-table").innerHTML = "";
  const spinner = document.getElementById("loader");
  spinner.removeAttribute("hidden");
  const start = picker.getStartDate();
  const end = picker.getEndDate();
  fetch(
    window.location.origin +
      `/companies?start_date=${start.getTime()}&end_date=${end.getTime()}`
  )
    .then((response) => response.text())
    .then((table) => {
      spinner.setAttribute("hidden", "");
      document.getElementById("company-table").innerHTML = table;
      setCheckboxesAndMailButtonsHandlers();
      toggleInvoiceButtonDisplay();
    });
};
