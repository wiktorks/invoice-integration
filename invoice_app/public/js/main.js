import { loadCompanyData } from "./modules/checkboxes.js";
import { picker, filterByDate } from "./modules/calendar.js";

const calendarButton = document.getElementById("filter-by-date");

picker.show();
loadCompanyData(picker);

calendarButton.addEventListener("click", filterByDate);
