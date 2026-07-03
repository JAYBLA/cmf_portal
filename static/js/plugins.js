/* =========================================
   TOOLTIPS
========================================= */

function initializeTooltips(container = document) {
  container
    .querySelectorAll('[data-bs-toggle="tooltip"]')
    .forEach(function (element) {
      bootstrap.Tooltip.getOrCreateInstance(element);
    });
}

/* =========================================
   CHOICES.JS
========================================= */

function initializeChoices(container = document) {
  if (
    !container ||
    typeof container.querySelectorAll !== "function"
  ) {
    container = document;
  }


  /* =========================================
     NORMAL SELECT
  ========================================= */

  container
    .querySelectorAll(".choices-select")
    .forEach(function (element) {

      if (
        element.dataset.choicesLoaded === "true"
      ) {
        return;
      }

      new Choices(element, {
        searchEnabled: true,
        itemSelectText: "",
        shouldSort: false,
      });

      element.dataset.choicesLoaded = "true";
    });


  /* =========================================
     TAG / CREATE NEW VALUE
  ========================================= */

  container
    .querySelectorAll(".choices-tags")
    .forEach(function (element) {

      if (
        element.dataset.choicesLoaded === "true"
      ) {
        return;
      }


      /* =====================================
         INITIALIZE CHOICES
      ===================================== */

      const choices = new Choices(
        element,
        {
          searchEnabled: true,

          searchChoices: true,

          itemSelectText: "",

          shouldSort: false,

          duplicateItemsAllowed: false,

          allowHTML: false,

          noResultsText:
            "Press Enter to add customer",

          noChoicesText:
            "No customers available",
        }
      );


      /* =====================================
         GET SEARCH INPUT
      ===================================== */

      const searchInput =
        choices.input.element;


      /* =====================================
         CREATE CUSTOMER ON ENTER
      ===================================== */

      searchInput.addEventListener(
        "keydown",

        function (event) {

          if (event.key !== "Enter") {
            return;
          }


          const value =
            searchInput.value.trim();


          if (!value) {
            return;
          }


          /* =================================
             CHECK EXISTING CUSTOMER
          ================================= */

          const existingOption =
            Array.from(element.options).find(
              function (option) {

                return (
                  option.text
                    .trim()
                    .toLowerCase()
                  ===
                  value.toLowerCase()
                );

              }
            );


          if (existingOption) {

            return;

          }


          /* =================================
             PREVENT FORM SUBMISSION
          ================================= */

          event.preventDefault();

          event.stopPropagation();


          /* =================================
             ADD NEW CUSTOMER
          ================================= */

          choices.setChoices(
            [
              {
                value: value,

                label: value,

                selected: true,
              },
            ],

            "value",

            "label",

            false
          );


          /* =================================
             CLEAR SEARCH
          ================================= */

          choices.clearInput();

        }
      );


      element.dataset.choicesLoaded = "true";
    });
}

/* =========================================
   FLATPICKR
========================================= */

function initializeFlatpickr(container = document) {
  if (
    !container ||
    typeof container.querySelectorAll !== "function"
  ) {
    container = document;
  }

  const elements = [];

  // =========================================
  // INCLUDE CONTAINER ITSELF
  // =========================================

  if (
    container.matches &&
    container.matches(".flatpickr")
  ) {
    elements.push(container);
  }

  // =========================================
  // FIND FLATPICKR FIELDS
  // =========================================

  elements.push(
    ...container.querySelectorAll(".flatpickr")
  );

  // =========================================
  // INITIALIZE
  // =========================================

  elements.forEach(function (element) {
    if (element._flatpickr) {
      return;
    }

    flatpickr(element, {
      dateFormat: "Y-m-d",
      allowInput: false,
      clickOpens: true,
      closeOnSelect: true,
    });
  });
}
/* =========================================
   TINYMCE
========================================= */

