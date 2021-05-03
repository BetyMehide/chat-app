from datetime import datetime

from django.test import TestCase, Client
from django.db.utils import IntegrityError
from lxml import html

from chat.models import ConversationModel, MessageModel, ThoughtModel


c = Client()


class ConversationModelTestCase(TestCase):
    def setUp(self, **kwargs):
        cur_id = kwargs.get("id", 1)
        values = {
            "title": kwargs.get("title", f"test {cur_id}"),
            "description": kwargs.get("description", "test"),
            "date": kwargs.get("date", datetime(2021, 1, 1)),
            "id": cur_id
        }
        ConversationModel.objects.create(**values)

    def test_get_absolute_url(self):
        conversation = ConversationModel.objects.get(id=1)
        self.assertEqual(conversation.get_absolute_url(), "/chat/1/")


class MessageModelTestCase(TestCase):
    def setUp(self, **kwargs):
        conv_id = kwargs.get("conversation_id", 1)
        values = {
            "content": kwargs.get("content", "test"),
            "date_time": kwargs.get("date_time", datetime(2021, 1, 1, 1, 1, 1)),
            "id": kwargs.get("id", 1),
        }
        if not ConversationModel.objects.filter(id=conv_id).first():
            ConversationModelTestCase().setUp(id=conv_id)
        MessageModel.objects.create(
            conversation_id=ConversationModel.objects.get(id=conv_id),
            **values)

    def test_get_absolute_url(self):
        message = MessageModel.objects.get(id=1)
        self.assertEqual(message.get_absolute_url(), "/chat/msg/1/")


class ThoughtModelTestCase(TestCase):
    def setUp(self, **kwargs):
        msg_id = kwargs.get("message_id", 1)
        values = {
            "content": kwargs.get("content", "test"),
            "date_time": kwargs.get("date_time", datetime(2021, 1, 1, 1, 1, 1)),
            "id": kwargs.get("id", 1),
        }
        if not MessageModel.objects.filter(id=msg_id).first():
            MessageModelTestCase().setUp(id=msg_id, conversation_id=kwargs.get("conversation_id", 1))
        ThoughtModel.objects.create(
            message_id=MessageModel.objects.get(id=msg_id),
            **values)


class ConversationSearchTestCase(TestCase):
    title_to_search = "Test"
    title_to_ignore = "Crash"

    def setUp(self):
        mock_db = ConversationModelTestCase()
        mock_db.setUp(id=1, title=self.title_to_search)
        mock_db.setUp(id=2, title=self.title_to_ignore)

    def test_conversation_search(self):
        response = c.get("/chat/", {"q": self.title_to_search})
        self.assertEqual(response.status_code, 200)
        assert self.title_to_ignore not in response.content.decode("utf-8")
        assert self.title_to_search in response.content.decode("utf-8")


class MessageSearchTestCase(TestCase):
    content_to_search = "Test"
    content_to_ignore = "Crash"

    def setUp(self):
        mock_db = MessageModelTestCase()
        mock_db.setUp(id=1, content=self.content_to_search)
        mock_db.setUp(id=2, content=self.content_to_ignore)

    def test_message_search(self):
        response = c.get("/chat/1/", {"q": self.content_to_search})
        self.assertEqual(response.status_code, 200)
        assert self.content_to_ignore not in response.content.decode("utf-8")
        assert self.content_to_search in response.content.decode("utf-8")


class MessageListTestCase(TestCase):
    def setUp(self):
        mock_db = MessageModelTestCase()
        mock_db.setUp(id=1, conversation_id=1)
        mock_db.setUp(id=2, conversation_id=1)
        mock_db.setUp(id=3, conversation_id=2)

    def test_message_list(self):
        response = c.get("/chat/1/")
        self.assertEqual(response.status_code, 200)
        root = html.fromstring(response.content)
        # only contains messages for conversation with id 1
        self.assertEqual(len(root.xpath(".//a[contains(@class, 'list-group-item')]")), 2)


