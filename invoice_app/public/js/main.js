import {
  toggleAllCheckboxes,
  toggleInvoiceButtonDisplay,
} from "./modules/checkboxes.js";
import { picker, filterByDate } from "./modules/calendar.js";
import {
  viewMail,
  sendInvoiceMail,
  viewMails,
  sendMails,
} from "./modules/mailer.js";

const mainCheckbox = document
  .getElementsByClassName("invoice-main-checkbox")
  .item(0);
const mainTaskCheckboxList =
  document.getElementsByClassName("task-main-checkbox");
const checkboxList = document.getElementsByClassName("invoice-checkbox");
const mailViewButtons = document.getElementsByClassName("mail-sender");
const mailSendButton = document.getElementsByClassName("send-mail")[0];
const calendarButton = document.getElementById("filter-by-date");
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

mainCheckbox.addEventListener("change", toggleAllCheckboxes);
mainCheckbox.addEventListener("change", toggleInvoiceButtonDisplay);
for (let element of checkboxList) {
  element.addEventListener("change", toggleInvoiceButtonDisplay);
}
for (let mainTaskCheckbox of mainTaskCheckboxList) {
  mainTaskCheckbox.addEventListener("change", toggleAllCheckboxes);
}

toggleInvoiceButtonDisplay();

picker.show();

calendarButton.addEventListener("click", filterByDate);
