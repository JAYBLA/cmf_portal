/* =========================================
   INITIALIZE ALL PLUGINS (GLOBAL)
========================================= */

function initializePlugins(container = document) {
  if (typeof initializeTooltips === "function") {
    initializeTooltips(container);
  }

  if (typeof initializeChoices === "function") {
    initializeChoices(container);
  }

  if (typeof initializeFlatpickr === "function") {
    initializeFlatpickr(container);
  }

  if (typeof initializeTinyMCE === "function") {
    initializeTinyMCE(container);
  }

  if (typeof initializeDataTables === "function") {
    initializeDataTables(container);
  }

  if (typeof initializeAutoFormsets === "function") {
    initializeAutoFormsets(container);
  }

  if (typeof initializePurchaseCategory === "function") {
    initializePurchaseCategory(container);
  }
}

/* =========================================
   GLOBAL HTMX APPLICATION
========================================= */

document.addEventListener(
  "DOMContentLoaded",

  function () {
    const modalElement = document.getElementById("globalModal");

    const modalBody = document.getElementById("modal-body");

    /* =====================================
           OPEN MODAL AFTER SWAP
        ===================================== */

    document.body.addEventListener(
      "htmx:afterSwap",

      function (event) {
        if (event.detail.target.id === "modal-body") {
          const modal = bootstrap.Modal.getOrCreateInstance(modalElement);

          modal.show();

          initializePlugins(event.detail.target);
        }
      },
    );

    /* =====================================
           REINITIALIZE PLUGINS
        ===================================== */

    document.body.addEventListener(
      "htmx:afterSettle",

      function (event) {
        initializePlugins(event.target);
      },
    );

    /* =====================================
           CLOSE MODAL
        ===================================== */

    document.body.addEventListener(
      "closeModal",

      function () {
        const modal = bootstrap.Modal.getInstance(modalElement);

        if (modal) {
          modal.hide();
        }
      },
    );

    /* =====================================
           RECORD SAVED
        ===================================== */

    document.body.addEventListener(
      "recordSaved",

      function () {
        const modal = bootstrap.Modal.getInstance(modalElement);

        if (modal) {
          modal.hide();
        }

        if (typeof Swal !== "undefined") {
          Swal.fire({
            icon: "success",

            title: "Saved Successfully",

            timer: 1500,

            showConfirmButton: false,
          });
        }
      },
    );

    /* =====================================
           REFRESH TABLE
        ===================================== */

    document.body.addEventListener(
      "refreshTable",

      function () {
        const container = document.getElementById("table-container");

        if (!container) {
          return;
        }

        const refreshUrl = container.dataset.refreshUrl;

        if (!refreshUrl) {
          console.warn("Missing data-refresh-url on #table-container");

          return;
        }

        htmx.ajax("GET", refreshUrl, {
          target: "#table-container",
          swap: "innerHTML",
        });
      },
    );

    /* =====================================
           SHOW MESSAGE
        ===================================== */

    document.body.addEventListener(
      "showMessage",

      function (event) {
        if (typeof Swal === "undefined") {
          return;
        }

        Swal.fire({
          icon: event.detail.type || "success",

          title: event.detail.message || "Success",

          timer: 2500,

          showConfirmButton: false,
        });
      },
    );

    /* =====================================
           CLEAR MODAL CONTENT
        ===================================== */

    if (modalElement) {
      modalElement.addEventListener(
        "hidden.bs.modal",

        function () {
          if (modalBody) {
            modalBody.innerHTML = "";
          }
        },
      );
    }

    /* =====================================
           RESPONSE ERRORS
        ===================================== */

    document.body.addEventListener(
      "htmx:responseError",

      function (event) {
        console.error("HTMX Response Error:", event);

        if (typeof Swal !== "undefined") {
          Swal.fire({
            icon: "error",

            title: "Request Failed",

            text: "An error occurred while processing your request.",
          });
        }
      },
    );

    /* =====================================
           NETWORK ERRORS
        ===================================== */

    document.body.addEventListener(
      "htmx:sendError",

      function (event) {
        console.error("HTMX Network Error:", event);

        if (typeof Swal !== "undefined") {
          Swal.fire({
            icon: "error",

            title: "Network Error",

            text: "Unable to connect to the server.",
          });
        }
      },
    );

    /* =====================================
           LOADING START
        ===================================== */

    document.body.addEventListener(
      "htmx:beforeRequest",

      function () {
        document.body.classList.add("loading");
      },
    );

    /* =====================================
           LOADING END
        ===================================== */

    document.body.addEventListener(
      "htmx:afterRequest",

      function () {
        document.body.classList.remove("loading");
      },
    );

    /* =====================================
           INITIAL PAGE LOAD
        ===================================== */

    initializePlugins(document);
  },
);
