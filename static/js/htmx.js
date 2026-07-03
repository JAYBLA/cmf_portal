/* =========================================
   INITIALIZE ALL PLUGINS (GLOBAL)
========================================= */

function initializePlugins(container = document) {
  if (
    !container ||
    typeof container.querySelectorAll !== "function"
  ) {
    container = document;
  }


  /* =========================================
     TOOLTIPS
  ========================================= */

  if (typeof initializeTooltips === "function") {
    initializeTooltips(container);
  }


  /* =========================================
     CHOICES.JS
  ========================================= */

  if (typeof initializeChoices === "function") {
    initializeChoices(container);
  }


  /* =========================================
     FLATPICKR
  ========================================= */

  if (typeof initializeFlatpickr === "function") {
    initializeFlatpickr(container);
  }


  /* =========================================
     TINYMCE
  ========================================= */

  if (typeof initializeTinyMCE === "function") {
    initializeTinyMCE(container);
  }


  /* =========================================
     DATA TABLES
  ========================================= */

  if (typeof initializeDataTables === "function") {
    initializeDataTables(container);
  }


  /* =========================================
     AUTO FORMSETS
  ========================================= */

  if (typeof initializeAutoFormsets === "function") {
    initializeAutoFormsets(container);
  }


  /* =========================================
     PURCHASE CATEGORY
  ========================================= */

  if (
    typeof initializePurchaseCategory === "function"
  ) {
    initializePurchaseCategory(container);
  }


  /* =========================================
     TOASTR / DJANGO MESSAGES
  ========================================= */

  if (typeof initializeMessages === "function") {
    initializeMessages(container);
  }
}


/* =========================================
   GLOBAL HTMX APPLICATION
========================================= */

document.addEventListener(
  "DOMContentLoaded",

  function () {

    const modalElement =
      document.getElementById("globalModal");

    const modalBody =
      document.getElementById("modal-body");


    /* =====================================
       INITIAL PAGE LOAD
    ===================================== */

    initializePlugins(document);


    /* =====================================
       OPEN MODAL AFTER SWAP
    ===================================== */

    document.body.addEventListener(
      "htmx:afterSwap",

      function (event) {

        const target =
          event.detail.target;

        if (!target) {
          return;
        }

        if (
          target.id === "modal-body" &&
          modalElement
        ) {

          const modal =
            bootstrap.Modal.getOrCreateInstance(
              modalElement
            );

          modal.show();
        }

      }
    );


    /* =====================================
       INITIALIZE PLUGINS AFTER HTMX SETTLE
    ===================================== */

    document.body.addEventListener(
      "htmx:afterSettle",

      function (event) {

        const target =
          event.detail.target;

        if (!target) {
          return;
        }

        initializePlugins(target);

      }
    );


    /* =====================================
       CLOSE MODAL
    ===================================== */

    document.body.addEventListener(
      "closeModal",

      function () {

        if (!modalElement) {
          return;
        }

        const modal =
          bootstrap.Modal.getInstance(
            modalElement
          );

        if (modal) {
          modal.hide();
        }

      }
    );


    /* =====================================
       RECORD SAVED
    ===================================== */

    document.body.addEventListener(
      "recordSaved",

      function () {

        if (!modalElement) {
          return;
        }

        const modal =
          bootstrap.Modal.getInstance(
            modalElement
          );

        if (modal) {
          modal.hide();
        }

      }
    );


    /* =====================================
       REFRESH TABLE
    ===================================== */

    document.body.addEventListener(
      "refreshTable",

      function () {

        const tableContainer =
          document.getElementById(
            "table-container"
          );

        if (!tableContainer) {
          return;
        }

        const refreshUrl =
          tableContainer.dataset.refreshUrl;

        if (!refreshUrl) {

          console.warn(
            "Missing data-refresh-url on #table-container"
          );

          return;
        }


        htmx.ajax(
          "GET",

          refreshUrl,

          {
            target: "#table-container",

            swap: "innerHTML",
          }
        );

      }
    );


    /* =====================================
       SHOW TOASTR MESSAGE
    ===================================== */

    document.body.addEventListener(
      "showMessage",

      function (event) {

        const detail =
          event.detail || {};

        if (typeof showMessage !== "function") {

          console.warn(
            "Global showMessage() is not loaded."
          );

          return;
        }


        showMessage({
          type:
            detail.type || "info",

          message:
            detail.message ||
            "Operation completed.",

          title:
            detail.title || "",
        });

      }
    );


    /* =====================================
       CLEAR MODAL CONTENT
    ===================================== */

    if (modalElement) {

      modalElement.addEventListener(
        "hidden.bs.modal",

        function () {

          if (!modalBody) {
            return;
          }


          /* =================================
             DESTROY FLATPICKR
          ================================= */

          modalBody
            .querySelectorAll(".flatpickr")
            .forEach(function (element) {

              if (element._flatpickr) {

                element._flatpickr.destroy();

              }

            });


          /* =================================
             REMOVE TINYMCE
          ================================= */

          if (typeof tinymce !== "undefined") {

            modalBody
              .querySelectorAll("textarea")
              .forEach(function (element) {

                if (!element.id) {
                  return;
                }

                const editor =
                  tinymce.get(element.id);

                if (editor) {
                  editor.remove();
                }

              });

          }


          /* =================================
             CLEAR MODAL
          ================================= */

          modalBody.innerHTML = "";

        }
      );

    }


    /* =====================================
       RESPONSE ERRORS
    ===================================== */

    document.body.addEventListener(
      "htmx:responseError",

      function (event) {

        console.error(
          "HTMX Response Error:",
          event
        );


        if (typeof showMessage !== "function") {
          return;
        }


        showMessage({
          type: "error",

          message:
            "An error occurred while processing your request.",

          title:
            "Request Failed",
        });

      }
    );


    /* =====================================
       NETWORK ERRORS
    ===================================== */

    document.body.addEventListener(
      "htmx:sendError",

      function (event) {

        console.error(
          "HTMX Network Error:",
          event
        );


        if (typeof showMessage !== "function") {
          return;
        }


        showMessage({
          type: "error",

          message:
            "Unable to connect to the server.",

          title:
            "Network Error",
        });

      }
    );


    /* =====================================
       LOADING START
    ===================================== */

    document.body.addEventListener(
      "htmx:beforeRequest",

      function () {

        document.body.classList.add(
          "loading"
        );

      }
    );


    /* =====================================
       LOADING END
    ===================================== */

    document.body.addEventListener(
      "htmx:afterRequest",

      function () {

        document.body.classList.remove(
          "loading"
        );

      }
    );

  }
);