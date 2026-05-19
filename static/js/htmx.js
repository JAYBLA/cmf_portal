document.addEventListener("DOMContentLoaded", function () {

    // =========================================
    // GLOBAL MODAL ELEMENT
    // =========================================

    const modalElement = document.getElementById("globalModal")



    // =========================================
    // OPEN MODAL AFTER HTMX SWAP
    // =========================================

    document.body.addEventListener("htmx:afterSwap", function (event) {

        // ONLY HANDLE MODAL CONTENT

        if (event.detail.target.id === "modal-body") {

            let modal = bootstrap.Modal.getOrCreateInstance(
                modalElement
            )

            modal.show()


            // =========================================
            // INITIALIZE TOMSELECT INSIDE MODAL
            // =========================================

            initializeTomSelect(modalElement)

        }

    })



    // =========================================
    // CLOSE MODAL VIA HTMX EVENT
    // =========================================

    document.body.addEventListener("closeModal", function () {

        let modal = bootstrap.Modal.getInstance(
            modalElement
        )

        if (modal) {

            modal.hide()

        }

    })



    // =========================================
    // CLEAN MODAL CONTENT AFTER CLOSE
    // =========================================

    modalElement.addEventListener("hidden.bs.modal", function () {

        document.getElementById("modal-body").innerHTML = ""

    })



    // =========================================
    // GLOBAL HTMX ERROR HANDLER
    // =========================================

    document.body.addEventListener("htmx:responseError", function (event) {

        console.error(event)

        alert("An error occurred. Please try again.")

    })



    // =========================================
    // GLOBAL LOADING INDICATOR
    // =========================================

    document.body.addEventListener("htmx:beforeRequest", function () {

        document.body.classList.add("loading")

    })


    document.body.addEventListener("htmx:afterRequest", function () {

        document.body.classList.remove("loading")

    })

})



/* =========================================
   TOM SELECT INITIALIZER
========================================= */

function initializeTomSelect(parent = document) {

    parent.querySelectorAll(".tom-select").forEach(function (select) {

        // PREVENT DOUBLE INITIALIZATION

        if (select.tomselect) {

            return

        }

        new TomSelect(select, {

            create: false,

            maxOptions: 500,

            allowEmptyOption: true,

            preload: true,

            closeAfterSelect: true,

            dropdownParent: "body",

            placeholder:
                select.dataset.placeholder ||
                "Select an option",

            sortField: {

                field: "text",

                direction: "asc"

            },

            render: {

                no_results: function () {

                    return `
                        <div class="no-results p-2 text-muted">
                            No results found
                        </div>
                    `
                }

            },

            onInitialize: function () {

                // FORCE HIGH Z-INDEX

                this.dropdown.style.zIndex = 999999

            }

        })

    })

}

document.body.addEventListener("purchaseChanged", function () {

    htmx.ajax(
        "GET",
        "/purchases/table/",
        {
            target: "#purchase-table-body",
            swap: "outerHTML"
        }
    )

})