class ThoughtListTestCase(TestCase):
    def setUp(self):
        mock_db = ThoughtModelTestCase()
        mock_db.setUp(id=1, message_id=1)
        mock_db.setUp(id=2, message_id=1)
        mock_db.setUp(id=3, message_id=2)

    def test_thought_filtering(self):
        response = c.get("/chat/msg/1", follow=True)
        self.assertEqual(response.status_code, 200)
        root = html.fromstring(response.content)
        # only contains thoughts for message with id 1
        self.assertEqual(len(root.xpath(".//a[contains(@class, 'list-group-item')]")), 2)


class CreateNewTestCase(TestCase):
    def test_create_new_conversation(self):
        new_conv_data = {
            "title": "test title",
            "description": "test description",
            "date": "2021-1-1",
        }
        init_convs = len(ConversationModel.objects.all())

        response = c.post("/chat/create_conversation/", new_conv_data, follow=True)
        self.assertEqual(response.status_code, 200)
        root = html.fromstring(response.content)
        # make sure the redirect to messages page worked
        self.assertEqual(root.xpath(".//nav[contains(@class, 'navbar')]/h1/text()")[0], "Messages")
        new_convs = len(ConversationModel.objects.all())
        self.assertEqual(new_convs, init_convs + 1)
        assert ConversationModel.objects.filter(title=new_conv_data["title"])

    def test_create_new_conversation_bad_data(self):
        mock_db = ConversationModelTestCase()
        common_title = "test"
        mock_db.setUp(id=1, title=common_title)
        new_conv_data = {
            "title": common_title,
            "description": "test description",
            "date": "2021-1-1",
        }
        init_convs = len(ConversationModel.objects.all())

        response = c.post("/chat/create_conversation/", new_conv_data, follow=True)
        self.assertEqual(response.status_code, 200)
        new_convs = len(ConversationModel.objects.all())
        self.assertEqual(new_convs, init_convs)


class CreateNewMessageTestCase(TestCase):
    def setUp(self):
        mock_db = ConversationModelTestCase()
        mock_db.setUp(id=1)

    def test_create_new_message(self):
        new_msg_data = {
            "content": "test message",
            "date_time": "2021-01-10 08:10:10",
        }
        init_msg_count = len(MessageModel.objects.all())

        response = c.post("/chat/1/", new_msg_data, follow=True)
        self.assertEqual(response.status_code, 200)
        new_msg_count = len(MessageModel.objects.all())
        self.assertEqual(new_msg_count, init_msg_count + 1)
        assert MessageModel.objects.filter(content=new_msg_data["content"])

    def test_create_new_message_bad_data(self):
        new_msg_data = {
            "content": "",
            "date_time": "2021-01-10 08:10:10",
        }
        init_msg_count = len(MessageModel.objects.all())

        response = c.post("/chat/1/", new_msg_data, follow=True)
        self.assertEqual(response.status_code, 200)
        new_msg_count = len(MessageModel.objects.all())
        self.assertEqual(new_msg_count, init_msg_count)
        assert not MessageModel.objects.filter(content=new_msg_data["content"])


class CreateNewThoughtTestCase(TestCase):
    def setUp(self):
        mock_db = MessageModelTestCase()
        mock_db.setUp(id=1)

    def test_create_new_thought(self):
        new_thought_data = {
            "content": "test thought",
            "date_time": "2021-01-10 08:10:10",
        }
        init_thought_count = len(ThoughtModel.objects.all())

        response = c.post("/chat/msg/1/", new_thought_data, follow=True)
        self.assertEqual(response.status_code, 200)
        new_thought_count = len(ThoughtModel.objects.all())
        self.assertEqual(new_thought_count, init_thought_count + 1)
        assert ThoughtModel.objects.filter(content=new_thought_data["content"])

    def test_create_new_thought_bad_data(self):
        new_thought_data = {
            "content": "test thought",
            "date_time": "",
        }
        init_thought_count = len(ThoughtModel.objects.all())

        response = c.post("/chat/msg/1/", new_thought_data, follow=True)
        self.assertEqual(response.status_code, 200)
        new_thought_count = len(ThoughtModel.objects.all())
        self.assertEqual(new_thought_count, init_thought_count)
        assert not ThoughtModel.objects.filter(content=new_thought_data["content"])
