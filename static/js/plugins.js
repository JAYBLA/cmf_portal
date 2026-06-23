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
  container.querySelectorAll(".choices-select").forEach(function (element) {
    if (element.dataset.choicesLoaded) {
      return;
    }

    new Choices(element, {
      searchEnabled: true,

      itemSelectText: "",

      shouldSort: false,
    });

    element.dataset.choicesLoaded = "true";
  });
}

/* =========================================
   FLATPICKR
========================================= */

function initializeFlatpickr(container = document) {
  container.querySelectorAll(".flatpickr").forEach(function (element) {
    if (element._flatpickr) {
      return;
    }

    flatpickr(element, {
      dateFormat: "Y-m-d",
      allowInput: true,
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

      pageLength: 25,

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