import { queryParamsParser } from "./queryParamsParser.js";

const getCompanyReportData = (companyId) => {
  const [startDate, endDate] = queryParamsParser();
  const company = document.getElementById(`company-${companyId}`);
  const my_date = endDate ? endDate : new Date();
  let mail = {
    name: company.children[2].innerText,
    date_start: startDate instanceof Date ? startDate.getTime() : startDate,
    date_end: my_date instanceof Date ? my_date.getTime() : my_date,
  };
  const taskElements = document.querySelectorAll(
    `.tasks-${companyId} tbody tr`
  );
  let taskList = [];
  let totalBillable = 0;
  let totalNonBillable = 0;
  for (let element of taskElements) {
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

  return mail;
};

// TODO Zmieniaj dynamicznie godziny po zmianie checkboxa!
export const sendInvoiceMail = (e) => {
  const el = e.target;
  const companyId = el.id.split("-").at(-1);
  const mail = getCompanyReportData(companyId);
  fetch(window.location.origin + "/sendmail", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRF-TOKEN": document.cookie.match(
        /csrf_access_token=([0-9a-zA-Z\-]+)/
      )[1],
    },
    credentials: "same-origin",
    body: JSON.stringify(mail),
  })
    .then((res) => {
      if (!res.ok) {
        return res.text().then((text) => {
          throw new Error(text);
        });
      } else {
        return res.json();
      }
    })
    .then((data) => {
      if (data.message === "success") {
        alert("Pomyślnie wysłano wiadomość!");
      }
    })
    .catch((e) => {
      alert("Nie udało sie wysłać maila");
      console.log(e);
    });
};

export const viewMail = (e) => {
  const el = e.target;
  const companyId = el.classList.item(2).split("-").at(-1);
  const mail = getCompanyReportData(companyId);
  const mailModal = new bootstrap.Modal(
    document.getElementById("mail-display")
  );

  fetch(window.location.origin + "/sendmail?view=true", {
    method: "POST",
    credentials: "same-origin",
    body: JSON.stringify(mail),
    headers: {
      "X-CSRF-TOKEN": document.cookie.match(
        /csrf_access_token=([0-9a-zA-Z\-]+)/
      )[1],
    },
  })
    .then((res) => {
      if (!res.ok) {
        return res.text().then((text) => {
          throw new Error(text);
        });
      } else {
        return res.text();
      }
    })
    .then((text) => {
      document.getElementById("mail-body").innerHTML = text;
      mailModal.show();
    })
    .catch((e) => {
      alert("Nie udało sie wygenerować podglądu");
      console.log(e);
    });
  const sendMailButton = document.getElementsByClassName("send-mail")[0];
  sendMailButton.setAttribute("id", `send-mail-${companyId}`);
};

export const viewMails = (e) => {
  const mails = [...document.querySelectorAll(".invoice-checkbox:checked")]
    .map((el) => el.classList.item(2).split("-").at(-1))
    .map((companyId) => getCompanyReportData(companyId));
  const multipleMailModal = new bootstrap.Modal(
    document.getElementById("multiple-mail-display")
  );
  fetch(window.location.origin + "/sendmails?view=true", {
    method: "POST",
    credentials: "same-origin",
    body: JSON.stringify({ mails: mails }),
    headers: {
      "X-CSRF-TOKEN": document.cookie.match(
        /csrf_access_token=([0-9a-zA-Z\-]+)/
      )[1],
    },
  })
    .then((res) => {
      if (!res.ok) {
        return res.text().then((text) => {
          throw new Error(text);
        });
      } else {
        return res.json();
      }
    })
    .then((data) => {
      let innerHTML = "";
      for (let view_idx in data["views"]) {
        innerHTML += `<div class="carousel-item${
          view_idx == 0 ? " active" : ""
        }">${data["views"][view_idx]}</div>`;
      }
      document.getElementById("mails-carousel").innerHTML = innerHTML;
      multipleMailModal.show();
    })
    .catch((e) => {
      alert("Nie udało sie wygenerować podglądu");
      console.log(e);
    });
};

export const sendMails = (e) => {
  const mails = [...document.querySelectorAll(".invoice-checkbox:checked")]
    .map((el) => el.classList.item(2).split("-").at(-1))
    .map((companyId) => getCompanyReportData(companyId));

  fetch(window.location.origin + "/sendmails", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRF-TOKEN": document.cookie.match(
        /csrf_access_token=([0-9a-zA-Z\-]+)/
      )[1],
    },
    credentials: "same-origin",
    body: JSON.stringify({ mails: mails }),
  })
    .then((res) => {
      if (!res.ok) {
        return res.text().then((text) => {
          throw new Error(text);
        });
      } else {
        return res.json();
      }
    })
    .then((data) => {
      if (data.message === "success") {
        alert("Pomyślnie wysłano wiadomość!");
      }
    })
    .catch((e) => {
      alert("Nie udało sie wysłać maila");
      console.log(e);
    });
};
