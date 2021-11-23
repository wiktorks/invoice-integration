export const queryParamsParser = () => {
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
  return [startDate, endDate];
};
