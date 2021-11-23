import { queryParamsParser } from "./queryParamsParser.js";

const [startDate, endDate] = queryParamsParser();

export const picker = new Litepicker({
  element: document.getElementById("litepicker"),
  singleMode: false,
  numberOfMonths: 2,
  numberOfColumns: 2,
  inlineMode: true,
  startDate: startDate,
  endDate: endDate ? endDate : new Date(),
});

export const filterByDate = () => {
  const start = picker.getStartDate();
  const end = picker.getEndDate();

  window.location.href =
    window.location.origin +
    `/?start_date=${start.getTime()}&end_date=${end.getTime()}`;
};
