from django.http import Http404
from django.urls import reverse
from django.views.generic import CreateView, ListView
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import F, Count

from .models import ConversationModel, MessageModel, ThoughtModel
from .forms import ConversationCreateForm


class ConversationListView(ListView):
    template_name = "conversation_list.html"
    queryset = ConversationModel.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query = self.request.GET.get("q", "")
        vector = SearchVector("title")
        search_query = SearchQuery(query)
        object_list = (ConversationModel.objects.filter(title__icontains=query).annotate(
            rank=SearchRank(vector, search_query), content=F("title"), date_time=F("date"),
            sub_content_count=Count('messagemodel')).order_by("-rank"))

        context.update({
            "object_list": object_list,
            "has_search": True,
            "menu_title": "Conversations",
            "prev_page": None,
        })
        return context


class ConversationCreateView(CreateView):
    template_name = "conversation_create.html"
    form_class = ConversationCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "menu_title": "Messages",
            "prev_page": reverse("chat:conversations"),
        })
        return context


class MessageListView(CreateView):
    template_name = "messages.html"
    model = MessageModel
    fields = ["content", "date_time"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        conv_id = self.kwargs.get("id")
        try:
            context["conversation"] = ConversationModel.objects.get(id=conv_id)
        except ConversationModel.DoesNotExist:
            raise Http404("Conversation does not exist.")
        query = self.request.GET.get("q", "")
        vector = SearchVector("content")
        search_query = SearchQuery(query)
        object_list = (
            MessageModel.objects.filter(conversation_id=conv_id, content__icontains=query)
            .annotate(rank=SearchRank(vector, search_query), sub_content_count=Count("thoughtmodel")
            ).order_by("-rank")
        )

        context.update({
            "object_list": object_list,
            "has_search": True,
            "menu_title": "Messages",
            "prev_page": reverse("chat:conversations"),
        })
        return context

    def form_valid(self, form):
        form.instance.conversation_id = ConversationModel.objects.get(id=self.kwargs.get("id"))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("chat:messages", kwargs={"id": self.kwargs.get("id")})


class ThoughtListView(CreateView):
    template_name = "thoughts.html"
    model = ThoughtModel
    fields = ["content", "date_time"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["has_search"] = False
        context["menu_title"] = "Thoughts"

        msg_id = self.kwargs.get("id")
        try:
            cur_msg_obj = MessageModel.objects.get(id=msg_id)
        except ConversationModel.DoesNotExist:
            raise Http404("Message does not exist.")
        object_list = ThoughtModel.objects.filter(message_id=msg_id)
        context["object_list"] = object_list
        context["prev_page"] = reverse("chat:messages", kwargs={"id": cur_msg_obj.conversation_id.id})
        context["message"] = cur_msg_obj
        return context

    def form_valid(self, form):
        form.instance.message_id = MessageModel.objects.get(id=self.kwargs.get("id"))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("chat:thoughts", kwargs={"id": self.kwargs.get("id")})
