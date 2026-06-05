/* =========================================
   CHOICES INITIALIZER
========================================= */

function initializeChoices(parent = document) {

    if (typeof Choices === "undefined") {

        return

    }

    parent.querySelectorAll(

        "select.form-select:not(.no-choices)"

    ).forEach(function(select){

        if (

            select.dataset.choicesInitialized

        ) {

            return

        }

        new Choices(

            select,

            {

                searchEnabled: true,

                itemSelectText: "",

                shouldSort: false,

                allowHTML: false,

                searchResultLimit: 100,

                renderChoiceLimit: 100,

                placeholder: true,

                placeholderValue:

                    select.dataset.placeholder ||

                    "Select an option"

            }

        )

        select.dataset.choicesInitialized = "true"

    })

}



/* =========================================
   INITIAL LOAD
========================================= */

document.addEventListener(

    "DOMContentLoaded",

    function(){

        initializeChoices(document)

    }

)



/* =========================================
   HTMX SUPPORT
========================================= */

document.body.addEventListener(

    "htmx:afterSettle",

    function(event){

        initializeChoices(

            event.target

        )

    }

)