function initializeTinyMCE(container = document) {
  container.querySelectorAll(".tinymce").forEach(function (element) {
    if (tinymce.get(element.id)) {
      return;
    }

    tinymce.init({
      selector: "#" + element.id,

      height: 300,

      menubar: false,

      plugins: "lists link table code",

      toolbar: "undo redo | bold italic | bullist numlist | link table | code",
    });
  });
}

/* =========================================
   DATATABLES
========================================= */

function initializeDataTables(container = document) {
  container.querySelectorAll("#responsiveTable").forEach(function (table) {
    if ($.fn.DataTable.isDataTable(table)) {
      return;
    }

    $(table).DataTable({
      responsive: true,

      pageLength: 10,

      ordering: true,

      autoWidth: false,
    });
  });
}

/* =========================================
   AUTO FORMSET ROWS
========================================= */

function initializeAutoFormsets(container = document) {

    const template =
        container.querySelector(
            "#empty-form-template"
        )

    if (!template) return

    const tbody =
        container.querySelector("tbody")

    if (!tbody) return

    const managementForm =
        container.querySelector(
            '[name$="-TOTAL_FORMS"]'
        )

    if (!managementForm) return

    /* =====================================
       PREVENT DUPLICATE BINDINGS
    ===================================== */

    if (tbody.dataset.autoFormsetLoaded) {
        return
    }

    tbody.dataset.autoFormsetLoaded = "true"

    /* =====================================
       ADD ROW
    ===================================== */

    function addRow() {

        const formIndex =
            parseInt(
                managementForm.value
            )

        const html =
            template.innerHTML.replace(
                /__prefix__/g,
                formIndex
            )

        tbody.insertAdjacentHTML(
            "beforeend",
            html
        )

        managementForm.value =
            formIndex + 1

        const newRow =
            tbody.lastElementChild

        if (
            typeof initializePlugins ===
            "function"
        ) {

            initializePlugins(
                newRow
            )

        }

    }

    /* =====================================
       CHECK IF ROW HAS DATA
    ===================================== */

    function rowHasData(row) {

        return Array.from(

            row.querySelectorAll(
                "input, select, textarea"
            )

        ).some(function (field) {

            if (
                field.type === "hidden" ||
                field.name.includes("DELETE")
            ) {
                return false
            }

            if (
                field.type === "file"
            ) {
                return (
                    field.files &&
                    field.files.length > 0
                )
            }

            return (
                field.value &&
                field.value.toString().trim() !== ""
            )

        })

    }

    /* =====================================
       ENSURE EMPTY LAST ROW
    ===================================== */

    function ensureEmptyRow() {

        const rows =
            tbody.querySelectorAll("tr")

        if (!rows.length) {

            addRow()

            return

        }

        const lastRow =
            rows[rows.length - 1]

        if (
            rowHasData(lastRow)
        ) {

            addRow()

        }

    }

    /* =====================================
       AUTO CREATE ROW
    ===================================== */

    tbody.addEventListener(

        "input",

        function () {

            ensureEmptyRow()

        }

    )

    tbody.addEventListener(

        "change",

        function () {

            ensureEmptyRow()

        }

    )

    /* =====================================
       REMOVE ROW
    ===================================== */

    tbody.addEventListener(

        "click",

        function (event) {

            const removeBtn =
                event.target.closest(
                    ".remove-row"
                )

            if (!removeBtn) return

            const row =
                removeBtn.closest("tr")

            if (!row) return

            row.remove()

            ensureEmptyRow()

        }

    )

    /* =====================================
       MANUAL ADD BUTTON
    ===================================== */

    const addButton =
        container.querySelector(
            "#add-item-row"
        )

    if (addButton) {

        addButton.addEventListener(

            "click",

            function () {

                addRow()

            }

        )

    }

    /* =====================================
       INITIAL CHECK
    ===================================== */

    ensureEmptyRow()

}
/* =========================================
   PURCHASE CATEGORY LOGIC
========================================= */

