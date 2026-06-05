/* =========================================
   MAIN APPLICATION
========================================= */

document.addEventListener(

    "DOMContentLoaded",

    function () {

        const modalElement = document.getElementById(
            "globalModal"
        )



        // =====================================
        // OPEN MODAL AFTER HTMX SWAP
        // =====================================

        document.body.addEventListener(

            "htmx:afterSwap",

            function (event) {

                if (

                    event.detail.target.id ===

                    "modal-body"

                ) {

                    const modal =

                        bootstrap.Modal.getOrCreateInstance(

                            modalElement

                        )

                    modal.show()

                }

            }

        )



        // =====================================
        // HTMX AFTER SETTLE
        // =====================================

        document.body.addEventListener(

            "htmx:afterSettle",

            function (event) {

                initializeTooltips(

                    event.target

                )

            }

        )



        // =====================================
        // CLOSE MODAL
        // =====================================

        document.body.addEventListener(

            "closeModal",

            function () {

                const modal =

                    bootstrap.Modal.getInstance(

                        modalElement

                    )

                if (modal) {

                    modal.hide()

                }

            }

        )



        // =====================================
        // CLEAR MODAL CONTENT
        // =====================================

        if (modalElement) {

            modalElement.addEventListener(

                "hidden.bs.modal",

                function () {

                    document.getElementById(

                        "modal-body"

                    ).innerHTML = ""

                }

            )

        }



        // =====================================
        // GLOBAL HTMX ERROR HANDLER
        // =====================================

        document.body.addEventListener(

            "htmx:responseError",

            function (event) {

                console.error(event)

                alert(

                    "An error occurred. Please try again."

                )

            }

        )



        // =====================================
        // LOADING INDICATOR
        // =====================================

        document.body.addEventListener(

            "htmx:beforeRequest",

            function () {

                document.body.classList.add(

                    "loading"

                )

            }

        )



        document.body.addEventListener(

            "htmx:afterRequest",

            function () {

                document.body.classList.remove(

                    "loading"

                )

            }

        )



        // =====================================
        // INITIAL PAGE LOAD
        // =====================================

        initializeTooltips(document)

    }

)