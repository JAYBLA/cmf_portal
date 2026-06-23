import json

from django.shortcuts import (
    render,
    get_object_or_404
)

from django.http import HttpResponse

from django.db.models import ProtectedError

from .models import ClearingAgent

from .forms import ClearingAgentForm


# =========================================
# CLEARING AGENT LIST
# =========================================

def clearing_agent_list(request):

    agents = ClearingAgent.objects.order_by(
        "-created_at"
    )

    context = {
        "agents": agents
    }

    return render(
        request,
        "clearing_agents/list.html",
        context
    )


# =========================================
# CLEARING AGENT TABLE
# =========================================

def clearing_agent_table(request):

    agents = ClearingAgent.objects.order_by(
        "-created_at"
    )

    context = {
        "agents": agents
    }

    return render(
        request,
        "clearing_agents/table.html",
        context
    )


# =========================================
# CREATE CLEARING AGENT
# =========================================

def clearing_agent_create(request):

    form = ClearingAgentForm(
        request.POST or None
    )

    if request.method == "POST":

        if form.is_valid():

            form.save()

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps({

                "recordSaved": True,

                "refreshTable": True,

                "showMessage": {

                    "type": "success",

                    "message":
                        "Clearing agent created successfully."

                }

            })

            return response

    context = {
        "form": form
    }

    return render(
        request,
        "clearing_agents/form.html",
        context
    )


# =========================================
# UPDATE CLEARING AGENT
# =========================================

def clearing_agent_update(request, pk):

    agent = get_object_or_404(
        ClearingAgent,
        pk=pk
    )

    form = ClearingAgentForm(
        request.POST or None,
        instance=agent
    )

    if request.method == "POST":

        if form.is_valid():

            form.save()

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps({

                "recordSaved": True,

                "refreshTable": True,

                "showMessage": {

                    "type": "success",

                    "message":
                        "Clearing agent updated successfully."

                }

            })

            return response

    context = {

        "form": form,

        "agent": agent

    }

    return render(
        request,
        "clearing_agents/form.html",
        context
    )


# =========================================
# DELETE CLEARING AGENT
# =========================================

def clearing_agent_delete(request, pk):

    agent = get_object_or_404(
        ClearingAgent,
        pk=pk
    )

    if request.method == "POST":

        try:

            agent.delete()

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps({

                "recordSaved": True,

                "refreshTable": True,

                "showMessage": {

                    "type": "success",

                    "message":
                        "Clearing agent deleted successfully."

                }

            })

            return response

        except ProtectedError:

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps({

                "showMessage": {

                    "type": "error",

                    "message":
                        (
                            "This clearing agent is already "
                            "used in transactions and "
                            "cannot be deleted."
                        )

                }

            })

            return response

    context = {
        "agent": agent
    }

    return render(
        request,
        "clearing_agents/delete.html",
        context
    )