function initializePurchaseCategory(container = document) {

    const category =
        container.querySelector("#purchase-category");

    const currency =
        container.querySelector("#purchase-currency");

    const exchangeRate =
        container.querySelector("#exchange-rate");

    const exchangeWrapper =
        container.querySelector("#exchange-rate-wrapper");

    if (!category || !currency) {
        return;
    }

    function updatePurchaseFields() {

        if (category.value === "international") {

            currency.value = "USD";

            if (exchangeWrapper) {
                exchangeWrapper.style.display = "";
            }

            if (exchangeRate && !exchangeRate.value) {
                exchangeRate.value = 1;
            }

        } else {

            currency.value = "TZS";

            if (exchangeRate) {
                exchangeRate.value = 1;
            }

            if (exchangeWrapper) {
                exchangeWrapper.style.display = "none";
            }
        }

        /* Prevent manual changes but still submit value */

        currency.style.pointerEvents = "none";
        currency.style.backgroundColor = "#f8f9fa";

        /* Refresh Choices */

        const choicesInstance =
            currency.closest(".choices");

        if (choicesInstance && currency.choices) {

            currency.choices.setChoiceByValue(
                currency.value
            );

        }
    }

    category.removeEventListener(
        "change",
        updatePurchaseFields
    );

    category.addEventListener(
        "change",
        updatePurchaseFields
    );

    updatePurchaseFields();
}

/* =========================================
   SALE PRODUCT PRICE
========================================= */

document.body.addEventListener(
    "change",
    async function (event) {

        const productField =
            event.target.closest(".sale-product");

        if (!productField) {
            return;
        }

        const productId =
            productField.value;

        if (!productId) {
            return;
        }

        const row =
            productField.closest("tr");

        const priceField =
            row.querySelector(".item-price");

        if (!priceField) {
            return;
        }

        try {

            const response =
                await fetch(
                    `/sales/product-price/${productId}/`
                );

            const data =
                await response.json();

            priceField.value =
                data.selling_price || 0;

            priceField.dispatchEvent(
                new Event(
                    "input",
                    { bubbles: true }
                )
            );

        } catch (error) {

            console.error(
                "Unable to load product price",
                error
            );

        }

    }
);

/* =========================================
   GLOBAL TOASTR MESSAGE
========================================= */

function showMessage(options = {}) {
  if (typeof toastr === "undefined") {
    console.warn("Toastr is not loaded.");
    return;
  }

  let type = options.type || "info";

  const message =
    options.message || "Operation completed.";

  const title =
    options.title || "";


  /* =========================================
     NORMALIZE MESSAGE TYPE
  ========================================= */

  if (type.includes("success")) {
    type = "success";
  } else if (type.includes("error")) {
    type = "error";
  } else if (type.includes("warning")) {
    type = "warning";
  } else if (type.includes("info")) {
    type = "info";
  } else if (type.includes("debug")) {
    type = "info";
  } else {
    type = "info";
  }


  /* =========================================
     TOASTR OPTIONS
  ========================================= */

  toastr.options = {
    closeButton: true,
    debug: false,
    newestOnTop: true,
    progressBar: true,
    positionClass: "toast-top-right",
    preventDuplicates: true,
    onclick: null,
    showDuration: "300",
    hideDuration: "500",
    timeOut: "3000",
    extendedTimeOut: "1000",
    showEasing: "swing",
    hideEasing: "linear",
    showMethod: "fadeIn",
    hideMethod: "fadeOut",
  };


  /* =========================================
     SHOW TOAST
  ========================================= */

  toastr[type](
    message,
    title
  );
}


/* =========================================
   INITIALIZE DJANGO MESSAGES
========================================= */

function initializeMessages(container = document) {
  if (
    !container ||
    typeof container.querySelectorAll !== "function"
  ) {
    container = document;
  }

  const messages =
    container.querySelectorAll(
      ".django-message:not([data-message-loaded])"
    );

  messages.forEach(function (element) {
    element.dataset.messageLoaded = "true";

    showMessage({
      type: element.dataset.type || "info",

      message:
        element.dataset.message || "",
    });
  });
}